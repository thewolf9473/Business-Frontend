import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = "AKIA4QB2WTN5WMNEVGW5"
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

# bucket_name = "deepcon"
# s3_file_name = "audio_file.txt"

# uploaded = upload_to_aws('sample.txt', bucket_name, s3_file_name)