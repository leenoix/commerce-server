from storages.backends.s3boto3 import S3Boto3Storage
  
from project import settings


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False
