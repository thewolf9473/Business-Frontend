import boto3
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv
load_dotenv()


ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")


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

