import time
import json
import requests
import numpy as np
import pandas as pd
from tqdm import tqdm
from typing import List
from urllib.parse import urljoin
from requests_toolbelt import MultipartEncoder
from requests_toolbelt import MultipartEncoderMonitor

from .common import common
from .common import get_uuid
from .common import decode_base64_array
from .common.https_agent import HttpsAgent
from .typing import StudyUnit


class Connector(object):
  """
  Shared functions of all platforms
  """

  def __init__(self, host: str, token: str, ssl: bool = True):
    """
    Parameters
    ----------
    host : str
      The URL of the host server, only support HTTPS connection\n
      Example:
        BBrowserX: https://talk2data.bioturing.com/t2d_index_tool/ \n
        Lens_SC: https://talk2data.bioturing.com/lens_sc/ \n
        Lens_Bulk: https://talk2data.bioturing.com/lens_bulk/ \n
    token : str
      The API token to verify authority. Generated in-app.
    """
    self.__host = host
    self.__token = token
    self.__ssl = ssl
    self.__https_agent = HttpsAgent(self.__token, self.__ssl)


  def _add_file_upload(self, folder_id, n_chunks, file_name):
    params = {
      'folder_id': folder_id,
      'n_chunks': n_chunks,
      'original_file_name': file_name
    }
    response = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/add_file_upload'),
      body=params
    )

    common.check_result_status(response)
    id = response['data'][0]['id']
    return id


  def _upload_each_file_in_chunk(
      self,
      folder_id,
      id,
      file_path,
      file_name,
      chunk_size,
      n_chunks
    ):
    file = open(file_path, 'rb')
    for chunk_order in range(n_chunks):
      chunk = file.read(chunk_size)

      if not chunk:
        raise Exception('Something went wrong')

      with tqdm(
        desc='{} - chunk_{}'.format(file_name, chunk_order),
        total=chunk_size,
        unit='MB',
        unit_scale=True,
        unit_divisor=1024,
      ) as bar:
        fields = {
          'params': json.dumps({
            'folder_id': folder_id,
            'id': id,
            'chunk': chunk_order,
            'n_chunks': n_chunks,
          }),
          'file': (file_name, chunk)
        }

        encoder = MultipartEncoder(fields=fields)
        multipart = MultipartEncoderMonitor(
          encoder, lambda monitor: bar.update(monitor.bytes_read - bar.n)
        )
        headers = {
          'Content-Type': multipart.content_type,
          'bioturing-api-token': self.__token
        }
        response = requests.post(
          urljoin(self.__host, 'api/v1/upload_chunk'),
          headers=headers,
          data=multipart,
          verify=self.__ssl
        ).json()
        if not response:
          raise Exception('Something went wrong')
        if 'status' not in response or response['status'] != 200:
          raise Exception(response)

    output_dir = response['data']['output_dir']
    return output_dir


  def upload_chunk(self, file_names, files, chunk_size):
    """
    :meta private:
    """
    folder_id = get_uuid()
    for file_name, file in zip(file_names, files):
      file_size = file.stat().st_size
      n_chunks = int(np.ceil(file_size / chunk_size))
      id = self._add_file_upload(
        folder_id,
        n_chunks,
        file_name,
      )
      output_dir = self._upload_each_file_in_chunk(
        folder_id,
        id,
        file,
        file_name,
        chunk_size,
        n_chunks
      )
    return output_dir


  def post_request(self, api_route, data={}):
    """
    :meta private:
    """
    submission_status = self.__https_agent.post(
      url=urljoin(self.__host, api_route),
      body=data
    )
    return submission_status


  def test_connection(self):
    """
    Test the connection to the host

    Returns
    ----------
    connection status : str
    """
    url = urljoin(self.__host, 'api/v1/test_connection')
    print(f'Connecting to host at {url}')
    res = self.__https_agent.post(url=url)
    if res and 'status' in res and res['status'] == 200:
      print('Connection successful')
      return True
    else:
      print('Connection failed')
    return False


  def get_submission_log(self, group_id: str, task_id: str):
    """
    :meta private:
    """
    last_status = []
    while True:
      submission_log = self.post_request(
        api_route='api/v1/get_submission_log',
        data={'task_id': task_id}
      )
      if not submission_log or 'status' not in submission_log or \
        submission_log['status'] != 200:
        print('Internal server error. Please check server log.')
        break

      if submission_log['data']['status'] == 'ERROR':
        print (submission_log['data']['log'])
        print ('Failed to summit. Please check server log.')
        break

      current_status = submission_log['data']['log'].split('\n')[:-1]
      new_status = current_status[len(last_status):]
      if len(new_status):
        print('\n'.join(new_status))

      last_status += new_status
      if submission_log['data']['status'] != 'SUCCESS':
        time.sleep(5)
        continue
      else:
        res = self.post_request(
          api_route='api/v1/commit_submission_result',
          data={
            'group_id': group_id,
            'task_id': task_id
          }
        )
        if not res or 'status' not in res:
          print('Internal server error. Please check server log.')
          break
        elif res['status'] != 200:
          if 'message' in res:
            print(f"Connection failed. {res['message']}")
          else:
            print('Connection failed.')
          break
        else:
          print('Study submitted successfully!')
          return {
            'status': True,
            'study_info': res['study_info']
          }
    return False


  def get_user_groups(self):
    """
    Get all available groups of current token

    Returns
    ----------
    List of groups' info : List[dict]
      In which:
        'group_id': uuid of the group, which will be used in further steps,\n
        'group_name': displaying name of the group
    """
    res = self.post_request(
      api_route='api/v1/get_user_groups'
    )
    if res and 'status' in res and res['status'] == 200:
      return res['data']
    raise Exception('''Something went wrong, please contact support@bioturing.com''')


  def get_user_s3(self):
    """
    Get all available groups of current token

    Returns
    ----------
    List of s3 bucket' info : List[dict]
      In which:
        'id': uuid of the s3 bucket, which will be used in further steps,\n
        'bucket': bucket of s3,\n
        'prefix': prefix of s3,\n
      ( s3_path = s3://[bucket]/[prefix]/ )
    """
    res = self.post_request(
      api_route='api/v1/get_user_s3'
    )
    if res and 'status' in res and res['status'] == 200:
      return res['data']
    raise Exception('''Something went wrong, please contact support@bioturing.com''')


  def get_shared_s3_of_group(self, group_id: str):
    """
    Get all available groups of current token

    Parameters
    ----------
    group_id : str,
      Group hash id (uuid)

    Returns
    ----------
    List of s3 bucket' info : List[dict]
      In which:
        'id': uuid of the s3 bucket, which will be used in further steps,\n
        'bucket': bucket of s3,\n
        'prefix': prefix of s3,\n
      ( s3_path = s3://[bucket]/[prefix]/ )
    """
    res = self.post_request(
      api_route='api/v1/get_shared_s3_of_group',
      data = {
        'group_id': group_id
      }
    )
    if res and 'status' in res and res['status'] == 200:
      return res['data']
    raise Exception('''Something went wrong, please contact support@bioturing.com''')


  def get_all_studies_info_in_group(
    self,
    species: str,
    group_id: str
  ):
    """
    Get info of all studies within group.

    Parameters
    -------------
    species : bioturing_connector.typing.Species.typing.Species
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    group_id : str,
          Group hash id (uuid)

    Returns
    -------------
    List of studies' info : List[dict]
      In which:
        'uuid': the uuid of study, which will be used in further steps, \n
        'study_hash_id': the displaying id of study on platform,\n
        'created_by': email of person who submitted the study,\n
    """
    data = {
      'species': species,
      'group_id': group_id
    }
    result = self.post_request(
      api_route='api/v1/get_all_studies_info_in_group',
      data=data
    )
    common.check_result_status(result)
    return result['data']


  def query_genes(
    self,
    species: str,
    study_id: str,
    gene_names: List[str],
    unit: str = StudyUnit.UNIT_RAW.value
  ):
    """
    Query genes expression of a study.

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study
    gene_names : List[str]
          Querying gene names. \n
          If gene_names=[], full matrix will be returned
    unit : bioturing_connector.typing.StudyUnit. Default 'raw'
          Expression unit\n
          Support:
            bioturing_connector.typing.StudyUnit.UNIT_LOGNORM.value\n
            bioturing_connector.typing.StudyUnit.UNIT_RAW.value\n

    Returns
    ----------
    expression_matrix : csc_matrix
          Expression matrix, shape=(n_cells, n_genes)
    """
    data = {
      'species': species,
      'study_id': study_id,
      'gene_names': gene_names,
      'unit': unit
    }
    result = self.post_request(
      api_route='api/v1/study/query_genes',
      data=data
    )
    return common.parse_query_genes_result(result)


  def get_metadata_fields(
    self,
    species: str,
    study_id: str,
    group_id: str = None,
  ):
    """
    Get full metadata fields of a study.

    Parameters
    ----------
      species : bioturing_connector.typing.Species,
            Species of the study.\n
            Support:
              bioturing_connector.typing.Species.HUMAN.value\n
              bioturing_connector.typing.Species.MOUSE.value\n
              bioturing_connector.typing.Species.PRIMATE.value\n
              bioturing_connector.typing.Species.OTHERS.value\n
      study_id : str,
            uuidv4 of study
      group_id : str, optional. Default=None
            If you want to get metadata from a study in group "bioturing_public_studies",\n
            set group_id = 'bioturing_public_studies',\n
            otherwise, leave it as default.

    Returns
    ----------
      Metadata : pd.DataFrame
    """
    data = {
      'species': species,
      'study_id': study_id,
      'group_id': group_id,
    }
    result = self.post_request(
      api_route='api/v1/study/get_metadata_fields',
      data=data
    )
    common.check_result_status(result)
    fields = result['data']
    return fields


  def get_metadata(
    self,
    species: str,
    study_id: str,
    group_id: str = None,
    fields: List[str] = []
  ):
    """
    Get full metadata of a study.

    Parameters
    ----------
      species : bioturing_connector.typing.Species,
            Species of the study.\n
            Support:
              bioturing_connector.typing.Species.HUMAN.value\n
              bioturing_connector.typing.Species.MOUSE.value\n
              bioturing_connector.typing.Species.PRIMATE.value\n
              bioturing_connector.typing.Species.OTHERS.value\n
      study_id : str,
            uuidv4 of study
      group_id : str, optional. Default=None
            If you want to get metadata from a study in group "bioturing_public_studies",\n
            set group_id = 'bioturing_public_studies',\n
            otherwise, leave it as default.
      fields : List[str], optional. Default=[]

    Returns
    ----------
      Metadata : pd.DataFrame
    """
    data = {
      'species': species,
      'study_id': study_id,
      'group_id': group_id,
      'fields': fields,
    }
    result = self.post_request(
      api_route='api/v1/study/get_metadata',
      data=data
    )
    common.check_result_status(result)
    metadata_dict = result['data']
    metadata_df = pd.DataFrame(metadata_dict)
    return metadata_df


  def get_barcodes(
    self,
    species: str,
    study_id: str
  ):
    """
    Get barcodes of a study.

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,\n
          uuidv4 of study

    Returns
    ----------
    barcodes : List[]
    """
    data = {
      'species': species,
      'study_id': study_id
    }
    result = self.post_request(
      api_route='api/v1/study/get_barcodes',
      data=data
    )
    common.check_result_status(result)
    return result['data']


  def get_features(
    self,
    species: str,
    study_id: str
  ):
    """
    Get features of a study.

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study

    Returns
    ----------
    Features : List[]
    """
    data = {
      'species': species,
      'study_id': study_id
    }
    result = self.post_request(
      api_route='api/v1/study/get_features',
      data=data
    )
    common.check_result_status(result)
    return result['data']


  def list_all_custom_embeddings(
    self,
    species: str,
    study_id: str
  ):
    """
    List all custom embeddings of a study

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study

    Returns
    ----------
    List of embeddings' info : List[dict]
      In which:
        'embedding_id': the uuid used in further steps\n
        'embedding_name': displaying name on platform\n
    """
    data = {
      'species': species,
      'study_id': study_id
    }
    result = self.post_request(
      api_route='api/v1/list_all_custom_embeddings',
      data=data
    )
    common.check_result_status(result)
    return result['data']


  def retrieve_custom_embedding(
    self,
    species: str,
    study_id: str,
    embedding_id: str
  ):
    """
    Retrieve an embedding array of a study

    Parameters
    -------------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study
    embedding_id : str,
          Embedding id (uuid)

    Returns
    -------------
    embedding_arr : np.ndarray with shape (n_cells x n_dims)
    """
    data = {
      'species': species,
      'study_id': study_id,
      'embedding_id': embedding_id
    }
    result = self.post_request(
      api_route='api/v1/retrieve_custom_embedding',
      data=data
    )
    common.check_result_status(result)
    coord_arr = result['data']['coord_arr']
    coord_shape = result['data']['coord_shape']
    return decode_base64_array(coord_arr, 'float32', coord_shape)


  def submit_metadata_from_dataframe(
    self,
    species: str,
    study_id: str,
    group_id: str,
    df: pd.DataFrame
  ):
    """
    Submit metadata dataframe directly to a study

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study
    group_id : str,
          ID of the group containing study id
    df : pandas DataFrame,
          Barcodes must be in df.index!!!!

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    metadata_dct = common.dataframe2dictionary(df)
    data = {
      'species': species,
      'study_id': study_id,
      'group_id': group_id,
      'metadata_dct': metadata_dct
    }
    result = self.post_request(
      api_route='api/v1/submit_metadata_dataframe',
      data=data
    )
    common.check_result_status(result)
    print('Successful')
    return True


  def submit_metadata_from_local(
    self,
    species: str,
    study_id: str,
    group_id: str,
    file_path: str
  ):
    """
    Submit metadata to a study with local path

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study
    group_id : str,
          ID of the group containing study id
    file_path : local path leading to metadata file,
          Barcodes must be in the first column\n
          File suffix must be in .tsv/.csv

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    df = common.read_csv(file_path, index_col=0)
    return self.submit_metadata_from_dataframe(
      species,
      study_id,
      group_id,
      df
    )


  def submit_metadata_from_s3(
    self,
    species: str,
    study_id: str,
    group_id: str,
    file_path: str,
    s3_id: str = None,
  ):
    """
    Submit metadata to a study with s3 path

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study
    group_id : str,
          ID of the group containing study id
    file_path : str,
          Path in s3 bucket leading to metadata file,\n
          Notes:
            Barcodes must be in the fist column\n
            File suffix must be in .tsv/.csv\n
            File_path DOES NOT contain s3_bucket path configured on the platform
              E.g:
                realpath: 's3://bucket/folder/metadata.tsv'\n
                inputpath: 'folder/metadata.tsv'
    s3_id : str, Optional
          ID of s3 bucket. Default: None\n
          If s3_id is not provided, we will use the first s3 bucket configured on the platform.

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    data = {
      'species': species,
      'study_id': study_id,
      'group_id': group_id,
      'file_path': file_path,
      's3_id': s3_id,
    }
    result = self.post_request(
      api_route='api/v1/submit_metadata_s3',
      data=data
    )
    common.check_result_status(result)
    print('Successful')
    return True


  def submit_metadata_from_shared_s3(
    self,
    species: str,
    study_id: str,
    group_id: str,
    file_path: str,
    shared_s3_id: str = None,
  ):
    """
    Submit metadata to a study with s3 path

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study
    group_id : str,
          ID of the group containing study id
    file_path : str,
          Path in s3 bucket leading to metadata file,\n
          Notes:
            Barcodes must be in the fist column\n
            File suffix must be in .tsv/.csv\n
            File_path DOES NOT contain s3_bucket path configured on the platform
              E.g:
                realpath: 's3://bucket/prefix/metadata.tsv'\n
                inputpath: 'prefix/metadata.tsv'
    shared_s3_id : str
          ID of shared s3 bucket

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    data = {
      'species': species,
      'study_id': study_id,
      'group_id': group_id,
      'file_path': file_path,
      'shared_s3_id': shared_s3_id,
    }
    result = self.post_request(
      api_route='api/v1/submit_metadata_from_shared_s3',
      data=data
    )
    common.check_result_status(result)
    print('Successful')
    return True


  def get_ontologies_tree(
    self,
    species,
    group_id,
  ):
    """
    Get standardized ontologies tree

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value
    group_id : str
          ID of the group.

    Returns
    ----------
    Ontologies tree : Dict[Dict]
      In which:
        'name': name of the node, which will be used in further steps\n
    """
    data = {
      'species': species,
      'group_id': group_id
    }
    result = self.post_request(
      api_route='api/v1/get_ontologies',
      data=data
    )
    common.check_result_status(result)
    return result['data']


  def assign_standardized_meta(
    self,
    species,
    group_id,
    study_id,
    metadata_field,
    metadata_value,
    root_name,
    leaf_name,
  ):
    """
    Assign metadata value to a standardized term on ontologies tree

    Parameters
    ----------
    species : bioturing_connector.typing.Species
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    group_id  : str
          ID of the group to submit the data to.
    study_id  : str
          ID of the study (uuid)
    metadata_field  : str
          ~ column name of meta dataframe in platform (eg: author's tissue)
    metadata_value  : str
          ~ metadata value within the metadata field (eg: normal lung)
    root_name : str
          name of root in btr ontologies tree (eg: tissue)
    leaf_name : str
          name of leaf in btr ontologies tree (eg: lung)

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    ontologies_tree = self.get_ontologies_tree(species, group_id)
    root_id, leaf_id = common.parse_root_leaf_name(
      ontologies_tree,
      root_name,
      leaf_name
    )
    data = {
      'species': species,
      'group_id': group_id,
      'study_id': study_id,
      'group': metadata_field,
      'name': metadata_value,
      'root_id': root_id,
      'leaf_id': leaf_id,
    }
    result = self.post_request(
      api_route='api/v1/study/assign_standardized_term',
      data=data
    )
    common.check_result_status(result)
    return 'Successul'