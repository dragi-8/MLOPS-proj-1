import boto3
import os
from src.constants import AWS_SECRET_ACCESS_KEY_ENV_KEY, AWS_ACCESS_KEY_ID_ENV_KEY, REGION_NAME

class S3Client:
    s3_client=None
    s3_resource=None

    def __init__(self,region_name=REGION_NAME):

        if self.s3_client==None or self.s3_resource==None:
            __acces_key=os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
            __aws_secret_key=os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY)
            if __acces_key is None:
                raise Exception(f"Environment variable {AWS_ACCESS_KEY_ID_ENV_KEY} not found.")
            if __aws_secret_key is None:
                raise Exception(f"Environment variable {AWS_SECRET_ACCESS_KEY_ENV_KEY} not found.")
            S3Client.s3_client=boto3.client('s3',aws_access_key_id=__acces_key,aws_secret_access_key=__aws_secret_key,region_name=region_name)
            S3Client.s3_resource=boto3.resource('s3',aws_access_key_id=__acces_key,aws_secret_access_key=__aws_secret_key,region_name=region_name)

        self.s3_client=S3Client.s3_client
        self.s3_resource=S3Client.s3_resource    
    