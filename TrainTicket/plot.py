from plotnine import *
import pandas as pandas
from glob import glob

import sys
import os
import traceback

from datetime import datetime

sys.path.append("../global-ressources")
import plot_utils as utils

sys.path.append("./ressources")
from globalAppConf import *


subtitle=None

# read the script args
if len(sys.argv) <= 2:
	print("Error missing args: <path to result folder> <loadfilename> [<subtitle>]")
if len(sys.argv) >= 1 + 2:
	global_result_folder_path = sys.argv[1]
	load_filename = sys.argv[2]
if len(sys.argv) >= 1 + 3:
	subtitle = sys.argv[3]

experiment_folder_name = global_result_folder_path.split('/')[-1]
today_date = datetime.today().strftime('%Y/%m/%d')
caption=f"experiment id: {experiment_folder_name} - plot generated on {today_date}"

# ensure the plots folder exist
plots_folder_path = f"{global_result_folder_path}/plots"
if not os.path.exists(plots_folder_path):
	os.makedirs(plots_folder_path)

def getServiceNameFromPodName(row, key):
	splitted = row[key].split('-')
	splitted = splitted[1:len(splitted)-2]
	name = ""
	for s in splitted:
		name += s + "-"
	return name.strip('-')

def getServiceNameFromPodNameIstio(row, key):
	splitted = row[key].split('-')
	splitted = splitted[1:len(splitted)]
	name = ""
	for s in splitted:
		name += s + "-"
	return name.strip('-')

def select_10_max(datas):
	max_value = []

	for column in datas.columns:
		if column == "timestamp":
			continue
		else:
			max = pandas.Series.max(datas[column])
			max_value.append((column, max))
	
	def sort_util(t):
		return t[1]
	max_value.sort(key=sort_util, reverse=True)
	
	max_value = max_value[min(9, len(max_value)):len(max_value)]
	
	for t in max_value:
		datas = datas.drop(t[0], axis=1)
	
	return datas

def select_10_services_max(datas):
	max_value = []

	for column in datas.columns:
		if column == "timestamp":
			continue
		else:
			max = pandas.Series.max(datas[column])
			max_value.append((column, max))
	
	def sort_util(t):
		return t[1]
	max_value.sort(key=sort_util, reverse=True)

	for i in range(len(max_value)):
		splitted = max_value[i][0].split('-')
		splitted = splitted[1:len(splitted)-2]
		name = ""
		for s in splitted:
			name += s + "-"
		max_value[i] = (max_value[i][0], max_value[i][1], name.strip('-'))

	services = {}
	cutIdx = 9
	for i in range(len(max_value)):
		# print(max_value[i])
		if len(services) < 10:
			services[max_value[i][2]] = ""
		else:
			cutIdx = i
			break
	
	max_value = max_value[min(cutIdx, len(max_value)):len(max_value)]
	
	for t in max_value:
		datas = datas.drop(t[0], axis=1)
	
	return datas

def select_10_services_max_fromServiceName(datas):
	max_value = []

	for column in datas.columns:
		if column == "timestamp":
			continue
		else:
			max = pandas.Series.max(datas[column])
			max_value.append((column, max))
	
	def sort_util(t):
		return t[1]
	max_value.sort(key=sort_util, reverse=True)

	for i in range(len(max_value)):
		splitted = max_value[i][0].split('-')
		splitted = splitted[1:len(splitted)]
		name = ""
		for s in splitted:
			name += s + "-"
		max_value[i] = (max_value[i][0], max_value[i][1], name.strip('-'))

	services = {}
	cutIdx = 9
	for i in range(len(max_value)):
		# print(max_value[i])
		if len(services) < 10:
			services[max_value[i][2]] = ""
		else:
			cutIdx = i
			break
	
	max_value = max_value[min(cutIdx, len(max_value)):len(max_value)]
	
	for t in max_value:
		datas = datas.drop(t[0], axis=1)
	
	return datas

### list of the plots ###

## CPU

# CPU per replicas

utils.plot_cpu_per_replicas(global_result_folder_path, plots_folder_path, getServiceNameFromPodName, subtitle, CPU_LIMIT, select_10_services_max, caption=caption)

# CPU per service

utils.plot_cpu_per_service(global_result_folder_path, plots_folder_path, getServiceNameFromPodNameIstio, subtitle, CPU_LIMIT, select_10_services_max_fromServiceName, caption=caption)

# AVG CPU PER REPLICAS

