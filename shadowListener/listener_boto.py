import json
import boto3

client = boto3.client('iot-data', region_name='us-east-1', aws_access_key_id='xx', aws_secret_access_key='xx')
r = client.get_thing_shadow(thingName='raspberry_pi')

streamingBody = r['payload']
jsonState = json.loads(streamingBody.read())

print jsonState
