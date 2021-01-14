
#leer el archivo y seleciono los campos que me interesan para guardar en un csv
import os, json
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt

def search_attribute(attribute_list):
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

	

def json_data_loader():
    # pd.set_option('display.max_columns', None)
    #target json files
    json_pattern = os.path.join('*.jsonl')
    file_list = glob.glob(json_pattern)
    #open a list
    terrains = []
    for file in file_list:
    	print(f"estoy por abrir este archivo --> {file}")
    	with open(file, 'r') as j:
        	json_data = json.load(j)#, encoding='utf8'
        	
        	for i in range(len(json_data.keys())-2):
        		if json_data['results']:
		        	for i,result in enumerate(json_data['results']):
		        		row = []
		        		print(f"resultado Nº {i}")
		        		# print((result['id'], result['title'], result['price']))
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
		        		# city_name = result['location']['city']['name']
		        		# state_name = result['location']['state']['name']
		        		country_id = result['location']['country']['id']
		        		country_name = result['location']['country']['name']
		        		latitude = result['location']['latitude']
		        		longitude = result['location']['longitude']
		        		size, size_num, size_unit = search_attribute(result['attributes'])

			        	row = [_id, title, price, currency_id, stop_time, permalink, state_name, city_name, address_line, neighborhood_name, country_id, country_name, latitude, longitude,size, size_num, size_unit]
		        		terrains.append(row)
    return terrains


os.chdir('./data')
data = json_data_loader()


df = pd.DataFrame(data)
df.to_csv('terrain_detail.csv', index=False)
