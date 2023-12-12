import sys
from urllib.parse import urlsplit
import boto3
import datetime
from botocore.client import Config
import logging
import botocore.vendored.requests.exceptions as botoRequestsExceptions
import botocore.exceptions as botoExceptions

_logger = logging.getLogger('storage_stats')

class S3StorageShare:
    def __init__(self, storage_share):

        self.plugin_settings = storage_share['plugin_settings']

        self.plugin_settings.update(
            {
                'url': storage_share['url']
            }
        )

        _url = urlsplit(storage_share['url'])
        self.uri = {
            'netloc':   _url.netloc,
            'path':     _url.path,
            'scheme':   _url.scheme,
        }

        self.validators = {
            'conn_timeout': {
                'default': 10,
                'required': False,
                'status_code': '005',
                'type': 'int',
            },
            'ssl_check': {
                'boolean': True,
                'default': True,
                'required': False,
                'status_code': '006',
                'valid': ['true', 'false', 'yes', 'no']
            },
            's3.priv_key': {
                'required': True,
                'status_code': '021',
            },
            's3.pub_key': {
                'required': True,
                'status_code': '022',
            },
            's3.region': {
                'default': 'us-east-1',
                'required': False,
                'status_code': '023',
            },
            's3.signature_ver': {
                'default': 's3v4',
                'required': False,
                'status_code': '024',
                'valid': ['s3', 's3v4'],
            },
        }

        self.validate_plugin_settings()

        self.uri['bucket'] = self.uri['path'].rpartition('/')[-1]


    def validate_plugin_settings(self):
        """ 
        checks for required plugin settings
        """
        
        _logger.info("Validating configured setitngs.")
        
        for _setting in self.validators:
            _logger.debug(f"Validating setting {_setting}")
            
            try:
                self.plugin_settings[_setting]

            except KeyError:
                if self.validators[_setting]['required']:
                    _logger.error(f"Missing required setting: {_setting}")
                    
                else:
                    _logger.warn(f"Missing setting: {_setting}, using default value: {self.validators[_setting]['default']}")
                    self.plugin_settings.update({_setting: self.validators[_setting]['default']})
            
            else:
                try:
                    if self.plugin_settings[_setting].lower() not in self.validators[_setting]['valid']:
                        _logger.error(f"Invalid setting {self.plugin_settings[_setting]} for {_setting}. \
                            Valid settings: {self.validators[_setting]['valid']}")
                        exit(self.validators[_setting]['status_code'])
                    
                    else:
                        try:
                            self.validators[_setting]['boolean']
                        except KeyError:
                            pass
                        else:
                            self.plugin_settings[_setting] = self.plugin_settings[_setting].lower() == 'true' \
                                or self.plugin_settings[_setting].lower() == 'yes'
                                
                except KeyError:
                    pass
    

    def get_object_checksum(self, hash_type, object_url):
        """
        return the metadata of the specified hash type.
        returns None if the metadata does not exist
        """
        _metadata = self.get_object_metadata(object_url)
        
        try:
            _logger.info(f"Checking if metadata contains checksum of hash type {hash_type}")
            _logger.debug(f"Metadata being checked: {_metadata}")
            return _metadata[hash_type]
        
        except KeyError:
            _logger.warning(f"No checksum found for hash type {hash_type}")
            return None


    def get_object_metadata(self, object_url):
        """
        get and return the metadata from the file
        in s3 storage
        """
        _connection = self.get_s3_boto_client()
        _kwargs = {
            'Bucket': self.uri['bucket'],
            'Key': object_url,
        }
        
        _result = run_boto_client(_connection, 'head_object', _kwargs)
        
        try:
            _metadata = {k.lower(): v for k, v in _result['Metadata'].items()}
            return _metadata

        except KeyError:
            _logger.warning("No key Metadata in _result")
            return {}


    def put_object_checksum(self, checksum, hash_type, object_url, force):
        """
        check if there is existing metadata in the s3 file metadata
        if metadata exists, exit unless force is true
        """
        _metadata = self.get_object_metadata(object_url)

        if hash_type not in _metadata:
            # no metadata exists of this hash type, add metadata
            _metadata.setdefault(hash_type, checksum)
            _logger.info(f"New metadata detected, calling API to upload: {_metadata}")
            
            self.put_object_metadata(_metadata, object_url)

        elif force:
            # metadata already exists, replace metadata
            _metadata[hash_type] = checksum
            _logger.info(f"Force flag detected, calling API to update: {_metadata}")
            
            self.put_object_metadata(_metadata, object_url)

        else:
            # metadata already exists
            _logger.info("No new metadata detected, no need to call API. To update the existing data, use --force")
            _logger.debug(f"Metadata: {_metadata}")
            exit(0)


    def put_object_metadata(self, metadata, object_url):
        """
        put the new data in the metadata of the
        specified file in s3 storage
        """
        _connection = self.get_s3_boto_client()

        _kwargs = {
            'Bucket': self.uri['bucket'],
            'CopySource': {
                'Bucket': self.uri['bucket'],
                'Key': object_url,
            },
            'Key': object_url,
            'Metadata': metadata,
            'MetadataDirective': 'REPLACE',
        }

        try:
            # ensure there is new metadata to enter
            assert len(metadata) != 0
            
            _logger.info(f"Updating metdata of object '{object_url}'")
            _logger.debug(f"Metadata being uploaded: '{metadata}'")
            
            run_boto_client(_connection, 'copy_object', _kwargs)
        
        except AssertionError as INFO:
            _logger.info(f"Empty metadata. Skipping API request. {INFO}")
            sys.exit(1)


    def get_s3_boto_client(self):
        """
        create and return a connection to s3 storage
        """
        _api_url = f"{self.uri['scheme']}://{self.uri['netloc']}"
        _session = boto3.session.Session()

        _connection = _session.client(
            "s3",
            region_name=self.plugin_settings['s3.region'],
            endpoint_url=_api_url,
            aws_access_key_id=self.plugin_settings['s3.pub_key'],
            aws_secret_access_key=self.plugin_settings['s3.priv_key'],
            use_ssl=True,
            verify=self.plugin_settings['ssl_check'],
            config = Config(
                signature_version=self.plugin_settings['s3.signature_ver'],
                connect_timeout=int(self.plugin_settings['conn_timeout']),
                retries=dict(max_attempts=0)
            )
        )
        
        return _connection


    def list_objects(self):
        """
        get the files in s3 storage, calculate, and 
        return the number of files and bytes used
        """
        _connection = self.get_s3_boto_client()
        
        _total_bytes = 0
        _total_files = 0
        
        _kwargs = {
            'Bucket': self.uri['bucket'],
            'Prefix': '',
            # 'Delimiter': '*',
        }
        
        while True:
            _response = run_boto_client(_connection, 'list_objects', _kwargs)
            
            # check for files in the response
            try:
                _response['Contents']
            except KeyError:
                break
            else:
                for _file in _response['Contents']:
                    _total_bytes += int(_file['Size'])
                    _total_files += 1
            
            # marker indicating the location of the last file read        
            try:
                _kwargs['Marker'] = _response['NextMarker']
            except KeyError:
                break
                
        return int(_total_bytes), _total_files