utils.plot_avg_cpu_per_replicas(global_result_folder_path, plots_folder_path, getServiceNameFromPodNameIstio, subtitle, CPU_LIMIT, select_10_services_max_fromServiceName, caption=caption)

## MEMORY

# container_memory_working_set_bytes

try:
	files_list = glob(f"{global_result_folder_path}/data/container_memory_working_set_bytes/*.json")
	files_list = sorted(files_list, reverse=True)
	datas = utils.get_datas_with_metric_per_key(
		files_list=files_list,
		key='pod',
		value_start_zero=False,
		gauge=True
	)
	# print(datas)
	# print(datas.columns)
	utils.plot_from_datas(
		datas=datas,
		plots_folder_path=plots_folder_path,
		title="Memory usage per service",
		metric_name="container_memory_working_set_bytes",
		ylab="Memory usage (byte)",
		select=select_10_services_max,
		custom_y_breaks_func=utils.custom_breaks_rps,
		custom_y_label_func=utils.custom_labels_bytes,
		serviceFromPod=getServiceNameFromPodName,
		caption=caption,
		subtitle=subtitle
	)
except:
	print("ERROR memory plot")
	traceback.print_exc()

## REQUESTS


# WRK REQUESTS
utils.plot_wrk_requests(global_result_folder_path, plots_folder_path, load_filename, subtitle, caption)

# istio_requests_total : mobile average
csv_wrk_request = pandas.read_csv(f"{global_result_folder_path}/data/requests_stats.csv", header=0)#, usecols=["timestamp", "requests_sent"])
csv_wrk_request["C_sent_roll10"] = csv_wrk_request["requests_sent"].diff().rolling(10, min_periods=0).mean()

try:

	dir_list = glob(f"{global_result_folder_path}/data/istio_requests_total/*")
	datas = utils.get_datas_with_metric_per_directory(
		dir_list=dir_list,
		value_start_zero=True
	)

	x = 20
	def custom_rolling_average_requests(datas):
		return utils.rolling_average_X_Y(datas, x, 1)

	utils.plot_from_datas(
		datas=datas,
		plots_folder_path=plots_folder_path,
		title=f"Processed requests/s per service - rolling avg {x}s",
		metric_name="istio_requests_total_avg",
		custom_y_breaks_func=utils.custom_breaks_rps,
		custom_y_label_func=utils.custom_labels_value,
		logScale=False,
		ylab="Requests/s",
		transform=custom_rolling_average_requests,
		select=select_10_services_max_fromServiceName,
		serviceFromPod=getServiceNameFromPodNameIstio,
		subtitle=subtitle,
		caption=caption,
		additionnal_serie=csv_wrk_request["C_sent_roll10"],
		additionnal_serie_key="wrk-requests_sent"
	)

except:
	print("ERROR rps/service plot")
	traceback.print_exc()

## REQUESTS PER REPLICAS

try:

	dir_list = glob(f"{global_result_folder_path}/data/requests_per_pod/*.json")
	if (dir_list):
		datas = utils.get_datas_with_metric_per_filename(
			files_list=dir_list,
			value_start_zero=True
		)
		utils.plot_from_datas(
			datas=datas,
			plots_folder_path=plots_folder_path,
			title=f"Processed requests/s per pod - rolling avg {x}s",
			metric_name="requests_per_pod",
			custom_y_breaks_func=utils.custom_breaks_rps,
			custom_y_label_func=utils.custom_labels_value,
			ylab="Requests/s",
			transform=custom_rolling_average_requests,
			select=select_10_services_max,
			serviceFromPod=getServiceNameFromPodName,
			subtitle=subtitle,
			caption=caption,
			additionnal_serie=csv_wrk_request["C_sent_roll10"],
			additionnal_serie_key="wrk-requests_sent--"
		)
except:
	print("ERROR rps/replicas plot")
	traceback.print_exc()

## LATENCY

RATIO = { # search ticket
	"ts-basic-service" : 12.5,
	"ts-config-service" : 5,
	"ts-order-service" : 7.5,
	"ts-price-service" : 2.5,
	"ts-route-service" : 12.5,
	"ts-seat-service" : 5,
	"ts-station-service" : 20,
	"ts-ticketinfo-service" : 12.5,
	"ts-train-service" : 10,
	"ts-travel-service" : 11
}

utils.plot_latency(global_result_folder_path, plots_folder_path, getServiceNameFromPodNameIstio, subtitle, MAX_LATENCY, caption=caption, select=select_10_services_max_fromServiceName, RATIO=RATIO)

