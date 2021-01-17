
#leer el archivo y seleciono los campos que me interesan para guardar en un csv
import os, json
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import logging


logging.basicConfig(filename='json_reader.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def search_attribute(attribute_list):
	"""
	searches for size, size_num and size units in attributes.
	"""
	size, size_num, size_unit = 0,0,None
	for ele in attribute_list:
		if ele['id'] == 'TOTAL_AREA' or ele['id'] == 'MAX_TOTAL_AREA' :
			try:
				size = ele['value_name']
				size_num = ele['value_struct']['number']
				size_unit = ele['value_struct']['unit']
			except:
				size = 0
				size_num = 0
				size_unit = None
			break
		else:
			size = 0
			size_num = 0
			size_unit = None
	return size, size_num, size_unit

	

def json_data_loader(file_list):
	"""
	list file_list : 
	extracts data of interest from every json file in the list;
	returns a list of rows with every record
	"""
	terrains = list()
	for file in file_list:
		logging.info(f"Opening a file: {file}")
		with open(file, 'r') as j:
			json_data = json.load(j)#, encoding='utf8'
			for i in range(len(json_data.keys())-2):
				if json_data['results']:
					for i,result in enumerate(json_data['results']):
						row = []
						_id = result['id']
						title = result['title']
						price = result['price']
						currency_id = result['currency_id']
						stop_time = result['stop_time']
						permalink = result['permalink']
						state_name = result['address']['state_name']
						city_name = result['address']['city_name']
						address_line = result['location']['address_line']
						neighborhood_name =  result['location']['neighborhood']['name']
						country_id = result['location']['country']['id']
						country_name = result['location']['country']['name']
						latitude = result['location']['latitude']
						longitude = result['location']['longitude']
						size, size_num, size_unit = search_attribute(result['attributes'])
						row = [_id, title, price, currency_id, stop_time, permalink, state_name, city_name, address_line, neighborhood_name, country_id, country_name, latitude, longitude,size, size_num, size_unit]
						terrains.append(row)
	return terrains


def get_directories_in_path(directory="."):
	"""
	returns a list of the folders names in the argument dir
	default --> cwd() e.g. "." 
	"""
	directories = [x[0] for x in os.walk(directory)]
	directories.remove('.')
	return directories


def get_json_files_in_cwd():
	json_pattern = os.path.join('*.jsonl')
	file_list = glob.glob(json_pattern)
	return file_list



#open data dir
os.chdir('./data/json')
#open each file, extract usefull information and create a csv
for d in get_directories_in_path():
	os.chdir(d)
	#define date for new directory 
	fecha = d[-10:]
	logging.info(f"Current working directory: { os.getcwd()}")
	#read all files in directory
	json_file_list = get_json_files_in_cwd()
	data = json_data_loader(json_file_list)
	#create csv
	df = pd.DataFrame(data)
	df.to_csv('~/documents/landlord/data/csv/' + fecha + '.csv', index=False)
