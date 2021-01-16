import requests
import json
import time
import numpy as np
from pathlib import Path
import os
from datetime import date
import jsonlines
import api_downloader as ad

today = date.today()
URL = "https://api.mercadolibre.com/sites/MLA/search?category=MLA1495"

#defino parametros del request
parameters = {
            'offset':  0,
            'since' : 'today'
            }

print(f"Parametros del request: {parameters}")
print(f"HAGO EL PRIMER REQUEST")
res = ad.get_data(URL, parameters)
print(today)

#create directory for saving data if not exists
if not os.path.exists('./data/json/' + str(today)):
    os.makedirs('./data/json/' + str(today))

#change to saving directory
os.chdir('./data/json/' + str(today))

#save file
ad.save_jsonlines_to_fs(res, str(today))

# check total records
print(f"el total de registros del dia {today}  es: {res['paging']['total']}")

#iterates over all the results pages
paginators = round(res['paging']['total']/50)+1
if paginators > 1:
    for j,offset in enumerate(range(1,min(paginators, 21))):
        # print(f"esto es i: {i} y esto es el offset: {offset}")
        parameters['offset']=offset*50
        data = ad.get_data(URL, parameters)
        ad.save_jsonlines_to_fs(data, str(today) + "_" + str(offset))

