from plotnine import *
import pandas as pandas
import json
from glob import glob
import math
import pydot
import traceback

def substract(row, key, value):
	""" 
	Used by applying the function to a pandas serie.
	Substract a value from the given row and return the result
	"""
	return row[key] - value

def replaceNaNWithValue (row, key, value):
	if row[key] == "NaN":
		return value
	else:
		return row[key]

def negToZero (row, key):
	if row[key] < 0:
		return 0
	else:
		return row[key]

def custom_breaks_rps(limits):
	min, max = limits[0], limits[1]

	idx = 0
	interval = 1
	multiplier=[2,5]
	while ((max // interval) + 1) > 10:
		interval *= multiplier[idx % 2]
		idx += 1

	if (interval % 2 == 0) and (((max // (interval / 2)) + 1) <= 10):
		interval = int(interval / 2)
	breaks = []
	for i in range(0, round(((max // interval) + 1) * interval), interval):
		breaks.append(i)
	return breaks

# def custom_minor_breaks_continuous(limits):
# 	min, max = limits[0], limits[1]
# 	majorBreaks = custom_breaks_ms_log(limits)
# 	# del majorBreaks[-1]

# 	minorBreaks = []
# 	for mb in majorBreaks:
# 		for i in range(1, 10):
# 			if mb * i > max:
# 				break
# 			minorBreaks.append(mb * i)
# 	# print(limits, majorBreaks, minorBreaks)
# 	return minorBreaks

def custom_breaks_replicas(limits):
	min, max = int(limits[0]), int(limits[1])

	idx = 0
	interval = 1
	while (((max - min) // interval) + 1) >= 10:
		if idx % 2 == 0:
			interval *= 2
		else:
			interval *= 5
		idx += 1

	return range(min, round((((max - min) // interval) + 1) * interval), interval)

def custom_breaks_millicpu(limits):
	min, max = limits[0], limits[1]

	pct = 1000
	idx = 0
	while (math.floor(max * pct) + 1) >= 10:
		if idx % 2 == 0:
			pct /= 2
		else:
			pct /= 5
		idx += 1

	return [x / pct for x in range(0, math.floor(max * pct) + 1, 1)]

def custom_breaks_by_minutes(limits):
	"""
	Used during the building of a plot to generate custom breaks for a axis.
	Generate a break every minute.
	"""
	min, max = limits[0], limits[1]
	
	# return range(0, math.floor(max), 60)
	idx = 0
	interval = 60
	while ((max // interval)) > 10 and idx < 5:
		if idx == 0:
			interval = 2 * 60
		elif idx == 1:
			interval = 5 * 60
		elif idx == 2:
			interval = 10 * 60
		elif idx == 3:
			interval = 20 * 60
		elif idx == 4:
			interval = 60 * 60
		idx += 1

	return range(0, round(((max // interval) + 1) * interval), interval)

def custom_labels_s(breaks):
	"""
	Used during the building of a plot to generate custom labels for the break of a axis.
	Generate labels according to the scale of the break value, to keep it human friendly.
	"""
	second = 1
	minute = 60 * second
	hour = 60 * minute
	day = 24 * hour
	scale = second
	symbol = "s"
	
	labels = []
	for b in breaks:
		if b == 0:
			labels.append("0")
		else:
			if b >= day:
				scale = day
				symbol = "D"
			elif b >= hour:
				scale = hour
				symbol = "H"
			elif b >= minute:
				scale = minute
				symbol = "m"

			labels.append(str(b // scale) + symbol)
	return labels

# named custom_breaks_ms before
def custom_breaks_ms_log(limits):
	min, max = limits[0], limits[1]

	base = 10
	idx = 0
	pow_value = 0
	
	while (max / pow(base, pow_value)) >= base:
		pow_value += 1
		if pow_value == 10:
			base *=10
			pow_value = 0
	
	breaks = []

	for i in range(pow_value+1):
		breaks.append(1 * pow(base, i))
	
	return breaks

def custom_minor_breaks_log10(limits):
	min, max = limits[0], limits[1]
	majorBreaks = custom_breaks_ms_log(limits)
	# del majorBreaks[-1]

	minorBreaks = []
	for mb in majorBreaks:
		for i in range(1, 10):
			if mb * i > max:
				break
			minorBreaks.append(mb * i)
	# print(limits, majorBreaks, minorBreaks)
	return minorBreaks


def value_to_labels_ms(value):
	ms = 1
	second = 1000 * ms
	minute = 60 * second
	hour = 60 * minute
	day = 24 * hour
	scale = ms
	symbol = "ms"

	if math.isinf(value):
		return "Inf"

	if value == 0:
		return "0"
	else:
		if value >= day:
			scale = day
			symbol = "D"
		elif value >= hour:
			scale = hour
			symbol = "H"
		elif value >= minute:
			scale = minute
			symbol = "m"
		elif value >= second:
			scale = second
			symbol = "s"
		value = value / scale
		if (value - int(value)) == 0:
			value = int(value)
		return str(value) + " " + symbol

def custom_labels_ms(breaks):
	"""
	Used during the building of a plot to generate custom labels for the break of a axis.
	Generate labels according to the scale of the break value, to keep it human friendly.
	"""
	ms = 1
	second = 1000 * ms
	minute = 60 * second
	hour = 60 * minute
	day = 24 * hour
	scale = ms
	symbol = "ms"
	
	labels = []
	for b in breaks:
		labels.append(value_to_labels_ms(b))

		# if b == 0:
		# 	labels.append("0")
		# else:
		# 	if b >= day:
		# 		scale = day
		# 		symbol = "D"
		# 	elif b >= hour:
		# 		scale = hour
		# 		symbol = "H"
		# 	elif b >= minute:
		# 		scale = minute
		# 		symbol = "m"
		# 	elif b >= second:
		# 		scale = second
		# 		symbol = "s"

		# 	labels.append(str(b / scale) + " " + symbol)
	return labels

def scale_value(value):
	unit = 1
	kilo = 1000 * unit
	mega = 1000 * kilo
	giga = 1000 * mega
	tera = 1000 * giga
	scale = unit
	symbol = ""

	if value == 0:
			return 0, None
	else:
		if value >= tera:
			scale = tera
			symbol = "T"
		elif value >= giga:
			scale = giga
			symbol = "G"
		elif value >= mega:
			scale = mega
			symbol = "M"
		elif value >= kilo:
			scale = kilo
			symbol = "K"
		
		return (value / scale), symbol

def custom_labels_value(breaks):
	"""
	Used during the building of a plot to generate custom labels for the break of a axis.
	Generate labels according to the scale of the break value, to keep it human friendly.
	"""
	
	labels = []
	for b in breaks:
		value, symbol = scale_value(b)
		if value == 0:
			labels.append(str(value))
		else:
			labels.append(str(value) + " " + symbol)
	return labels

def custom_labels_bytes(breaks):
	"""
	Used during the building of a plot to generate custom labels for the break of a axis.
	Generate labels according to the scale of the break value, to keep it human friendly.
	Specific version for Bytes.
	"""
	labels = []
	for b in custom_labels_value(breaks):
		if b == "0":
			labels.append(b)
		else:
			labels.append(b + "B")
	return labels

def custom_labels_pct(breaks):
	labels = []
	for b in breaks:
		labels.append(str(b) + " %")
	return labels

def rolling_average_60s(datas):
	"""
	Transform the given data.
	The data should be accumulation.

	Each serie, except timestamp, is transformed to the amount per second 
	based on the rolling average over 60s of the raw value.
	"""
	for column in datas.columns:
		if column == "timestamp":
			continue
		datas[column] = datas[column].diff().rolling(60, min_periods=0).mean()
	return datas

def rolling_average_60s_20s(datas):
	"""
	Transform the given data.
	The data should be accumulation.

	Each serie, except timestamp, is transformed to the amount per second 
	based on the rolling average over 60s of the raw value.
	"""
	for column in datas.columns:
		if column == "timestamp":
			continue
		datas[column] = datas[column].diff().rolling(60, min_periods=0).mean().rolling(20, min_periods=0).mean()
	return datas

def rolling_average_X_Y(datas, x, y):
	"""
	Transform the given data.
	The data should be accumulation.
	"""
	for column in datas.columns:
		if column == "timestamp":
			continue
		datas[column] = datas[column].diff().rolling(x, min_periods=0).mean().rolling(y, min_periods=0).mean()
	return datas
	

def get_datas_with_metric_per_directory(dir_list, value_start_zero):
	"""
	Read the data contained in a list of folders.
	Each folder contains one data serie, potentially scattered across multiple files.
	
	dir_list : the folders list,
	value_start_zero : boolean, if true, each value will be substracted the min of it's serie,
	"""
	
	# reading and merging the files in each folder
	datas = pandas.DataFrame()
	i = 0
	for dir in dir_list:
		data_files = glob(dir + "/*.json")
		service = dir.split('/')[-1]
		j = 0
		for data_file_path in data_files:
			with open(data_file_path, 'r') as file:
				data_file = json.load(file)
			raw_data = pandas.DataFrame(data=data_file['values'], columns=["timestamp", service])
			raw_data[service] = raw_data.apply(replaceNaNWithValue, axis=1, key=service, value=0)
			raw_data[service] = pandas.to_numeric(raw_data[service])

			# si la valeur est un compteur, on peut vouloir ignorer les valeurs précédent start_timestamp
			if value_start_zero:
				raw_data[service] = raw_data.apply(substract, axis=1, key=service, value=pandas.Series.min(raw_data[service]))

			if i == 0 and j == 0:
				# la première série de donnée du premier dossier initialise datas
				datas["timestamp"] = raw_data["timestamp"]
				datas[service] =  raw_data[service]
			else:
				if j == 0:
					# la première série de donnée d'un dossier ajoute la colonne du dossier
					datas = pandas.merge(datas, raw_data, how='outer', on='timestamp', suffixes=(None, None))
				else:
					# les séries suivantes du dossier sont additionnée à la première série du dossier
					datas = pandas.merge(datas, raw_data, how='outer', on='timestamp', suffixes=(None, f"_{j}"))
					datas[service] = datas[service].add(datas[f"{service}_{j}"], fill_value=0)
					datas = datas.drop(f"{service}_{j}", axis=1)			
			j += 1
		i += 1
	return datas

def get_datas_with_metric_per_filename(files_list, value_start_zero, gauge=False):
	"""
	Read the data contained in a list of files.
	A data serie is scattered across all file with the same prefix.
	
	dir_list : the folders list,
	value_start_zero : boolean, if true, each value will be substracted the min of it's serie,
	gauge : boolean, default false.
		If true, the values from the different files of a serie will not be added.
		For each timestamp, if multiple values are available from different files,
		the value will be taken from the file with the latest first timestamp.
	"""

	# reading and merging the files
	datas = pandas.DataFrame()
	i = 0
	for data_file_path in files_list:
		# tous les fichiers concernant le même service auront le même nom
		service = data_file_path.split('/')[-1].split('.')[0].split('(')[0]
		#print(data_file_path.split('/')[-1], service)
		
		with open(data_file_path, 'r') as file:
			data_file = json.load(file)
		raw_data = pandas.DataFrame(data=data_file['values'], columns=["timestamp", service])
		raw_data[service] = raw_data.apply(replaceNaNWithValue, axis=1, key=service, value=0)
		raw_data[service] = pandas.to_numeric(raw_data[service])

		# si la valeur est un compteur, on peut vouloir ignorer les valeurs précédent start_timestamp
		# todo : uniquement le vrai start_timestamp, pas le min, il peut être en plein dans l'interval de l'exp si redemarrage
		if value_start_zero:
			raw_data[service] = raw_data.apply(substract, axis=1, key=service, value=pandas.Series.min(raw_data[service]))

		if i == 0:
			# la première série de donnée initialise datas
			datas["timestamp"] = raw_data["timestamp"]
			datas[service] =  raw_data[service]
		elif service in datas.columns:
			datas_min_timestamp = datas["timestamp"].min()
			datas_max_timestamp = datas["timestamp"].max()
			datas = pandas.merge(datas, raw_data, how='outer', on='timestamp', suffixes=(None, f"_{i}"))
			if gauge:
				# use the data from the correct series no matter the read order 
				def get_correct_row(row):
					if ((
							datas_min_timestamp < raw_data["timestamp"].min() and 
							row["timestamp"] < raw_data["timestamp"].min()
						)
						or 
						(
							raw_data["timestamp"].min() < datas_min_timestamp and 
							row["timestamp"] > datas_min_timestamp
						)
						or
						(
							raw_data["timestamp"].min() == datas_min_timestamp and
							raw_data["timestamp"].max() < datas_max_timestamp
						)):

						return row[service]
					else:
						return row[f"{service}_{i}"]
				
				datas[service] = datas.apply(get_correct_row, axis=1)
			else:
				datas[service] = datas[service].add(datas[f"{service}_{i}"], fill_value=0)
			datas = datas.drop(f"{service}_{i}", axis=1)
		else:
			datas = pandas.merge(datas, raw_data, how='outer', on='timestamp', suffixes=(None, None))
		i += 1
		#print(datas)
	return datas


def get_datas_with_metric_per_key(files_list, key, value_start_zero, gauge=False):
	"""
	Read the data contained in a list of files.
	A data serie is scattered across all files with the same key in header.
	
	dir_list : the folders list,
	key : the key to read in the header,
	value_start_zero : boolean, if true, each value will be substracted the min of it's serie,
	title : string, the title of the plot,
	gauge : boolean, default false.
		If true, the values from the different files of a serie will not be added.
		For each timestamp, if multiple values are available from different files,
		the value will be taken from the file with the latest first timestamp.
	"""

	# reading and merging the files
	datas = pandas.DataFrame()
	i = 0
	for data_file_path in files_list:
		
		with open(data_file_path, 'r') as file:
			data_file = json.load(file)

		service = data_file['metric'][key]
		raw_data = pandas.DataFrame(data=data_file['values'], columns=["timestamp", service])
		raw_data[service] = raw_data.apply(replaceNaNWithValue, axis=1, key=service, value=0)
		raw_data[service] = pandas.to_numeric(raw_data[service])

		# si la valeur est un compteur, on peut vouloir ignorer les valeurs précédent start_timestamp
		# todo : uniquement le vrai start_timestamp, pas le min, il peut être en plein dans l'interval de l'exp si redemarrage
		if value_start_zero:
			raw_data[service] = raw_data.apply(substract, axis=1, key=service, value=pandas.Series.min(raw_data[service]))

		if i == 0:
			# la première série de donnée initialise datas
			datas["timestamp"] = raw_data["timestamp"]
			datas[service] =  raw_data[service]
		elif service in datas.columns:
			datas_min_timestamp = datas["timestamp"].min()
			datas_max_timestamp = datas["timestamp"].max()
			datas = pandas.merge(datas, raw_data, how='outer', on='timestamp', suffixes=(None, f"_{i}"))
			# print(datas)
			if gauge:
				# use the data from the correct series no matter the read order 
				def get_correct_row(row):
					if ((
							datas_min_timestamp < raw_data["timestamp"].min() and 
							row["timestamp"] < raw_data["timestamp"].min()
						)
						or 
						(
							raw_data["timestamp"].min() < datas_min_timestamp and 
							row["timestamp"] > datas_min_timestamp
						)
						or
						(
							raw_data["timestamp"].min() == datas_min_timestamp and
							raw_data["timestamp"].max() < datas_max_timestamp
						)):

						return row[service]
					else:
						return row[f"{service}_{i}"]
				
				datas[service] = datas.apply(get_correct_row, axis=1)
			else:
				datas[service] = datas[service].add(datas[f"{service}_{i}"], fill_value=0)
			datas = datas.drop(f"{service}_{i}", axis=1)
		else:
			datas = pandas.merge(datas, raw_data, how='outer', on='timestamp', suffixes=(None, None))
		i += 1
		# print(datas)
	return datas


def plot_from_datas(datas, plots_folder_path, title, metric_name, ylab="", custom_y_breaks_func=False, custom_y_label_func=False, transform=False, select=False, serviceFromPod=None, subtitle="no subtitle", logScale=False, ymin=0, ymax=False, additionnal_serie=False, additionnal_serie_key=None, caption=False, hLine=False):
	"""
	TODO
	"""
	if ylab == "":
		ylab = metric_name
	# on veut un temps qui commence à zéro
	datas["timestamp"] = datas.apply(substract, axis=1, key="timestamp",value=(pandas.Series.min(datas["timestamp"])+60))

	if transform:
		datas = transform(datas)
	# datas = datas.drop(datas[datas.timestamp < 0].index)

	if select:
		datas = select(datas)

	# print(datas)
	datas = datas.shift(-60)
	# print(datas)

	if additionnal_serie_key:
		datas[additionnal_serie_key] = additionnal_serie


	# reforme le tableau de donnée pour que toutes les valeurs soit dans la même colonne, distinguée par une nouvelle colonne service
	datas = datas.melt(id_vars="timestamp", var_name="Pod", value_name=metric_name)

	# add a service column, different than pod
	if serviceFromPod:
		datas["Service"] = datas.apply(serviceFromPod, axis=1, key="Pod")
	else:
		datas["Service"] = datas["Pod"]

	symbol_interval = round(pandas.Series.max(datas["timestamp"]) / 10)
	datas_thinned = pandas.DataFrame()
	for data_idx in datas.index:
		if datas.loc[data_idx]["timestamp"] % symbol_interval == 0:
			datas_thinned = pandas.concat([datas_thinned, datas.loc[[data_idx]]])

	plot = (
	ggplot(datas)
	+ aes(x='timestamp', y=metric_name, group="Pod", ymin=ymin)
	+ geom_point(data=datas_thinned, mapping=aes( x="timestamp", y=metric_name, shape="Service", color="Service"), size=5, stroke=1, fill="#00000000", show_legend={"color": False})
	+ geom_line(mapping=aes(color="Service"), size=0.8)
	+ labs(x="Time", y=ylab, color="Service", title=title, subtitle=subtitle)
	+ scale_x_continuous(breaks=custom_breaks_by_minutes, labels=custom_labels_s)
	+ theme(legend_box="horizontal", legend_key_size=10)
	)

	if ymax:
		plot = plot + aes(ymax=ymax)

	if hLine:
		plot = plot + geom_hline(yintercept=hLine, color='gray', linetype="dashed")

	if logScale and custom_y_label_func:
		if custom_y_breaks_func:
			plot = plot + scale_y_log10(breaks=custom_y_breaks_func, labels=custom_y_label_func)
		else:
			plot = plot + scale_y_log10(labels=custom_y_label_func)
	elif logScale and not custom_y_label_func:
		if custom_y_breaks_func:
			plot = plot + scale_y_log10(breaks=custom_y_breaks_func)
		else:
			plot = plot + scale_y_log10()
	elif not logScale and custom_y_label_func:
		if custom_y_breaks_func:
			plot = plot + scale_y_continuous(breaks=custom_y_breaks_func, labels=custom_y_label_func)
		else:
			plot = plot + scale_y_continuous(labels=custom_y_label_func)
	elif not logScale and not custom_y_label_func:
		if custom_y_breaks_func:
			plot = plot + scale_y_continuous(breaks=custom_y_breaks_func)
		else:
			plot = plot + scale_y_continuous()

	if caption:
		plot = plot + labs(caption=caption) + theme(plot_caption=element_text(color="grey", size=5, hjust=0))

	plot.save(filename=f"{metric_name}.svg", path=plots_folder_path, width=10, height=4.8)


def plot_call_graph(data_folder, plots_folder_path, title, db_id, filters=[]):

	folders = ["requests"]
	# folders = ["requests", "tcp_received_bytes", "tcp_sent_bytes"]

	call_graph = {}
	for folder in folders:
		start_files_list = glob(f"{data_folder}/{folder}/start/*/*.json")
		end_files_list = glob(f"{data_folder}/{folder}/end/*/*.json")
		

		for data_file_path in end_files_list:
			with open(data_file_path, 'r') as file:
				data_file = json.load(file)
			start_service = data_file['metric']['source_workload']
			end_service = data_file['metric']['destination_workload']

			if folder == "tcp_sent_bytes":
				start_service = data_file['metric']['destination_workload']
				end_service = data_file['metric']['source_workload']

			if not start_service in call_graph:
				call_graph[start_service] = {}

			call_graph[start_service][end_service] = int(data_file['values'][0][1])
			# print(start_service, end_service, call_graph[start_service][end_service])
		
		for data_file_path in start_files_list:
			with open(data_file_path, 'r') as file:
				data_file = json.load(file)
			start_service = data_file['metric']['source_workload']
			end_service = data_file['metric']['destination_workload']

			if folder == "tcp_sent_bytes":
				start_service = data_file['metric']['destination_workload']
				end_service = data_file['metric']['source_workload']

			if not start_service in call_graph:
				print("ERROR : the start service should already exist. If it's there at the start, it must be there at the end.", start_service)
				call_graph[start_service] = {}
				call_graph[start_service][end_service] = -1
			else:
				if not end_service in call_graph[start_service]:
					call_graph[start_service][end_service] = -1
					print("ERROR : the end service should already exist. If it's there at the start, it must be there at the end.", end_service)
				else:
					call_graph[start_service][end_service] = call_graph[start_service][end_service] - int(data_file['values'][0][1])
					if call_graph[start_service][end_service] < 0:
						print("ERROR : the request can't be negative", start_service,  end_service)

			# print(start_service, end_service, call_graph[start_service][end_service])
	

	# remove disconnected service/db couple
	for key in list(call_graph.keys()):
		if key == "unknown": # ignore root
			continue
		# print("checking ", key)
		found = False
		for start, v in call_graph.items():
			if db_id in start:
				# print("mongo in ", start)
				continue
			for end, value in v.items():
				if end == key and value > 0:
					found = True
					break
			if found:
				break
		if not found:
			# print("removing ", key)
			del call_graph[key]

	# apply filters
	for key in list(call_graph.keys()):
		for filter in filters:
			if filter in key:
				del call_graph[key]
	
	for start, v in call_graph.items():
		for key in list(v.keys()):
			for filter in filters:
				if filter in key:
					del call_graph[start][key]


	dot_graph = pydot.Dot("call_graph", graph_type="digraph", bgcolor="white", label=title, fontsize=20, ratio=0.56) #, rankdir="LR"


	for start, v in call_graph.items():
		for end, value in v.items():
			if value != 0:
				# print(start, end, value)
				dot_graph.add_node(pydot.Node(start))
				dot_graph.add_node(pydot.Node(end))
				# if db_id in start or db_id in end:
				# 	value, symbol = scale_value(value)
				# 	value = str(round(value, 2)) + " " + symbol + "B"
				dot_graph.add_edge(pydot.Edge(start,end,label=value))

	dot_graph.write_pdf(f"{plots_folder_path}/call_graph.pdf")
	dot_graph.write_svg(f"{plots_folder_path}/call_graph.svg")

	return call_graph, dot_graph

def custom_rolling_average_60s(data):
	def cut_below_zero(row, key):
		return row[key] if row[key] > 0 else 0

	x = 20
	y = 5

	data = rolling_average_X_Y(data, x, y)

	for column in data.columns:
		if column == "timestamp":
			continue
		data[column] = data.apply(cut_below_zero, axis=1, key=column)
	return data

def cpu_to_pct(data, CPU_LIMIT):
	for column in data.columns:
		if column == "timestamp":
			continue
		else:
			for i in range(len(data)):
				data.loc[i, column] = (data.loc[i, column] / CPU_LIMIT) * 100
	return data

def plot_cpu_per_replicas(global_result_folder_path, plots_folder_path, serviceFromPod, subtitle, CPU_LIMIT, select=False, caption=False, filter=False):
	try:
		files_list = glob(f"{global_result_folder_path}/data/container_cpu_usage_seconds_total/*.json")

		if filter:
			files_list = filter(files_list)

		datas = get_datas_with_metric_per_key(
			files_list=files_list,
			key='pod',
			value_start_zero=True,
			gauge=False
		)

		# print(datas.head())

		def transform_and_pct(data):
			data = custom_rolling_average_60s(data)
			data = cpu_to_pct(data, CPU_LIMIT)
			return data


		plot_from_datas(
			datas=datas,
			plots_folder_path=plots_folder_path,
			title=f"CPU/s per pod - rolling avg",
			metric_name="container_cpu_usage_seconds_total_avg",
			ylab="CPU/s",
			transform=transform_and_pct,
			select=select,
			caption=caption,
			custom_y_breaks_func=custom_breaks_rps,
			custom_y_label_func=custom_labels_pct,
			serviceFromPod=serviceFromPod,
			subtitle=subtitle
		)
	except:
		print("ERROR CPU/replica plot")
		traceback.print_exc()

def plot_cpu_per_service(global_result_folder_path, plots_folder_path, serviceFromPod, subtitle, CPU_LIMIT, select=False, caption=False, filter=False):
	try:
		files_list = glob(f"{global_result_folder_path}/data/container_cpu_usage_seconds_total/*.json")

		if filter:
			files_list = filter(files_list)

		datas = get_datas_with_metric_per_key(
			files_list=files_list,
			key='container',
			value_start_zero=True,
			gauge=False
		)

		def transform_and_pct(data):
			data = custom_rolling_average_60s(data)
			data = cpu_to_pct(data, CPU_LIMIT)
			return data

		plot_from_datas(
			datas=datas,
			plots_folder_path=plots_folder_path,
			title=f"CPU/s per service - rolling avg",
			metric_name="cpu_per_service",
			ylab="CPU/s",
			transform=transform_and_pct,
			select=select,
			caption=caption,
			custom_y_breaks_func=custom_breaks_rps,
			custom_y_label_func=custom_labels_pct,
			serviceFromPod=serviceFromPod,
			subtitle=subtitle
		)
	except:
		print("ERROR CPU/service plot")
		traceback.print_exc()

def plot_avg_cpu_per_replicas(global_result_folder_path, plots_folder_path, serviceFromPod, subtitle, CPU_LIMIT, select=False, caption=False, filter=False, transform=False):
	def cpu_per_replicas_rolling_average(data):
		for column in data.columns:
			if column == "timestamp":
				continue
			data[column] = data[column].rolling(10, min_periods=0).mean()
		data = cpu_to_pct(data, CPU_LIMIT)
		return data
	
	try:
		files_list = glob(f"{global_result_folder_path}/data/cpu_per_replicas/*.json")

		if filter:
			files_list = filter(files_list)

		datas = get_datas_with_metric_per_filename(
			files_list=files_list,
			value_start_zero=False,
			gauge=True
		)
		plot_from_datas(
			datas=datas,
			plots_folder_path=plots_folder_path,
			title="Average CPU/s per replicas - rate 6s",
			metric_name="avg_cpu_per_replicas",
			ylab="CPU/s",
			transform=cpu_per_replicas_rolling_average,
			select=select,
			caption=caption,
			custom_y_breaks_func=custom_breaks_rps,
			custom_y_label_func=custom_labels_pct,
			serviceFromPod=serviceFromPod,
			subtitle=subtitle
		)
	except:
		print("ERROR avg CPU/replica plot")
		traceback.print_exc()

def plot_wrk_requests(global_result_folder_path, plots_folder_path, load_filename, subtitle, caption):
	try:
		csv_wrk_request = pandas.read_csv(f"{global_result_folder_path}/data/requests_stats.csv", header=0)#, usecols=["timestamp", "requests_sent"])
		csv_wrk_request["timestamp"] = csv_wrk_request.apply(substract, axis=1, key="timestamp",value=(pandas.Series.min(csv_wrk_request["timestamp"])))

		csv_wrk_request["B_sent"] = csv_wrk_request["requests_sent"].diff()
		csv_wrk_request["C_sent_roll10"] = csv_wrk_request["requests_sent"].diff().rolling(10, min_periods=0).mean()

		csv_wrk_request["timeout_10s"] = csv_wrk_request["requests_sent"]
		csv_wrk_request.loc[0, "timeout_10s"] = 0
		csv_wrk_request["request_shift"] = csv_wrk_request["requests_sent"].shift(periods=10, fill_value=0)
		timeoutAccum = 0
		for i in range(1, len(csv_wrk_request)):
			csv_wrk_request.loc[i, "timeout_10s"] = (csv_wrk_request.loc[i, "request_shift"] - csv_wrk_request.loc[i, "responses"]) - timeoutAccum
			if csv_wrk_request.loc[i, "timeout_10s"] <= 0:
				csv_wrk_request.loc[i, "timeout_10s"] = 0
			timeoutAccum += csv_wrk_request.loc[i, "timeout_10s"]
		# print(csv_wrk_request.to_string())

		csv_wrk_request["D_timeout_roll10"] = csv_wrk_request["timeout_10s"].rolling(10, min_periods=0).mean()
		csv_wrk_request = csv_wrk_request.drop("timeout_10s", axis=1)

		csv_wrk_request = csv_wrk_request.drop("request_shift", axis=1)

		csv_wrk_request["responses"] = csv_wrk_request["responses"].diff().rolling(10, min_periods=0).mean()
		csv_wrk_request["1xx"] = csv_wrk_request["1xx"].diff().rolling(10, min_periods=0).mean()
		csv_wrk_request["2xx"] = csv_wrk_request["2xx"].diff().rolling(10, min_periods=0).mean()
		csv_wrk_request["3xx"] = csv_wrk_request["3xx"].diff().rolling(10, min_periods=0).mean()
		csv_wrk_request["4xx"] = csv_wrk_request["4xx"].diff().rolling(10, min_periods=0).mean()
		csv_wrk_request["5xx"] = csv_wrk_request["5xx"].diff().rolling(10, min_periods=0).mean()

		csv_wrk_request = csv_wrk_request.drop("requests_sent", axis=1)
		csv_wrk_request = csv_wrk_request.drop("timeout", axis=1)

		csv_rate_df = pandas.read_csv(f"{global_result_folder_path}/ressources/{load_filename}", header=None, names=["timestamp", "target_rate"])
		csv_rate_df["timestamp"] = csv_rate_df.apply(substract, axis=1, key="timestamp",value=(pandas.Series.min(csv_rate_df["timestamp"])))

		csv_wrk_request["A_requested"] = csv_rate_df["target_rate"]

		csv_wrk_request_melted = csv_wrk_request.melt(id_vars="timestamp", var_name="Source", value_name="request_rate")

		datas_thinned = pandas.DataFrame()
		symbol_interval = round(pandas.Series.max(csv_wrk_request_melted["timestamp"]) / 10)
		for data_idx in csv_wrk_request_melted.index:
			if csv_wrk_request_melted.loc[data_idx]["timestamp"] % symbol_interval == 0:
				datas_thinned = pandas.concat([datas_thinned, csv_wrk_request_melted.loc[[data_idx]]])

		plot = (
			ggplot(csv_wrk_request_melted)
			+ aes(x='timestamp', y="request_rate", group="Source", color="Source", ymin=0)
			+ geom_line(size=0.8)
			+ geom_point(data=datas_thinned, mapping=aes( x="timestamp", y="request_rate", shape="Source", color="Source"), size=5, stroke=1, fill="#00000000")
			+ labs(x="Time (s)", y="Requests/s", title="Wrk - Requests requested, sent and responded", subtitle=subtitle)
			+ scale_x_continuous(breaks=custom_breaks_by_minutes, labels=custom_labels_s)
			+ scale_y_continuous(breaks=custom_breaks_rps, labels=custom_labels_value)
		)
		plot = plot + labs(caption=caption) + theme(plot_caption=element_text(color="grey", size=5, hjust=0))

		plot.save(filename="wrk_requests.svg", path=plots_folder_path, width=10, height=4.8)
	except:
		print("ERROR wrk plot")
		traceback.print_exc()

def plot_latency(global_result_folder_path, plots_folder_path, serviceFromPod, subtitle, MAX_LATENCY, select=False, caption=False, filter=False, RATIO=False):
	try:
		files_list = glob(f"{global_result_folder_path}/data/latency/*.json")

		if filter:
			files_list = filter(files_list)

		data = get_datas_with_metric_per_filename(
			files_list=files_list,
			value_start_zero=False,
			gauge=True
		)

		plot_from_datas(
			datas=data,
			plots_folder_path=plots_folder_path,
			title="Average latency per service - rate 6s",
			metric_name="avg_latency_log",
			ylab="Latency",
			logScale=True,
			ymax=MAX_LATENCY,
			hLine=MAX_LATENCY,
			select=select,
			custom_y_breaks_func=custom_breaks_ms_log,
			custom_y_label_func=custom_labels_ms,
			serviceFromPod=serviceFromPod,
			caption=caption,
			subtitle=subtitle
		)
		plot_from_datas(
			datas=data,
			plots_folder_path=plots_folder_path,
			title="Average latency per service - rate 6s",
			metric_name="avg_latency_linear",
			ylab="Latency",
			logScale=False,
			ymax=MAX_LATENCY,
			hLine=MAX_LATENCY,
			select=select,
			custom_y_breaks_func=custom_breaks_rps,
			custom_y_label_func=custom_labels_ms,
			serviceFromPod=serviceFromPod,
			caption=caption,
			subtitle=subtitle
		)

		if RATIO:
			for column in data.columns:
				if column == "timestamp":
					continue
				else:
					for service, ratio in RATIO.items():
						# print(service, column)
						if service == column:
							data[column] = data[column] * ratio
							break

			plot_from_datas(
				datas=data,
				plots_folder_path=plots_folder_path,
				title="Average latency per service per request- rate 6s",
				metric_name="avg_latency_log_ratio",
				ylab="Latency",
				logScale=True,
				ymax=MAX_LATENCY,
				hLine=MAX_LATENCY,
				select=select,
				custom_y_breaks_func=custom_breaks_ms_log,
				custom_y_label_func=custom_labels_ms,
				serviceFromPod=serviceFromPod,
				caption=caption,
				subtitle=subtitle
			)

	except:
		print("ERROR latency plot")
		traceback.print_exc()

	try:
		# 90 percentile
		files_list = glob(f"{global_result_folder_path}/data/latency_90_percentile/*.json")

		if filter:
			files_list = filter(files_list)

		data = get_datas_with_metric_per_filename(
			files_list=files_list,
			value_start_zero=False,
			gauge=True
		)
		plot_from_datas(
			datas=data,
			plots_folder_path=plots_folder_path,
			title="90-percentile latency per service - rate 6s",
			metric_name="90p_latency_linear",
			ylab="Latency",
			logScale=False,
			ymax=MAX_LATENCY,
			hLine=MAX_LATENCY,
			select=select,
			custom_y_breaks_func=custom_breaks_rps,
			custom_y_label_func=custom_labels_ms,
			serviceFromPod=serviceFromPod,
			caption=caption,
			subtitle=subtitle
		)

		# 95 percentile
		files_list = glob(f"{global_result_folder_path}/data/latency_95_percentile/*.json")

		if filter:
			files_list = filter(files_list)

		data = get_datas_with_metric_per_filename(
			files_list=files_list,
			value_start_zero=False,
			gauge=True
		)
		plot_from_datas(
			datas=data,
			plots_folder_path=plots_folder_path,
			title="95-percentile latency per service - rate 6s",
			metric_name="95p_latency_linear",
			ylab="Latency",
			logScale=False,
			ymax=MAX_LATENCY,
			hLine=MAX_LATENCY,
			select=select,
			custom_y_breaks_func=custom_breaks_rps,
			custom_y_label_func=custom_labels_ms,
			serviceFromPod=serviceFromPod,
			caption=caption,
			subtitle=subtitle
		)

		# 99 percentile
		files_list = glob(f"{global_result_folder_path}/data/latency_99_percentile/*.json")

		if filter:
			files_list = filter(files_list)

		data = get_datas_with_metric_per_filename(
			files_list=files_list,
			value_start_zero=False,
			gauge=True
		)
		plot_from_datas(
			datas=data,
			plots_folder_path=plots_folder_path,
			title="99-percentile latency per service - rate 6s",
			metric_name="99p_latency_linear",
			ylab="Latency",
			logScale=False,
			ymax=MAX_LATENCY,
			hLine=MAX_LATENCY,
			select=select,
			custom_y_breaks_func=custom_breaks_rps,
			custom_y_label_func=custom_labels_ms,
			serviceFromPod=serviceFromPod,
			caption=caption,
			subtitle=subtitle
		)
	except:
		print("ERROR latency percentile plot")
		traceback.print_exc()

def plot_replicas_spec_and_ready(plots_folder_path, replicas_datas, replicas_ready_datas, replicas_datas_thinned, replicas_ready_datas_thinned, subtitle, caption):
	plot = (
	ggplot()
	# + aes(x='timestamp', y=metric_name, group="Pod", ymin=ymin)
	+ geom_point(data=replicas_datas_thinned, mapping=aes( x="timestamp", y="kube_deployment_spec_replicas", shape="Service", color="Service"), size=5, stroke=1, fill="#00000000", show_legend={"color": False}, alpha=0.5)
	+ geom_point(data=replicas_ready_datas_thinned, mapping=aes( x="timestamp", y="kube_deployment_status_replicas_ready", shape="Service", color="Service"), size=5, stroke=1, fill="#00000000", show_legend={"color": False})
	+ geom_line(data=replicas_datas, mapping=aes(x='timestamp', y="kube_deployment_spec_replicas", group="Pod", ymin=0, color="Service"), linetype="dashed", size=0.8)
	+ geom_line(data=replicas_ready_datas, mapping=aes(x='timestamp', y="kube_deployment_status_replicas_ready", group="Pod", ymin=0, color="Service"), size=0.8)
	+ labs(x="Time", y="Replicas", color="Service", title="Replicas - count per service", subtitle=subtitle)
	+ scale_x_continuous(breaks=custom_breaks_by_minutes, labels=custom_labels_s)
	+ theme(legend_box="horizontal", legend_key_size=10)
	+ scale_y_continuous(breaks=custom_breaks_rps)
	)
	plot = plot + labs(caption=caption) + theme(plot_caption=element_text(color="grey", size=5, hjust=0))

	plot.save(filename="replicas.svg", path=plots_folder_path, width=10, height=4.8)

def plot_latency_histogram(global_result_folder_path, plots_folder_path, FRONTEND, MAX_LATENCY):

	try:
		files_list = glob(f"{global_result_folder_path}/data/latency_buckets/{FRONTEND}/*.json")

		# get data for all timestamp by le
		latency_buckets = get_datas_with_metric_per_key(
			files_list=files_list,
			key="le",
			value_start_zero=True,
			gauge=False
		)

		# print(latency_buckets)
		# print(latency_buckets.index.max())

		# get only the last timestamp and melt the data
		latency_buckets_thinned = pandas.DataFrame()
		i=0
		for column in latency_buckets.columns:
				if column == "timestamp":
					continue
				else:
					latency_buckets_thinned.loc[i, "bucket"] = float(column)
					latency_buckets_thinned.loc[i, "value"] = int(latency_buckets.loc[latency_buckets.index.max(), column])
					i = i + 1
		
		# sort by le
		latency_buckets_thinned.sort_values(by="bucket", inplace=True, ignore_index=True)
		# print(latency_buckets_thinned.to_string())
		
		# substract count from previous bucket
		for i in range(len(latency_buckets_thinned)-1, 0, -1):
			latency_buckets_thinned.loc[i, "value"] = latency_buckets_thinned.loc[i, "value"] - latency_buckets_thinned.loc[i-1, "value"]
		
		# merge buckets smaller than 100 with the one above
		for i in range(0, len(latency_buckets_thinned)):
			if latency_buckets_thinned.loc[i, "bucket"] < 100:
				latency_buckets_thinned.loc[i+1, "value"] = latency_buckets_thinned.loc[i+1, "value"] + latency_buckets_thinned.loc[i, "value"]
				latency_buckets_thinned.loc[i, "value"] = -1
		
		# merge buckets greater than 5s with the one before
		lastIndex = -1
		for i in range(len(latency_buckets_thinned)-1, 0, -1):
			if latency_buckets_thinned.loc[i, "bucket"] > 10000:
				latency_buckets_thinned.loc[i-1, "value"] = latency_buckets_thinned.loc[i-1, "value"] + latency_buckets_thinned.loc[i, "value"]
				latency_buckets_thinned.loc[i, "value"] = -1
				lastIndex = i
		if lastIndex > 0:
			latency_buckets_thinned.loc[lastIndex-1, "bucket"] = float('INF')

		# remove empty bucket
		latency_buckets_thinned = latency_buckets_thinned[latency_buckets_thinned["value"] >= 0]

		# reset index
		latency_buckets_thinned.reset_index(drop=True, inplace=True)
		print(latency_buckets_thinned.to_string())


		# rename bucket to proper labels
		# for i in range(len(latency_buckets_thinned)-1,-1,-1):
		# 	latency_buckets_thinned.loc[i, "bucket"] = f"{value_to_labels_ms(int(latency_buckets_thinned.loc[i, 'bucket']))}"
			# if i == 0:
			# 	latency_buckets_thinned.loc[i, "bucket"] = f"0-{value_to_labels_ms(int(latency_buckets_thinned.loc[i, "bucket"]))}"
			# else:
			# 	latency_buckets_thinned.loc[i, "bucket"] = f"{value_to_labels_ms(int(latency_buckets_thinned.loc[i-1, "bucket"]))}-{value_to_labels_ms(int(latency_buckets_thinned.loc[i, "bucket"]))}"
		
		# print(latency_buckets_thinned.to_string())

		latency_buckets_thinned = latency_buckets_thinned.assign(bucket = pandas.Categorical(latency_buckets_thinned.bucket, latency_buckets_thinned.bucket))

		# print(latency_buckets_thinned.to_string())

		plot = (
			ggplot(latency_buckets_thinned)
			+ aes(x="bucket", y="value")
			+ geom_col(position="dodge", just=1)
			+ labs(x="Latency Bucket", y="Request count", title="Request count per latency bucket")
			+ scale_y_continuous(breaks=custom_breaks_rps, labels=custom_labels_value)
			+ theme(axis_text_x=element_text(angle = 45, hjust = 1))
			# + geom_hline(yintercept=MAX_LATENCY, color='gray', linetype="dashed")
		)

		plot.save(filename=f"latency_histogram.svg", path=plots_folder_path, width=10, height=4.8)


	except:
		print("ERROR latency histogram plot")
		traceback.print_exc()

def plot_requests_repartition(global_result_folder_path, plots_folder_path, FRONTEND, MAX_LATENCY):
	try:
		files_list = glob(f"{global_result_folder_path}/data/latency_buckets/{FRONTEND}/*.json")

		# get data for all timestamp by le
		latency_buckets = get_datas_with_metric_per_key(
			files_list=files_list,
			key="le",
			value_start_zero=True,
			gauge=False
		)

		# print(latency_buckets)
		# print(latency_buckets.index.max())

		# get only the last timestamp and melt the data
		latency_buckets_thinned = pandas.DataFrame()
		i=0
		for column in latency_buckets.columns:
				if column == "timestamp":
					continue
				else:
					latency_buckets_thinned.loc[i, "bucket"] = float(column)
					latency_buckets_thinned.loc[i, "value"] = int(latency_buckets.loc[latency_buckets.index.max(), column])
					i = i + 1
		
		# sort by le
		latency_buckets_thinned.sort_values(by="bucket", inplace=True, ignore_index=True)
		# print(latency_buckets_thinned.to_string())
		
		# substract count from previous bucket
		for i in range(len(latency_buckets_thinned)-1, 0, -1):
			latency_buckets_thinned.loc[i, "value"] = latency_buckets_thinned.loc[i, "value"] - latency_buckets_thinned.loc[i-1, "value"]
		
		# merge buckets smaller than MAX_LATENCY with the one above
		for i in range(0, len(latency_buckets_thinned)):
			if latency_buckets_thinned.loc[i, "bucket"] < MAX_LATENCY:
				latency_buckets_thinned.loc[i+1, "value"] = latency_buckets_thinned.loc[i+1, "value"] + latency_buckets_thinned.loc[i, "value"]
				latency_buckets_thinned.loc[i, "value"] = 0
		
		# merge buckets greater than 5s with the one before
		for i in range(len(latency_buckets_thinned)-1, 0, -1):
			if latency_buckets_thinned.loc[i-1, "bucket"] > MAX_LATENCY:
				latency_buckets_thinned.loc[i-1, "value"] = latency_buckets_thinned.loc[i-1, "value"] + latency_buckets_thinned.loc[i, "value"]
				latency_buckets_thinned.loc[i, "value"] = 0

		# remove empty bucket
		latency_buckets_thinned = latency_buckets_thinned[latency_buckets_thinned["value"] > 0]

		# reset index
		latency_buckets_thinned.reset_index(drop=True, inplace=True)
		latency_buckets_thinned["bucket"] = latency_buckets_thinned["bucket"].astype('object')

		latency_buckets_thinned.loc[0, "bucket"] = "Below QOS"
		latency_buckets_thinned.loc[1, "bucket"] = "Above QOS"

		latency_buckets_thinned["value"] = latency_buckets_thinned["value"].astype('int')

		responses = latency_buckets_thinned.loc[0, "value"] + latency_buckets_thinned.loc[1, "value"]


		csv_wrk_request = pandas.read_csv(f"{global_result_folder_path}/data/requests_stats.csv", header=0)
		wrk_requests_sent = csv_wrk_request.loc[csv_wrk_request.index.max(), "requests_sent"]
		# wrk_responses = csv_wrk_request.loc[csv_wrk_request.index.max(), "responses"]
		
		latency_buckets_thinned.loc[2, "bucket"] = "No responses"
		latency_buckets_thinned.loc[2, "value"] = wrk_requests_sent - responses
		

		# print(latency_buckets_thinned.to_string(), responses, wrk_responses)

		for i in range(0, len(latency_buckets_thinned)):
			latency_buckets_thinned.loc[i, "x"] = ""
			latency_buckets_thinned.loc[i, "value"] = round((latency_buckets_thinned.loc[i, "value"] / wrk_requests_sent) * 100, 2)

		latency_buckets_thinned = latency_buckets_thinned.assign(x = pandas.Categorical(latency_buckets_thinned.x))
		latency_buckets_thinned = latency_buckets_thinned.assign(bucket = pandas.Categorical(latency_buckets_thinned.bucket, ["Below QOS", "Above QOS", "No responses"]))
		# latency_buckets_thinned = latency_buckets_thinned.assign(bucket = pandas.Categorical(latency_buckets_thinned.bucket, ["No responses", "Above QOS", "Below QOS"]))

		print(latency_buckets_thinned.to_string())

		plot = (
			ggplot(latency_buckets_thinned)
			+ aes(x="x", y="value", fill="bucket", label="value")
			+ geom_col(position=position_stack(reverse=True))
			+ geom_text(position=position_stack(reverse=True, vjust=0.5))
			+ labs(x="Scaling mode", y="Requests %", title="Requests repartition")
			+ scale_y_continuous(breaks=custom_breaks_rps, labels=custom_labels_pct)
			# + theme(axis_text_x=element_text(angle = 45, hjust = 1))
			+ scale_fill_manual(
				values={
					"Below QOS" : "#A1DEF0",
					"Above QOS" : "#BB458C",
					"No responses" : "#aaaaaa"
				}
			)
		)

		plot.save(filename=f"request_repartition.svg", path=plots_folder_path, width=10, height=4.8)

	except:
		print("ERROR request repartition plot")
		traceback.print_exc()