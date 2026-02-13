import sys
import math
import pandas as pandas
import subprocess
import time

import os
conf_folder = sys.argv[3]
sys.path.append(os.path.abspath(conf_folder))
from autoGroupScalerConf import *

NAMESPACE = "default"

REPLICAS = []
for i in range(len(DEPLOYMENTS)):
	REPLICAS.append(1)

def scale_deployment(deployment, replicas):
	cmd = ["kubectl", "scale", "deployment", deployment, f"--replicas={replicas}", "-n", NAMESPACE]
	print(cmd)
	subprocess.run(cmd)

def main():
	LOAD_FILE = sys.argv[1]
	ANTICIPATION_WINDOW = int(sys.argv[2])
	TIME_S = ANTICIPATION_WINDOW

	LOAD_VALUES = pandas.read_csv(LOAD_FILE, names=["time", "values"])

	currentValue = 0

	maxValue = 0
	for i in range(ANTICIPATION_WINDOW):
		currentValue = LOAD_VALUES.loc[i % LOAD_VALUES["values"].size, "values"]
		if currentValue > maxValue:
			maxValue = currentValue
	currentValue = maxValue	

	while TIME_S <= LOAD_VALUES["values"].size:
		print(TIME_S - ANTICIPATION_WINDOW, "->", TIME_S)

		for serviceID in ACTIVELY_SCALED_SERVICES:
			if REPLICAS[serviceID] < math.ceil(currentValue / (THRESHOLDS[serviceID] - 1)):
				REPLICAS[serviceID] = math.ceil(currentValue / (THRESHOLDS[serviceID] - 1))
				scale_deployment(DEPLOYMENTS[serviceID], REPLICAS[serviceID])

		for parentServiceID,  childServiceIDs in enumerate(PASSIVELY_SCALED_SERVICES):
			for childServiceID in childServiceIDs:
				if (REPLICAS[parentServiceID] * THRESHOLDS[parentServiceID]) > (REPLICAS[childServiceID] * THRESHOLDS[childServiceID]):
					REPLICAS[childServiceID] = math.ceil((REPLICAS[parentServiceID] * THRESHOLDS[parentServiceID]) / THRESHOLDS[childServiceID])
					scale_deployment(DEPLOYMENTS[childServiceID], REPLICAS[childServiceID])

		time.sleep(1)

		currentValue = LOAD_VALUES.loc[TIME_S % LOAD_VALUES["values"].size, "values"]
		TIME_S += 1


if __name__ == "__main__":
	main()
