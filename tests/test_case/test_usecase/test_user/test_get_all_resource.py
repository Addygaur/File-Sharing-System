
from unittest import IsolatedAsyncioTestCase
import boto3
from fastapi import HTTPException
from config import AWS_SECRET_KEY, AWS_ACCESS_KEY, AWS_ENDPOINT, BUCKET_NAME
from resource.resource_store import ResourceStore


class TestGetAllResourceUsecase(IsolatedAsyncioTestCase):

    async def test_get_all_resource(self):
       client=boto3.client(
           's3',
           aws_access_key_id=AWS_ACCESS_KEY,
           aws_secret_access_key=AWS_SECRET_KEY,
           endpoint_url=AWS_ENDPOINT
       )
       repo = ResourceStore(client, BUCKET_NAME)
       try:
           data = await repo.get_all_files()
           self.assertIsInstance(data,list)
           return data

       except:
           self.assertRaises(HTTPException,
                             HTTPException(status_code=400,detail="File Not Fetched")
                             )

