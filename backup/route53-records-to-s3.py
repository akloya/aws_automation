# Author : Ajaya Kumar Loya
# Description : This script takes backup of all recordsets for each hosted zone on your aws account and uploads to s3 bucket.


import boto3
import json
import time

# Variables
s3_bucket = "akloya-tests"

my_date = time.strftime("%Y%m%d")
r53_client = boto3.client('route53')
s3 = boto3.resource('s3')
r53_client.list_hosted_zones()
response = r53_client.list_hosted_zones_by_name(
    MaxItems='10'
)

for hosted_zone in response['HostedZones']:
    print("Fetching recordsets for hosted zone :", hosted_zone['Id'])
    hosted_zone_name = hosted_zone['Name']
    file_name = hosted_zone_name + my_date
    response = r53_client.list_resource_record_sets(
        HostedZoneId=hosted_zone['Id']
    )
    with open(file_name, 'w') as fp:
        json.dump(response, fp, sort_keys=True, indent=4)
    print("Uploading file[", file_name, "] to s3 bucket[", s3_bucket, "]")
    s3.meta.client.upload_file(file_name, s3_bucket, file_name)
