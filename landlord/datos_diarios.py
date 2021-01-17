import requests
import json
import time
import numpy as np
from pathlib import Path
import os
from datetime import date
import jsonlines
import api_downloader as ad
import logging


logging.basicConfig(filename='datos_diarios.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

today = date.today()
URL = "https://api.mercadolibre.com/sites/MLA/search?category=MLA1495"

#defino parametros del request
parameters = {
            'offset':  0,
            'since' : 'today'
            }

#request
res = ad.get_data(URL, parameters)

# check total records
logging.info(f"el total de registros del dia {today}  es: {res['paging']['total']}")

#create directory for saving data if not exists
if not os.path.exists('./data/json/' + str(today)):
    os.makedirs('./data/json/' + str(today))

#change to saving directory
os.chdir('./data/json/' + str(today))

#save file
ad.save_jsonlines_to_fs(res, str(today))

#iterates over all the results pages
paginators = round(res['paging']['total']/50)+1
if paginators > 1:
    for j,offset in enumerate(range(1,min(paginators, 21))):
        # print(f"esto es i: {i} y esto es el offset: {offset}")
        parameters['offset']=offset*50
        data = ad.get_data(URL, parameters)
        ad.save_jsonlines_to_fs(data, str(today) + "_" + str(offset))

