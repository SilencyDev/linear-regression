import sys

sys.path.insert(0, './modules/')

# get and parse csv
import pandas as pd
import matplotlib.pyplot as plt
import json


figure, ax = plt.subplots()

try :
	data =  pd.read_csv("data.csv")
	kms = data['km']
	prices = data['price']
	minKm, maxKm, minPrice, maxPrice = kms.min(), kms.max(), prices.min(), prices.max()
except :
	print("Couldn't read data.csv, make sure km and price are provided and associated values are number")
	sys.exit(1)

# normalization
def normalize(number, min, max):
	return (number - min) / (max - min)

def denormalize(number, min, max):
	return number *(max - min) + min

def denormalizeSlope(number):
	return number * (maxPrice - minPrice)/(maxKm - minKm)

def denormalizeIntercept(number):
	return number *(maxPrice - minPrice) + minPrice

kmsNormalize = normalize(kms, minKm, maxKm)
pricesNormalize = normalize(prices, minPrice, maxPrice)

#means
meanKms = sum(kmsNormalize) / len(kmsNormalize)
meanprices = sum(pricesNormalize) / len(pricesNormalize)

slope = 0
intercept = 0
learningRateIntercept = 1
learningRateSlope = 1
iterations = 1000

def printGraph(slope, intercept, x, y, xlabel, ylabel):
	ax.clear()
	ax.scatter(x,y, color='blue', label='donnee')
	# print(f"graph : {slope}, {intercept}")
	ax.plot(x, slope * x + intercept , color='red', label="linear regression")
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	# ax.plot(kms, -0.01933230365921051 * kms + 8277.034168116184 , color='red', label="linear regression")
	# plt.show()
	plt.pause(0.1)
	

def estimatePrice(intercept, slope, km) :
	return slope * km + intercept

def gradient_descent(kmsNormalize, pricesNormalize, intercept, slope, learningRateIntercept, learningRateSlope, iterations):
	nb = len(kmsNormalize)
	oldIntercept = False
	oldSlope = False
	for iteration in range(iterations):
		interceptGradient = 0
		slopeGradient = 0
		for i in range(nb):
			normalizedPriceEstimate = estimatePrice(intercept, slope, kmsNormalize[i])
			interceptGradient += normalizedPriceEstimate - pricesNormalize[i]
			slopeGradient += (normalizedPriceEstimate - pricesNormalize[i]) * kmsNormalize[i]
		intercept -= (learningRateIntercept * interceptGradient / nb)
		slope -= (learningRateSlope * slopeGradient / nb)
		if (iteration != 0) :
			if (oldIntercept != (learningRateIntercept * interceptGradient >= 0)):
				learningRateIntercept *= 0.5
			elif (learningRateIntercept * 1.1 <= 1.0):
				learningRateIntercept *= 1.1
			else:
				learningRateIntercept = 1
			if (oldSlope  != (learningRateSlope * slopeGradient >= 0)):
				learningRateSlope *= 0.5
			elif (learningRateSlope * 1.1 <= 1.0):
				learningRateSlope *= 1.1
			else:
				learningRateSlope = 1
		if (learningRateIntercept * interceptGradient >= 0) :
			oldIntercept = True
		else :
			oldIntercept = False
		if (learningRateSlope * slopeGradient >= 0) :
			oldSlope = True
		else :
			oldSlope = False
		print(iteration, intercept, slope, learningRateIntercept, learningRateSlope)
		if (iteration < 50 or iteration % 100 == 0):
			printGraph(denormalizeSlope(slope), denormalizeIntercept(intercept), denormalize(kmsNormalize, minKm, maxKm), denormalize(pricesNormalize, minPrice, maxPrice), "kms", "prices")
			# printGraph(slope, intercept, kmsNormalize, pricesNormalize)
			
		
	return intercept, slope

intercept, slope = gradient_descent(kmsNormalize, pricesNormalize, intercept, slope, learningRateIntercept, learningRateSlope, iterations)


plt.show()

# save to json
result = {
    "slope": denormalizeSlope(slope),
    "intercept": denormalizeIntercept(intercept)
}

json_file_path = "trainedSlopeIntercept.json"

with open(json_file_path, 'w') as f:
    json.dump(result, f)

print("trained slope and intercept saved in path:", json_file_path)