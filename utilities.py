import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = "AKIA4QB2WTN52EI4GUHM"
SECRET_KEY = "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"


def upload_to_aws(local_file, file_name, bucket="deepcon"):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    file_name = f"{file_name}.mp3"
    print("-------------file name------------ ", file_name)
    try:
        s3.upload_file(local_file, bucket, file_name)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

