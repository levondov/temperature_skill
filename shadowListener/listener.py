import time
import json

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

#awshost you got from `aws iot describe-endpoint`
awshost = "a134g88szk3vbi.iot.us-east-1.amazonaws.com"

# Edit this to be your device name in the AWS IoT console
thing = "raspberry_pi2"

awsport = 8883
caPath = "/home/levon/iot_keys/root-CA.crt"
certPath = "/home/levon/iot_keys/raspberry_pi.cert.pem"
keyPath = "/home/levon/iot_keys/raspberry_pi.private.key"

def parse_payload(payload, responseStatus, token):
    parsed_json = json.loads(payload)
    temp_num = parsed_json['state']['reported']['temp']
    temp_time_epoch = parsed_json['metadata']['reported']['temp']['timestamp']
    print temp_num,temp_time_epoch

# Set up the shadow client
myShadowClient = AWSIoTMQTTShadowClient(thing)
myShadowClient.configureEndpoint(awshost, awsport)
myShadowClient.configureCredentials(caPath, keyPath, certPath)
myShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()
myDeviceShadow = myShadowClient.createShadowHandlerWithName("raspberry_pi", True)
# You can implement a custom callback function if you like, but once working I didn't require one. We still need to define it though.
customCallback = "" 


while True:
    myDeviceShadow.shadowGet(parse_payload,5)
    time.sleep(60)






