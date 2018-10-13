import requests
import json
import time
import sys

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