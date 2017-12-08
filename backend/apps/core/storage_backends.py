from django.conf import settings

from storages.backends.s3boto import S3BotoStorage


class MediaRootS3BotoStorage(S3BotoStorage):
    """
    S3 storage backend for media content.
    """
    location = settings.MEDIA_S3_PATH

    def __init__(self, *args, **kwargs):
        super(MediaRootS3BotoStorage, self).__init__(*args, **kwargs)


class StaticRootS3BotoStorage(S3BotoStorage):
    """
    S3 storage backend for static content that saves the files locally, too.
    """
    location = settings.STATIC_S3_PATH

    def __init__(self, *args, **kwargs):
        super(StaticRootS3BotoStorage, self).__init__(*args, **kwargs)
