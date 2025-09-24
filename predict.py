import sys

sys.path.insert(0, './modules/')

import pandas as pd


print("please enter a mileage to receive an estimation of price : ")

try: 
	kms = float(input())
except:
	print("An error was raised while parsing your prompt, make sure your input is a number !")
	sys.exit(1)

slope = 0
intercept = 0
#read training data
try :
	slopeInterceptcsv = pd.read_json("trainedSlopeIntercept.json", typ='series')
	slope = float(slopeInterceptcsv.get("slope", 0))
	intercept = float(slopeInterceptcsv.get("intercept", 0))
except :
	print("Couldn't read trainedSlopeIntercept.json, slope and intercept kept at 0")
#use slope and intercept
result = slope * kms + intercept
print(f"Here your estimation for {kms} mileage : " + str(result))