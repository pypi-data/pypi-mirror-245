# functionality for defining and working with Vector Store objects
from typing import Optional
import requests
import json

import vectorshift
from vectorshift.consts import (
    API_VECTORSTORE_SYNC_ENDPOINT,
    API_VECTORSTORE_UPDATE_METADATA_ENDPOINT,
    API_VECTORSTORE_UPDATE_SELECTED_FILES_ENDPOINT,
    API_VECTORSTORE_FETCH_SHARED_ENDPOINT,
    API_VECTORSTORE_REMOVE_SHARE_ENDPOINT,
    API_VECTORSTORE_SHARE_ENDPOINT,
    VECTORSTORE_DEFAULT_CHUNK_SIZE,
    VECTORSTORE_DEFAULT_CHUNK_OVERLAP,
    API_VECTORSTORE_FETCH_ENDPOINT,
    API_VECTORSTORE_SAVE_ENDPOINT,
    API_VECTORSTORE_LOAD_ENDPOINT,
    API_VECTORSTORE_QUERY_ENDPOINT,
    API_VECTORSTORE_LIST_VECTORS_ENDPOINT,
    API_VECTORSTORE_DELETE_VECTORS_ENDPOINT,
)

class VectorStore:
    # initializes a new Vector Store
    def __init__(
        self,
        name: str,
        description: str = '',
        chunk_size: int = VECTORSTORE_DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = VECTORSTORE_DEFAULT_CHUNK_OVERLAP,
        is_hybrid: bool = False,
        id: str = None
    ):
        self.name = name
        self.description = description
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.is_hybrid = is_hybrid
        self.id = id

    # converts Vector Store object to JSON representation
    def to_json_rep(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'chunkSize': self.chunk_size,
            'chunkOverlap': self.chunk_overlap,
            'isHybrid': self.is_hybrid,
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_json_rep())
    
    @staticmethod
    def from_json_rep(json_data: dict[str, any]) -> 'VectorStore':
        return VectorStore(
            name=json_data.get('name'),
            description=json_data.get('description'),
            chunk_size=json_data.get('chunkSize', VECTORSTORE_DEFAULT_CHUNK_SIZE),
            chunk_overlap=json_data.get('chunkOverlap', VECTORSTORE_DEFAULT_CHUNK_OVERLAP),
            is_hybrid=json_data.get('isHybrid', False),
            id=json_data.get('id'),
        )
    
    @staticmethod
    def from_json(json_str: str) -> 'VectorStore':
        json_data = json.loads(json_str)
        return VectorStore.from_json_rep(json_data)

    def __repr__(self):
        # TODO: format this reprerentation to be more readable
        return f'VectorStore({", ".join(f"{k}={v}" for k, v in self.to_json_rep().items())})'

    # TODO: Add validation for vectorstore_id and pipeline_id (in pipeline.py)
    # to prevent 5XX errors
    @staticmethod
    def fetch(
        vectorstore_name: str = None,
        vectorstore_id: str = None,
        username: str = None,
        org_name: str = None,
        public_key: str = None,
        private_key: str = None
    ) -> 'VectorStore':
        if vectorstore_id is None and vectorstore_name is None:
            raise ValueError('Must specify either vectorstore_id or vectorstore_name.')
        if vectorstore_name is not None and username is None and org_name is not None:
            raise ValueError('Must specify username if org_name is specified.')

        response = requests.get(
            API_VECTORSTORE_FETCH_ENDPOINT,
            data={
                'vectorstore_id': vectorstore_id,
                'vectorstore_name': vectorstore_name,
                'username': username,
                'org_name': org_name,
            },
            headers={
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )
        if response.status_code != 200:
            raise Exception(f'Error fetching vectorstore object: {response.text}')
        response = response.json()

        return VectorStore.from_json_rep(response)

    def save(
        self,
        update_existing: bool = False,
        public_key: str = None,
        private_key: str = None,
    ) -> dict:
        if update_existing and not self.id:
            raise ValueError("Error updating: vectorstore object does not have an existing ID. It must be saved as a new vectorstore.")
        # if update_existing is false, save as a new vectorstore
        if not update_existing:
            self.id = None

        # API_VECTORSTORE_SAVE_ENDPOINT handles saving and updating vectorstore 
        # depending on whether or not the JSON has an id (logic in api repo)
        response = requests.post(
            API_VECTORSTORE_SAVE_ENDPOINT,
            data=({'vectorstore': self.to_json()}),
            headers={
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )

        if response.status_code != 200:
            raise Exception(f'Error saving vectorstore object: {response.text}')
        response = response.json()
        self.id = response.get('id')

        return response
    
    def update_metadata(
        self,
        list_of_document_ids: list[str],
        list_of_metadata: list[str],
        keep_prev: bool,
        public_key: str = None,
        private_key: str = None,
    ) -> None:
        if not self.id:
            raise ValueError("Error updating: vectorstore object does not have an existing ID. It must be saved first.")
        
        data = {
            'vectorstore_id': self.id,
            'list_of_document_ids': list_of_document_ids,
            'list_of_metadata': [json.dumps(metadata) for metadata in list_of_metadata],
            'keep_prev': keep_prev,            
        }

        response = requests.post(
            API_VECTORSTORE_UPDATE_METADATA_ENDPOINT,
            data=data,
            headers={
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )

        if response.status_code != 200:
            raise Exception(f'Error updating document(s) metadata: {response.text}')
        return


    def update_selected_files(
        self,
        integration_id: str,
        keep_prev: bool,
        selected_files: Optional[list[str]] = None,
        select_all_files_flag: Optional[bool] = True,
        public_key: str = None,
        private_key: str = None,
    ) -> None:
        if not self.id:
            raise ValueError("Error updating: vectorstore object does not have an existing ID. It must be saved first.")
        
        data = {
            'vectorstore_id': self.id,
            'integration_id': integration_id,
            'selected_files': selected_files,
            'keep_prev': keep_prev,
            'select_all_files_flag': select_all_files_flag,
        }

        response = requests.post(
            API_VECTORSTORE_UPDATE_SELECTED_FILES_ENDPOINT,
            data=data,
            headers={
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )

        if response.status_code != 200:
            raise Exception(f'Error updating files selected: {response.text}')
        return
    

    def sync(
        self,
        public_key: str = None,
        private_key: str = None,
    ) -> None:
        if not self.id:
            raise ValueError('Error loading vectors: vectorstore object does not have an existing ID. It must be saved as a new vectorstore.')
        
        response = requests.post(
            API_VECTORSTORE_SYNC_ENDPOINT,
            data={
                'vectorstore_id': self.id,
            },
            headers={
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )

        if response.status_code != 200:
            raise Exception(response.text)
        
        response = response.json()
        return

    def sync(
        self,
        public_key: str = None,
        private_key: str = None,
    ) -> None:
        if not self.id:
            raise ValueError('Error loading vectors: vectorstore object does not have an existing ID. It must be saved as a new vectorstore.')
        
        response = requests.post(
            API_VECTORSTORE_SYNC_ENDPOINT,
            data={
                'vectorstore_id': self.id,
            },
            headers={
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )

        if response.status_code != 200:
            raise Exception(response.text)
        
        response = response.json()
        return

    def load_vectors(
        self,
        value, # file or 1 integration_object
        value_type: str = 'File', # 'Integration'
        chunk_size: int = None,
        chunk_overlap: int = None,
        selected_files: list = None,
        select_all_files_flags: list = None,
        metadata: dict = None,
        metadata_by_document: dict = None,
        public_key: str = None,
        private_key: str = None,
    ) -> dict:
        if not self.id:
            raise ValueError('Error loading vectors: vectorstore object does not have an existing ID. It must be saved as a new vectorstore.')

        chunk_size = chunk_size or self.chunk_size
        chunk_overlap = chunk_overlap or self.chunk_overlap

        data = {
            'vectorstore_id': self.id,
            'type': value_type,
            'chunk_size': chunk_size,
            'chunk_overlap': chunk_overlap,
            'selected_files': json.dumps(selected_files),
            'select_all_files_flags': json.dumps(select_all_files_flags),
            'metadata': json.dumps(metadata),
            'metadata_by_document': json.dumps(metadata_by_document),
        }

        headers={
            'Public-Key': public_key or vectorshift.public_key,
            'Private-Key': private_key or vectorshift.private_key,
        }

        if value_type == 'File':
            if isinstance(value, str):
                with open(value, 'rb') as f:
                    files = {'value': f}
                    response = requests.post(
                        API_VECTORSTORE_LOAD_ENDPOINT,
                        data=data,
                        headers=headers,
                        files=files,
                    )
            else:
                files = {'value': value}
                response = requests.post(
                    API_VECTORSTORE_LOAD_ENDPOINT,
                    data=data,
                    headers=headers,
                    files=files,
                )
        elif value_type == 'Integration':
            data['value'] = value
            response = requests.post(
                    API_VECTORSTORE_LOAD_ENDPOINT,
                    data=data,
                    headers=headers,
                )
        else:
            data['value'] = value
            response = requests.post(
                API_VECTORSTORE_LOAD_ENDPOINT,
                data=data,
                headers=headers,
            )

        if response.status_code != 200:
            raise Exception(f'Error loading vectors: {response.text}')
        response = response.json()

        return response

    def query(
        self,
        query: str,
        max_docs: int = 5,
        filter: dict = None,
        rerank: bool = False,
        public_key: str = None,
        private_key: str = None,
    ) -> dict:
        filter = filter or {}
        response = requests.post(
            API_VECTORSTORE_QUERY_ENDPOINT,
            data={
                'vectorstore_id': self.id,
                'query': query,
                'max_docs': max_docs,
                'filter': filter,
                'rerank': rerank,
            },
            headers={
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )
        if response.status_code != 200:
            raise Exception(response.text)
        response = response.json()

        return response

    def list_vectors(self, max_vectors: int = None) -> dict:
        if not self.id:
            raise ValueError('Error listing vectors: vectorstore object does not have an existing ID. It must be saved as a new vectorstore.')
        response = requests.post(
            API_VECTORSTORE_LIST_VECTORS_ENDPOINT,
            data={
                'vectorstore_id': self.id,
                'max_vectors': max_vectors,
            },
            headers={
                'Public-Key': vectorshift.public_key,
                'Private-Key': vectorshift.private_key,
            }
        )
        if response.status_code != 200:
            raise Exception(f'Error listing vectors: {response.text}')
        response = response.json()

        return response

    def delete_vectors(self, vector_ids: list, filter: dict = None) -> dict:
        # TODO: Add the ability to delete multiple vectors at once or by filter
        if not self.id:
            raise ValueError('Error deleting vectors: vectorstore object does not have an existing ID. It must be saved as a new vectorstore.')
        
        if not isinstance(vector_ids, list):
            vector_ids = [vector_ids]
        if len(vector_ids) == 0:
            raise ValueError('Error deleting vectors: vector_ids must be a non-empty list of vector IDs.')
        elif len(vector_ids) > 1:
            raise NotImplementedError('Error deleting vectors: deleting multiple vectors at once is not yet supported.')
        response = requests.delete(
            API_VECTORSTORE_DELETE_VECTORS_ENDPOINT,
            data={
                'vectorstore_id': self.id,
                'vector_id': vector_ids[0],
            },
            headers={
                'Public-Key': vectorshift.public_key,
                'Private-Key': vectorshift.private_key,
            }
        )
        if response.status_code != 200:
            raise Exception(f'Error listing vectors: {response.text}')
        response = response.json()

        return response

    def share(self, shared_users:list[str]) -> dict:
        if not self.id:
            raise ValueError('Error listing vectors: vectorstore object does not have an existing ID. It must be saved in order to be shared.')
        
        shared_users_dicts = []
        for user in shared_users:
            shared_users_dicts.append({
                    'email': user,
                    'permissions': 'View',
            })
        response = requests.post(
            API_VECTORSTORE_SHARE_ENDPOINT,
            data={
                'vectorstore_id': self.id,
                'shared_users': json.dumps(shared_users_dicts),
            },
            headers={
                'Public-Key': vectorshift.public_key,
                'Private-Key': vectorshift.private_key,
            }
        )
        if response.status_code != 200:
            raise Exception(f'Error sharing vectorstore: {response.text}')
        response = response.json()

        return response
    
    def fetch_shared(self) -> dict:
        if not self.id:
            raise ValueError('Error listing vectors: vectorstore object does not have an existing ID. It must be saved.')
        
        response = requests.get(
            API_VECTORSTORE_FETCH_SHARED_ENDPOINT,
            headers={
                'Public-Key': vectorshift.public_key,
                'Private-Key': vectorshift.private_key,
            }
        )
        if response.status_code != 200:
            raise Exception(f'Error fetching shared vectorstores: {response.text}')
        response = response.json()

        return response
    
    def remove_share(self, users_to_remove:list[str]) -> dict:
        if not self.id:
            raise ValueError('Error listing vectors: vectorstore object does not have an existing ID. It must be saved in order to be shared.')
        
        response = requests.delete(
            API_VECTORSTORE_REMOVE_SHARE_ENDPOINT,
            data={
                'vectorstore_id': self.id,
                'users_to_remove': users_to_remove,
            },
            headers={
                'Public-Key': vectorshift.public_key,
                'Private-Key': vectorshift.private_key,
            }
        )
        if response.status_code != 200:
            raise Exception(f'Error removing shared vectorstore: {response.text}')
        response = response.json()

        return response
