#TSDB interface and functions
import requests
import json
import time
import sys

class LightStatusPrinter():
	def __init__(self,lightsObj):
        # Constructor. Get status for all lights and store in self.lightData for further use
		print("Constructing a LightStatusPrinter")
		# How to get "lights" to be usable in the methods below?
		self.lights = lightsObj #was: = HueLights()
		
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
	def __init__(self,lightsObj):
		self.lights = lightsObj
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
		#self.lights = lightsObj
		self.tsdbUrl = 'http://127.0.0.1:4242/api/put'	
            
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