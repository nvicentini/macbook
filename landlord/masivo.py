
import requests
import json
import time
import numpy as np
from pathlib import Path
import os
import api_downloader as ad

URL = "https://api.mercadolibre.com/sites/MLA/search?category=MLA1495"


print('Creando la carpeta Data')
# os.chdir('./data')
print("Buscando las regiones")
regiones = ad.get_regiones(URL)
localidades_por_region = ad.get_localidades_por_region(URL, regiones)
parameters = {}
for region in regiones:
    id_region = region['id']
    name_region = region['name']
    parameters['state'] = id_region
    localidades = localidades_por_region[name_region]
    print("esta es una vuelta")
    print(f"esta es la region : {name_region}")
    print(f"estas son las localidades: {localidades}")
    for localidad in localidades:
        id_localidad, name_localidad, q_results = localidad.values()
        parameters['city'] = id_localidad
        print(f"Procesando localidad {name_localidad}")
        parameters['offset'] = 0
        print(f"Parametros del request: {parameters}")
        print(f"HAGO EL PRIMER REQUEST")
        res = ad.get_data(URL, parameters)
        ad.save_json_to_fs(res, name_region + "_" + name_localidad)
        #check total records
        print(f"el total de registros de la localidad {name_region} es: {res['paging']['total']}")
        paginators = round(res['paging']['total']/50)+1
        if paginators > 1:
            for j,offset in enumerate(range(1,min(paginators, 21))):
                # print(f"esto es i: {i} y esto es el offset: {offset}")
                parameters['offset']=offset*50
                data = ad.get_data(URL, parameters)
                ad.save_json_to_fs(data, name_region + "_" + name_localidad + "_" + str(j) + "_" + str(offset))
