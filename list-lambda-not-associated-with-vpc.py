import boto3
from botocore.exceptions import ClientError

client = boto3.client('lambda')
response = client.list_functions()
for function in response['Functions']:
    try:
        response = client.get_function(
            FunctionName=function['FunctionName']
        )
        vpcid = response['Configuration']['VpcConfig']['VpcId']
    except KeyError:
        print("==>" + function['FunctionName'])
    except ClientError as e:
        print("[ERROR] Invoking Lambda Function" + e)
