import time
from temp import *

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

#awshost you got from `aws iot describe-endpoint`
awshost = "a134g88szk3vbi.iot.us-east-1.amazonaws.com"

# Edit this to be your device name in the AWS IoT console
thing = "raspberry_pi"

awsport = 8883
caPath = "/home/pi/iot_keys/root-CA.crt"
certPath = "/home/pi/iot_keys/raspberry_pi.cert.pem"
keyPath = "/home/pi/iot_keys/raspberry_pi.private.key"

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

# Delete shadow JSON doc
myDeviceShadow.shadowDelete(customCallback, 5)

while True:
	# grab temperature
	temp = read_temp()
	json_temp = "{ \"state\" : { \"reported\": {\"temp\": \"%s\" } } }" % str(temp)
	print temp
	myDeviceShadow.shadowUpdate(json_temp, customCallback, 5)
	time.sleep(60)




