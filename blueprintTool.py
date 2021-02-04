import os
import json
import re
import argparse

from colors import colorLookup

#Arguments
argParser = argparse.ArgumentParser()

argParser.add_argument("blueprint", help = "the name of the blueprint you are trying to edit")
argParser.add_argument("-c", "--connect", nargs = 2, metavar = ("SRC", "DST"), help = "connect logic gates of color SRC to logic gates of color DST (use this format: <baseColor>-<1-4> or hex directly for color)")
args = argParser.parse_args()

def parseColor(input):
	if(input in colorLookup):
		return colorLookup[input]
	return input

#Simple helper class to store paths
class paths:
   basePath = os.getenv("APPDATA") + "\\Axolot Games\\Scrap Mechanic\\User\\"
   
   userPath = basePath + re.search("User_[0-9]{17}", "".join(os.listdir(basePath))).group()
   blueprints = userPath + "\\Blueprints"

#Main
found = False
multipleFound = False
for BpDirItterator in os.listdir(paths.blueprints):
	try:
		with open("%s\\%s\\description.json" %(paths.blueprints, BpDirItterator), "r") as descriptionFile:
			name = json.load(descriptionFile)["name"]
			if(name == args.blueprint):
				multipleFound = found
				found = True
				bpDir = BpDirItterator
	except:
		pass

if(found):
	if(multipleFound):
		print("Multiple blueprints with the name \"%s\" have been found, please save the blueprint with a unique name." %(args.blueprint))
	else:
		destinations = []
		try:
			with open("%s\\%s\\blueprint.json" %(paths.blueprints, bpDir), "r+") as blueprintFile:
				blueprintJson = json.load(blueprintFile)
				if(args.connect):	#connect mode
					#loop over all parts to detect if they are a destination
					for body in blueprintJson["bodies"]:
						for child in body["childs"]:
							if(child["color"] == parseColor(args.connect[1]).lower()):	#if current part is destination color
								destinations.append({"id": child["controller"]["id"]})

					#loop over all parts again to write the destinations to the sources
					for body in blueprintJson["bodies"]:
						for child in body["childs"]:
							if(child["color"] == parseColor(args.connect[0]).lower()):	#if current part is source color
								for destination in destinations:
									if child["controller"]["controllers"] == None:	#check if the part already has connections and if not just write the whole array directly 
										child["controller"]["controllers"] = destinations
									else:	#if it already has connections check if the connections alreay exist and if not append them to the array
										if destination not in child["controller"]["controllers"]:
											child["controller"]["controllers"].append(destination)
				
				#overwrite file
				blueprintFile.seek(0)
				blueprintFile.write(json.dumps(blueprintJson))
				blueprintFile.truncate()

		except Exception as e:
			print("error while reading blueprint file")
			print(e)
else:
	print("No blueprint with the name of \"%s\" was found." %(args.blueprint))

