import os
import boto3
from boto3.session import Session


s3_url = os.environ['S3_URL']
s3_access_key = os.environ['S3_ACCESS_KEY']
s3_secret_key = os.environ['S3_SECRET_KEY']
s3_bucket = os.environ['S3_BUCKET']
s3_backups_to_keep = int(os.environ.get('S3_BACKUP_TO_KEEP', '3'))


def list_directories(bucket):
    backups = dict()
    for object in bucket.objects.all():
        directory = (os.path.dirname(object.key))
        last_modified = object.last_modified

        if (directory not in backups.keys()) or (backups.get(directory) < last_modified):
            backups[directory] = last_modified

    return sorted(backups, key=backups.get, reverse=True)


def delete_objects(bucket, directory):
    response = bucket.objects.filter(Prefix=directory).delete()
    print(response)


def main():
    session = Session(
        aws_access_key_id=s3_access_key,
        aws_secret_access_key=s3_secret_key
    )
    s3 = session.resource('s3', endpoint_url=s3_url)
    bucket = s3.Bucket(s3_bucket)

    directories = list_directories(bucket)

    to_delete = directories[s3_backups_to_keep:] # Drop the first X (ie most recent) items
    for directory in to_delete:
        delete_objects(bucket, directory)


if __name__ == "__main__":
    main()
