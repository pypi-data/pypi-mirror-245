import json
import logging
import traceback

import boto3

class S3Environment:
    def __init__(self, bucket, key, access_key=None, secret_key=None, region=None, log=logging):
        self._bucket = bucket
        self._key = key
        self._access_key = access_key
        self._secret_key = secret_key
        self._region = region
        self._log = log
        self._s3_client = self._get_s3_client()

    def get_backend_data(self, origin):
        try:
            obj = self._s3_client.get_object(
                Bucket=self._bucket,
                Key=self._key
            )
            obj_data = obj['Body'].read().decode("utf-8")
            obj_data = json.loads(obj_data)
            data = obj_data[origin]

        except Exception:
            print("ERROR", traceback.format_exc())
            data = None
        return data

    def _get_s3_client(self):
        if self._region and self._access_key and self._secret_key:
            s3_client = boto3.client(
                service_name='s3',
                region_name=self._region,
                aws_access_key_id=self._access_key,
                aws_secret_access_key=self._secret_key)
        else:
            s3_client = boto3.client(
                service_name='s3'
            )
        return s3_client
