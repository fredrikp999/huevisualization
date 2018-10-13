def printHello():
	print("Hello!")


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