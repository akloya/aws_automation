# Author : Ajaya Kumar Loya
# Description : This script takes backup of all recordsets for each hosted zone on your aws account.


import boto3
import json
import time

my_date = time.strftime("%Y%m%d")

r53_client = boto3.client('route53')
s3_client = boto3.client('s3')
r53_client.list_hosted_zones()
response = r53_client.list_hosted_zones_by_name(
    MaxItems='10'
)

for hosted_zone in response['HostedZones']:
    print("Generating JSON for Zone", hosted_zone['Id'])
    hosted_zone_name = hosted_zone['Name']
    file_name = hosted_zone_name + my_date
    print(file_name)
    response = r53_client.list_resource_record_sets(
        HostedZoneId=hosted_zone['Id']
    )
    with open(file_name, 'w') as fp:
        json.dump(response, fp, sort_keys=True, indent=4)


