import boto3

client = boto3.client('kms')
response = client.list_keys(
    Limit=100
)

print(response)

for key in response['Keys']:

    try:
        rotation_status = client.get_key_rotation_status(
            KeyId=key['KeyId']
        )


    except Exception as e:
        print(key['KeyId'])
        print(str(e))

    isEnabled = rotation_status['KeyRotationEnabled']

    if str(isEnabled) == str('False'):
        print("Lets Enable it for key : "+key['KeyId'])
        enable_rotation = client.enable_key_rotation(
            KeyId=key['KeyId']
        )
        print(enable_rotation)