def run_boto_client(_connection, method, _kwargs):
    """
    runs the specified function with the 
    given arguments and returns the result
    """
    _function = getattr(_connection, method)
    _result = {}
    try:
        _result = _function(**_kwargs)
    
    except botoExceptions.ClientError as ERR:
        _logger.error(f"[{ERR.__class__.__name__}][{ERR.response['ResponseMetadata']['HTTPStatusCode']}] Failed to establish a connection")
        _logger.debug(f"{str(ERR)}")
        print("An error occurred (404). File not found")
        sys.exit(1)
    
    except botoRequestsExceptions.SSLError as ERR:
        _logger.error(f"[{ERR.__class__.__name__}][092] Failed to establish a connection")
        _logger.debug(f"{str(ERR)}")

    except botoRequestsExceptions.RequestException as ERR:
        _logger.error(f"[{ERR.__class__.__name__}][400] Failed to establish a connection")
        _logger.debug(f"{str(ERR)}")
    
    except botoExceptions.ParamValidationError as ERR:
        _logger.error(f"[{ERR.__class__.__name__}][095] Failed to establish a connection")
        _logger.debug(f"{str(ERR)}")
            
    except botoExceptions.BotoCoreError as ERR:
        _logger.error(f"[{ERR.__class__.__name__}][400] Failed to establish a connection")
        _logger.debug(f"{str(ERR)}")
            
    return _result
