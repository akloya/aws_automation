# Author : Ajaya Kumar Loya
# Automated AMI Created based on tag: Backup -> yes
import boto3
import time
from typing import List

my_date = time.strftime("%Y%m%d")

def fetch_tag_value(tag_name: str, tags: List[dict]) -> bool:
    print('tag_name', tag_name)
    for tag in tags:
        if tag.get('Key') == tag_name:
            return tag.get('Value')


ec2_client = boto3.client('ec2')

response = ec2_client.describe_instances(
    Filters=[
        {
            'Name': 'tag:Backup',
            'Values': [
                'yes'
            ]
        }
    ]
)

for reservation in (response["Reservations"]):
        for instance in reservation["Instances"]:
            response = ec2_client.describe_tags(
                  Filters=[
                          {
                              'Name': 'resource-id',
                              'Values': [
                                  instance["InstanceId"]
                              ]
                          }
                      ]
                  )
            instance_name = fetch_tag_value('Name', response['Tags'])
            print('Tag', instance_name)
            ami_name = instance_name + " Automated " + instance["InstanceId"] + " on " + my_date
            print("Creating image with name", ami_name)
            create_ami = ec2_client.create_image(
                InstanceId=instance["InstanceId"],
                Name=ami_name,
                Description="automated script"
            )
            print(create_ami)
            create_tag = ec2_client.create_tags(
                Resources=[
                    create_ami['ImageId']
                ],
                Tags=[
                    {
                        'Key': 'Name',
                        'Value':  instance_name
                    }
                ]
            )
