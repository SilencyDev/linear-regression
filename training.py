import sys

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
	return number * (max - min) + min

def denormalizeSlope(slope):
	return slope * (maxPrice - minPrice)/(maxKm - minKm)

def denormalizeIntercept(intercept, slope, min, max):
	return denormalize(intercept, min, max) - denormalizeSlope(slope) * minKm

kmsNormalize = normalize(kms, minKm, maxKm)
pricesNormalize = normalize(prices, minPrice, maxPrice)

#means
meanKms = sum(kmsNormalize) / len(kmsNormalize)
meanprices = sum(pricesNormalize) / len(pricesNormalize)

slope = 0
intercept = 0
learningRate = 0.1
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

def gradient_descent(kmsNormalize, pricesNormalize, intercept, slope, learningRate, iterations):
	nb = len(kmsNormalize)
	for iteration in range(iterations):
		interceptGradient = 0
		slopeGradient = 0
		for i in range(nb):
			error = estimatePrice(intercept, slope, kmsNormalize[i]) - pricesNormalize[i]
			interceptGradient += error
			slopeGradient += error * kmsNormalize[i]
		intercept -= (interceptGradient * learningRate / nb)
		slope -= (slopeGradient * learningRate / nb)

		print(iteration, intercept, slope, learningRate)
		if (iteration > (iterations - 50) or iteration % 10 == 0):
			printGraph(denormalizeSlope(slope), denormalizeIntercept(intercept, slope, minPrice, maxPrice), kms, prices, "kms", "prices")
			# printGraph(slope, intercept, kmsNormalize, pricesNormalize)
			
		
	return intercept, slope


intercept, slope = gradient_descent(kmsNormalize, pricesNormalize, intercept, slope, learningRate, iterations)


plt.show()

# save to json
result = {
    "slope": denormalizeSlope(slope),
    "intercept": denormalizeIntercept(intercept, slope, minPrice, maxPrice)
}

json_file_path = "trainedSlopeIntercept.json"

with open(json_file_path, 'w') as f:
    json.dump(result, f)

print("trained slope and intercept saved in path:", json_file_path)