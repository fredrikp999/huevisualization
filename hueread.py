import requests
import json
import time
import sys

# Playing around with Philips Hur Lights
# And sinking some data to OpenTSDB for visualization in Grafana etc.

class HueLights:
	def __init__(self):
	# Constructor. Get status for all lights and store in self.lightData for further use
	# Also define some variable
		print("Constructing a HueLights object")
		self.url = 'http://192.168.0.82/api/HfXRDdNGFsrp29yO7BHWEHPAvsG8xpjYGbxucuXh/lights'
		self.readAllLights()

	def readAllLights(self):
	# Read in all available data on all lights from Philipe Hue Hub
	# Store in variable using setAllLightsData-method
		print ("Getting info on all lights")
		getdata = {}
		response = requests.get(self.url, data=json.dumps(getdata))
		toreturn = json.loads(response.text)
		self.setAllLightsData(toreturn)
		return

	def getOneLightState(self,lightNo):
	# Return all State-data on one specified light (no of light as input-parameter)
		allLightInfo = self.lightData
		oneLightInfo = allLightInfo[str(lightNo)]
		oneLightState = oneLightInfo["state"]
		return oneLightState

	def getOneLightOnOff(self,lightNo):
	# Extract and return if the specified light is currently on (1) or off (0)
		stateData = self.getOneLightState(lightNo)
		onOff = stateData["on"]
		if onOff == "True":
			return 1
		else:
			return 0

	def getOneLightBrightness(self,lightNo):
        # Extract and return brightness of the specified light
                stateData = self.getOneLightState(lightNo)
                brightness = stateData["bri"]
                return brightness


	def getOneLightHue(self,lightNo):
        # Extract and return hue of the specified light 
                stateData = self.getOneLightState(lightNo)
                hue = stateData["hue"]
                return hue
		
	def getOneLightSaturation(self,lightNo):
        # Extract and return saturation of the specified light       
                stateData = self.getOneLightState(lightNo)
                saturation = stateData["sat"]
                return saturation

	def getOneLightName(self,lightNo):
		allLightInfo = self.lightData
		oneLightInfo = allLightInfo[str(lightNo)]
		lightName = oneLightInfo["name"]
		return lightName

	def setAllLightsData(self,lightData):
		self.lightData = lightData
		return

class HueSensors:
	def __init__(self):
	# Constructor. Get status for all lights and store in self.lightData for further use
	# Also define some variable
		print("Constructing a HueLights object")
		self.url = 'http://192.168.0.82/api/HfXRDdNGFsrp29yO7BHWEHPAvsG8xpjYGbxucuXh/sensors'
		self.readAllSensors()

	def readAllSensors(self):
	# Read in all available data on all lights from Philipe Hue Hub
	# Store in variable using setAllLightsData-method
		print ("Getting info on all lights")
		getdata = {}
		response = requests.get(self.url, data=json.dumps(getdata))
		sensordata = json.loads(response.text)
		self.setAllSensorsData(sensordata)
		return

	def setAllSensorsData(self,sensorsData):
		self.sensorsData = sensorsData
		return

	def getOneSensorData(self,sensorNo):
		allSensorData = self.sensorsData
		oneSensorData = allSensorData[str(sensorNo)]
		return (oneSensorData)

	def getLightlevel(self,sensorNo):
		oneSensorData = self.getOneSensorData(sensorNo)
		stateInfo = oneSensorData["state"]
		lightlevel = stateInfo["lightlevel"]
		return (lightlevel)


