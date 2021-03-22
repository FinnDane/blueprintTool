
# BlueprintTool
A CLI blueprintTool

I made because I wanted a simple and fast solution for logic projects and didn't like having to use a GUI for that.

Currently only has a small ammount of features with a way to make "scripts" in JSON, I will probably add more features later.

Disclaimer: this is absolute shitcode

## Basic usage
```
blueprintTool.py [-h] (-b BLUEPRINT | -i INPUT) (-c SRC DST | -p BLOCK COLOR)
```
You can use HEX for the colors or the format: "\<baseColor>-\<row>" where \<baseColor> is one of the following:

`gray, yellow, lime, green, cyan, blue, violet, magenta, red or orange`

capitalization does not matter.

and \<row> are their vertical variants numbered 1 through 4 respectively 
## Scripting
Use the -i/-\-input flag to specify the json file.

Use this format for the JSON file:
```json
{
	"<blueprintName>":
	[
		[
			"<function>",
			"<argument1>",
			"<argument2>",
			"<etc...>"
		]
	]
}
```
Example script:
```json
{
	"blueprint1":
	[
		[
			"connect",
			"eeeeee",
			"222222"
		],
		[
			"connect",
			"gray-1",
			"orange-1"
		]
	],
	"blueprint2":
	[
		[
			"connect",
			"ffffff",
			"eeeeee"
		]
	]
}
```