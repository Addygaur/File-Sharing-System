from fastapi import HTTPException
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_ENDPOINT, BUCKET_NAME
import boto3
from resource.resource_store import ResourceStore


async def get_all_resource_usecase():

       client=boto3.client(
           's3',
           aws_access_key_id=AWS_ACCESS_KEY,
           aws_secret_access_key=AWS_SECRET_KEY,
           endpoint_url=AWS_ENDPOINT
       )
       repo = ResourceStore(client, BUCKET_NAME)
       try:
           data = await repo.get_all_files()
           return data

       except:
           raise HTTPException(status_code=400,detail="File Not Fetched")








