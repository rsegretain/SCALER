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
	return row[key].split('-')[0]

### list of the plots ###

## CPU

def custom_filelist_filter(files_list):
	files_list = list(filter(lambda file : "redis" not in file.split('/')[-1] , files_list))
	return files_list

# CPU per replicas

utils.plot_cpu_per_replicas(global_result_folder_path, plots_folder_path, getServiceNameFromPodName, subtitle, CPU_LIMIT, caption=caption, filter=custom_filelist_filter)

# CPU per service

utils.plot_cpu_per_service(global_result_folder_path, plots_folder_path, getServiceNameFromPodName, subtitle, CPU_LIMIT, caption=caption, filter=custom_filelist_filter)

## AVG CPU PER REPLICAS

utils.plot_avg_cpu_per_replicas(global_result_folder_path, plots_folder_path, getServiceNameFromPodName, subtitle, CPU_LIMIT, caption=caption)

## MEMORY

# container_memory_working_set_bytes
try:
	files_list = glob(f"{global_result_folder_path}/data/container_memory_working_set_bytes/*.json")
	files_list = custom_filelist_filter(files_list)
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
		serviceFromPod=getServiceNameFromPodName,
		subtitle=subtitle,
		caption=caption,
		additionnal_serie=csv_wrk_request["C_sent_roll10"],
		additionnal_serie_key="requests_sent"
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
			serviceFromPod=getServiceNameFromPodName,
			subtitle=subtitle,
			caption=caption,
			additionnal_serie=csv_wrk_request["C_sent_roll10"],
			additionnal_serie_key="requests_sent"
		)
except:
	print("ERROR rps/replicas plot")
	traceback.print_exc()

## LATENCY

utils.plot_latency(global_result_folder_path, plots_folder_path, getServiceNameFromPodName, subtitle, MAX_LATENCY, caption=caption)

# container restart
try:
	files_list = glob(f"{global_result_folder_path}/data/kube_pod_container_status_restarts_total/*.json")
	files_list = custom_filelist_filter(files_list)
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
		serviceFromPod=getServiceNameFromPodName,
		caption=caption,
		subtitle=subtitle
	)
except:
	print("ERROR container restart plot")
	traceback.print_exc()


## merge replicas and replicas ready
try:
	# replicas count
	files_list = glob(f"{global_result_folder_path}/data/kube_deployment_spec_replicas/*.json")
	files_list = custom_filelist_filter(files_list)
	replicas_datas = utils.get_datas_with_metric_per_key(
		files_list=files_list,
		key='deployment',
		value_start_zero=False
	)

	# replicas ready
	files_list = glob(f"{global_result_folder_path}/data/kube_deployment_status_replicas_ready/*.json")
	files_list = custom_filelist_filter(files_list)
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

	# reforme le tableau de donnée pour que toutes les valeurs soit dans la même colonne, distinguée par une nouvelle colonne service
	replicas_datas = replicas_datas.melt(id_vars="timestamp", var_name="Pod", value_name="kube_deployment_spec_replicas")
	replicas_ready_datas = replicas_ready_datas.melt(id_vars="timestamp", var_name="Pod", value_name="kube_deployment_status_replicas_ready")

	# add a service column, different than pod
	replicas_datas["Service"] = replicas_datas.apply(getServiceNameFromPodName, axis=1, key="Pod")
	replicas_ready_datas["Service"] = replicas_ready_datas.apply(getServiceNameFromPodName, axis=1, key="Pod")

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

	call_graph, dot_graph = utils.plot_call_graph(f"{global_result_folder_path}/data/call_graph", plots_folder_path, f"\nMicroservices call graph - total processed requests (istio)\n{subtitle}", "redis")

except:
	print("ERROR call_graph plot")
	traceback.print_exc()