class LightStatusPrinter:
	def __init__(self):
        # Constructor. Get status for all lights and store in self.lightData for further use
		print("Constructing a LightStatusPrinter")
		# How to get "lights" to be usable in the methods below?
		self.lights = HueLights()
		
	def printOneLight(self,lightNo):
		#lights = HueLights()
		focusLightNo = lightNo
		oneLightState = self.lights.getOneLightOnOff(focusLightNo)
		oneLightBrightness = self.lights.getOneLightBrightness(focusLightNo)
		oneLightHue = self.lights.getOneLightHue(focusLightNo)
		oneLightSaturation = self.lights.getOneLightSaturation(focusLightNo)
		print ("Light: ",self.lights.getOneLightName(focusLightNo),",",str(focusLightNo))
		print ("Is it on? ",oneLightState)
		print ("Brightness: ",oneLightBrightness)
		print ("Hue: ",oneLightHue)
		print ("Saturation: ",oneLightSaturation)
		return

	def refresh(self):
		self.lights.readAllLights()
		return

class LightStatusPusher:
	def __init__(self):
		self.lights = HueLights()
		self.tsdbUrl = 'http://localhost:4242/api/put'	

	def pushLightInfo(self,lightNo):
		self.lights.readAllLights()
		putdata = {
			"metric":"Downstairs.Kitchen.1.bri",
			"timestamp":time.time(),
			"value": self.lights.getOneLightBrightness(1),
			"tags": {
				"hst":"web01",
				"dc":"lgs"
				}
			}

		response = requests.post('http://127.0.0.1:4242/api/put',data=json.dumps(putdata))
		print(response)
		print(response.text)
		print(self.lights.getOneLightBrightness(1))


	def loopedPush(self,lightNo):
		for i in range(1,50):
			self.pushLightInfo(1)
			#Sleep 20 seconds
			time.sleep(20)
		return
    
    
class TSDBfixer:
	def __init__(self):
		self.lights = HueLights()
		self.tsdbUrl = 'http://localhost:4242/api/put'	
            
	def createTSDBbody(self,theTime,theMetric,theValue):
		putdata = {
			"metric":theMetric,
			"timestamp":theTime,
			"value": theValue,
			"tags": {
				"hst":"web01",
				"dc":"lgs"
				}
			}
		return putdata
	
	def writeTSDB (self,putdata):
		response = requests.post(self.tsdbUrl,data=json.dumps(putdata))
		print (response)
		print (response.text)
		return
        


def main(argv):
	if (len(argv)>=1):
		if (argv[0] == "doitOnce"):
			print("Do it")
			Pusher = LightStatusPusher()
			Pusher.pushLightInfo(1)
			
		elif (argv[0] == "test1"):
			focusLight = 1
			tsdb = TSDBfixer()
			lights = HueLights()
			brightness = lights.getOneLightBrightness(focusLight)
			theBody = tsdb.createTSDBbody(time.time(),"DS.Kitchen.island.bri",brightness)
			tsdb.writeTSDB(theBody)
			print (theBody)

		elif (argv[0] == "test2"):
			focusSensor = 13
			tsdb = TSDBfixer()
			sensors = HueSensors()
			lightlevel = sensors.getLightlevel(focusSensor)
			theBody = tsdb.createTSDBbody(time.time(),"DS.Kitchen.light",lightlevel)
			tsdb.writeTSDB(theBody)
			print (theBody)
			
		elif (argv[0] == "doitLoop"):
				print("Do it a while")
				Pusher = LightStatusPusher()
				Pusher.loopedPush(1)

		elif (argv[0] == "SensorLoop"):
			print("Sample and store light sensor in kitchen for a while")
			focusSensor = 13
			sensors = HueSensors()
			tsdb = TSDBfixer()
			for i in range (1,100000):
				sensors.readAllSensors()
				lightlevel = sensors.getLightlevel(focusSensor)
				theBody = tsdb.createTSDBbody(time.time(),"DS.Kitchen.light",lightlevel)
				tsdb.writeTSDB(theBody)
				print (theBody)
				time.sleep(10)
				print("Sleeping 10s")
                                
	
		else:
			print("Sorry, no such action")

	else:
		printer = LightStatusPrinter()
		for i in range(1,7):
        		focusLightNo = i
        		print ("-------------------")
        		printer.printOneLight(focusLightNo)

if __name__ == "__main__":
	main(sys.argv[1:])
