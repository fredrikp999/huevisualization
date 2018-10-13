import requests
import json
import time
import sys
import hueif
import tsdbif

# This is the new "main"

def main(argv):
	if (len(argv)>=1):
		if (argv[0] == "doitOnce"):
			print("Do it")
			Pusher = LightStatusPusher()
			Pusher.pushLightInfo(1)
			
		elif (argv[0] == "test1"):
			focusLight = 1
			tsdb = tsdbif.TSDBfixer()
			lights = hueif.HueLights()
			brightness = lights.getOneLightBrightness(focusLight)
			theBody = tsdb.createTSDBbody(time.time(),"DS.Kitchen.island.bri",brightness)
			tsdb.writeTSDB(theBody)
			print (theBody)

		elif (argv[0] == "test2"):
			focusSensor = 13
			tsdb = tsdbif.TSDBfixer()
			sensors = hueif.HueSensors()
			lightlevel = sensors.getLightlevel(focusSensor)
			theBody = tsdb.createTSDBbody(time.time(),"DS.Kitchen.light",lightlevel)
			tsdb.writeTSDB(theBody)
			print (theBody)
			
		elif (argv[0] == "doitLoop"):
				print("Do it a while")
				Pusher = tsdbif.LightStatusPusher()
				Pusher.loopedPush(1)

		elif (argv[0] == "SensorLoop"):
			print("Sample and store light sensor in kitchen for a while")
			sensorLoop()
                                
	
		else:
			print("Sorry, no such action")
			print("Use: doitOnce, test1, test2, doitLoop or SensorLoop")

	else:
		lights = hueif.HueLights()
		printer = tsdbif.LightStatusPrinter(lights)
		for i in range(1,7):
        		focusLightNo = i
        		print ("-------------------")
        		printer.printOneLight(focusLightNo)


def sensorLoop():
	focusSensor = 13
	sensors = hueif.HueSensors()
	tsdb = tsdbif.TSDBfixer()
	for i in range (1,100000):
		sensors.readAllSensors()
		lightlevel = sensors.getLightlevel(focusSensor)
		theBody = tsdb.createTSDBbody(time.time(),"DS.Kitchen.light",lightlevel)
		tsdb.writeTSDB(theBody)
		print (theBody)
		time.sleep(10)
		print("Sleeping 10s")

if __name__ == "__main__":
	main(sys.argv[1:])
