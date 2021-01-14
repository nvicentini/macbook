import requests
import json
import time
import numpy as np
from pathlib import Path
import os
import jsonlines



def get_data(url,parameters):
    """
    recieves a date and runs an api request,
    if status is 200 then returns the 
    whole API answer 
    """
    #request
    response = requests.get(url, parameters)
    # print(response.headers['content-type'])#application/json;charset=UTF-8
    # print(response.encoding)#UTF-8
    if (response.status_code == 200):
        return response.json()


def get_regiones(url):
    response = requests.get(url)
    print(response.url)
    print(f"response status: {response.status_code}")
    if (response.status_code == 200):
        data = response.json()
    filters = data['available_filters']
    regiones = []
    for filter_ in filters:
        if filter_['id'] == 'state':
            for item in filter_['values']:
                regiones.append(item)
    # print(f"Regiones -->{regiones} ")
    return regiones


def get_localidades_por_region(url, regiones):
    dicc = {}
    for region in regiones:
        name_region = region['name']
        parameters = { 'state' : region['id'] }
        time.sleep(np.random.randint(5,10))
        response = requests.get(url, parameters)
        if (response.status_code == 200):
            data = response.json()
        filters = data['available_filters']
        localidades = []
        for filter_ in filters:
            if filter_['id'] == 'city':
                for item in filter_['values']:
                    localidades.append(item)
        # print(f"localidades: {localidades}")
        dicc[name_region] =  localidades

    return dicc

def get_tamanos(url, parameters):
    time.sleep(np.random.randint(2,5))
    response = requests.get(url, parameters)
    print(response.url)
    # print(f"response status: {response.status_code}")
    if (response.status_code == 200):
      data = response.json()
    filters = data['available_filters']
    tamano = []
    for filter_ in filters:
    #print(filter_)
      if filter_['id'] == 'TOTAL_AREA':
          for item in filter_['values']:
              tamano.append(item)
    return tamano


def save_json_to_fs(json_data, file_name):    
    """Saves json files to data directory
    recieves json data and a file name"""
    print(f"grabando archivo {file_name}")
    with open(file_name + '.json', 'w', encoding='utf8') as file:
        json.dump(json_data, file, ensure_ascii=False)
    print(f"archivo grabado")


def save_jsonlines_to_fs(json_data, file_name):    
    """Saves jsonlines files to data directory
    recieves json data and a file name"""
    print(f"grabando archivo en formato jsonlines: {file_name}")
    with jsonlines.open( file_name + '.jsonl', mode='w') as writer:
        writer.write(json_data)
    print(f"archivo grabado")

    