## latency histogram

utils.plot_latency_histogram(global_result_folder_path, plots_folder_path, FRONTEND, MAX_LATENCY)

## REQUEST REPARTITION

utils.plot_requests_repartition(global_result_folder_path, plots_folder_path, FRONTEND, MAX_LATENCY)

# container restart

try:

	files_list = glob(f"{global_result_folder_path}/data/kube_pod_container_status_restarts_total/*.json")
	datas = utils.get_datas_with_metric_per_filename(
		files_list=files_list,
		value_start_zero=True
	)
	utils.plot_from_datas(
		datas=datas,
		plots_folder_path=plots_folder_path,
		title="Container restart count per service",
		metric_name="kube_pod_container_status_restarts_total",
		ylab="Restart count",
		serviceFromPod=getServiceNameFromPodNameIstio,
		select=select_10_max,
		caption=caption,
		subtitle=subtitle
	)

except:
	print("ERROR replica restart plot")
	traceback.print_exc()


## merge replicas and replicas ready

try:

	# replicas count
	files_list = glob(f"{global_result_folder_path}/data/kube_deployment_spec_replicas/*.json")
	replicas_datas = utils.get_datas_with_metric_per_key(
		files_list=files_list,
		key='deployment',
		value_start_zero=False
	)

	# replicas ready
	files_list = glob(f"{global_result_folder_path}/data/kube_deployment_status_replicas_ready/*.json")
	replicas_ready_datas = utils.get_datas_with_metric_per_key(
		files_list=files_list,
		key='deployment',
		value_start_zero=False
	)

	# on veut un temps qui commence à zéro
	replicas_datas["timestamp"] = replicas_datas.apply(utils.substract, axis=1, key="timestamp",value=(pandas.Series.min(replicas_datas["timestamp"])+60))
	replicas_ready_datas["timestamp"] = replicas_ready_datas.apply(utils.substract, axis=1, key="timestamp",value=(pandas.Series.min(replicas_ready_datas["timestamp"])+60))

	replicas_datas = replicas_datas.drop(replicas_datas[replicas_datas.timestamp < 0].index)
	replicas_ready_datas = replicas_ready_datas.drop(replicas_ready_datas[replicas_ready_datas.timestamp < 0].index)

	replicas_datas = select_10_max(replicas_datas)
	replicas_ready_datas = select_10_max(replicas_ready_datas)

	# reforme le tableau de donnée pour que toutes les valeurs soit dans la même colonne, distinguée par une nouvelle colonne service
	replicas_datas = replicas_datas.melt(id_vars="timestamp", var_name="Pod", value_name="kube_deployment_spec_replicas")
	replicas_ready_datas = replicas_ready_datas.melt(id_vars="timestamp", var_name="Pod", value_name="kube_deployment_status_replicas_ready")

	# add a service column, different than pod
	replicas_datas["Service"] = replicas_datas.apply(getServiceNameFromPodNameIstio, axis=1, key="Pod")
	replicas_ready_datas["Service"] = replicas_ready_datas.apply(getServiceNameFromPodNameIstio, axis=1, key="Pod")

	symbol_interval = round(pandas.Series.max(datas["timestamp"]) / 10)

	replicas_datas_thinned = pandas.DataFrame()
	for data_idx in replicas_datas.index:
		if replicas_datas.loc[data_idx]["timestamp"] % symbol_interval == 0:
			replicas_datas_thinned = pandas.concat([replicas_datas_thinned, replicas_datas.loc[[data_idx]]])


	replicas_ready_datas_thinned = pandas.DataFrame()
	for data_idx in replicas_ready_datas.index:
		if replicas_ready_datas.loc[data_idx]["timestamp"] % symbol_interval == 0:
			replicas_ready_datas_thinned = pandas.concat([replicas_ready_datas_thinned, replicas_ready_datas.loc[[data_idx]]])

	utils.plot_replicas_spec_and_ready(plots_folder_path, replicas_datas, replicas_ready_datas, replicas_datas_thinned, replicas_ready_datas_thinned, subtitle, caption)
except:
	print("ERROR replicas count/ready plot")
	traceback.print_exc()

### graph call

try:

	call_graph, dot_graph = utils.plot_call_graph(f"{global_result_folder_path}/data/call_graph", plots_folder_path, f"\nMicroservices call graph - total processed requests (istio)\n{subtitle}", "mongo")

except:
	print("ERROR call_graph plot")
	traceback.print_exc()