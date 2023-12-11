import json
import logging

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)
logging.getLogger(__name__).setLevel(logging.DEBUG)

ENV_FILE = './config.json'


def get_env_vars() -> dict:
    LOGGER.info('Fetching environment variables from config.json')
    with open(ENV_FILE) as file:
        data = json.load(file)
    return data


def get_total_s3_objects(s3_bucket) -> int:
    count = 0
    for i in s3_bucket.objects.all():
        count += 1
    LOGGER.info(f'Total: {count} objects in {s3_bucket}')
    return count


def delete_s3_objects(s3_bucket, extension=None) -> None:
    LOGGER.info(f'Clearing s3 bucket {s3_bucket.name}...')
    count = 0
    files = []
    for obj in s3_bucket.objects.all():
        if extension and not obj.key.endswith(extension):
            continue
        files.append(obj.key)
        obj.delete()
        count += 1
    LOGGER.info(f'Deleted {count} objects from {s3_bucket.name}: {files}')