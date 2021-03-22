import os
import json
import re
import argparse
import textwrap

from lookups import *

#Arguments
argParser = argparse.ArgumentParser(
	formatter_class=argparse.RawDescriptionHelpFormatter,
	epilog = textwrap.dedent("""\
		additional information:
			for colors you can use the format (<baseColor>-<1-4>) or hex directly
		""")
)

inputGroup = argParser.add_mutually_exclusive_group(required=True)
inputGroup.add_argument("-b", "--blueprint", help = "the name of the blueprint you want to edit")
inputGroup.add_argument("-i", "--input", help = "the path of the script you want to use")

optionGroup = argParser.add_mutually_exclusive_group(required=True)
optionGroup.add_argument("-c", "--connect", nargs = 2, metavar = ("SRC", "DST"), help = "connect logic gates of color <SRC> to logic gates of color <DST>")
optionGroup.add_argument("-p", "--paint", nargs = 2, metavar = ("BLOCK", "COLOR"), help = "paint all block of type <BLOCK> the color <COLOR>")

args = argParser.parse_args()

#Simple helper class to store paths
class paths:
   basePath = os.getenv("APPDATA") + "\\Axolot Games\\Scrap Mechanic\\User\\"
   
   userPath = basePath + re.search("User_[0-9]{17}", "".join(os.listdir(basePath))).group()
   blueprints = userPath + "\\Blueprints"

def error(msg):
	print(msg)
	exit()

def parseColor(input):
	if(input.lower() in colorLookup):
		return colorLookup[input.lower()].lower()
	return input.lower()

def connect(src, dst, JSON):
	destinations = []
	#loop over all parts to detect if they are a destination
	for body in JSON["bodies"]:
		for child in body["childs"]:
			if(child["color"] == parseColor(dst)):	#if current part is destination color
				destinations.append({"id": child["controller"]["id"]})

	#loop over all parts again to write the destinations to the sources
	for body in JSON["bodies"]:
		for child in body["childs"]:
			if(child["color"] == parseColor(src)):	#if current part is source color
				for destination in destinations:

					if child["controller"]["controllers"] == None:	#check if the part already has connections and if not just write the whole array directly 
						child["controller"]["controllers"] = destinations
					else:	#if it already has connections check if the connections alreay exist and if not append them to the array
						if destination not in child["controller"]["controllers"]:
							child["controller"]["controllers"].append(destination)

#will add lookup for blocks later
def paint(block, color, JSON):
	#loop over all parts
	for body in JSON["bodies"]:
		for child in body["childs"]:
			if(child["shapeId"] == block):
				child["color"] = parseColor(color)

def searchBlueprint(bpName):
	found = False
	multipleFound = False
	for BpDirItterator in os.listdir(paths.blueprints):
		try:
			with open(f"{paths.blueprints}\\{BpDirItterator}\\description.json", "r") as descriptionFile:
				name = json.load(descriptionFile)["name"]
				if(name == bpName):
					multipleFound = found
					found = True
					bpDir = BpDirItterator
		except:
			pass
	if(multipleFound):
		error(f"Multiple blueprints with the name \"{bpName}\" have been found, please save the blueprint with a unique name.")
	if(not found):
		error(f"No blueprint with the name of \"{bpName}\" was found.")
	return bpDir



#main
if(args.input):	#if file/script input
	try:
		with open(f"{args.input}", "r") as scriptFile:
			scriptJson = json.load(scriptFile)
			
			for blueprintName in scriptJson:
				blueprintDir = searchBlueprint(blueprintName)
				
				try:
					with open(f"{paths.blueprints}\\{blueprintDir}\\blueprint.json", "r+") as blueprintFile:	
						blueprintJson = json.load(blueprintFile)
					
						for command in scriptJson[blueprintName]:
						
							if(command[0] == "connect"):
								if(len(command) != 3): error("the command 'connect' requires 2 arguments")
								connect(command[1], command[2], blueprintJson)
							elif(command[0] == "paint"):
								if(len(command) != 3): error("the command 'paint' requires 2 arguments")
								paint(command[1], command[2], blueprintJson)
							else: error(f"command: '{command[0]}' is not recognised")
					
						#overwrite file
						blueprintFile.seek(0)
						blueprintFile.write(json.dumps(blueprintJson))
						blueprintFile.truncate()
				
				except Exception as e:
					error(f"error while reading blueprint file\n{e}")

	except Exception as e:
		error(f"error while reading script\n{e}")

else:
	blueprintDir = searchBlueprint(args.blueprint)
	try:
		with open(f"{paths.blueprints}\\{blueprintDir}\\blueprint.json", "r+") as blueprintFile:
			blueprintJson = json.load(blueprintFile)

			if(args.connect):
				connect(args.connect[0], args.connect[1], blueprintJson)
			elif(args.paint):
				paint(args.paint[0], args.paint[1], blueprintJson)

			#overwrite file
			blueprintFile.seek(0)
			blueprintFile.write(json.dumps(blueprintJson))
			blueprintFile.truncate()
	except Exception as e:
		error(f"error while reading blueprint file\n{e}")
