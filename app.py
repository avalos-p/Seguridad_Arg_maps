from functions.logger_sec import logger_project
import requests
import os

import pandas as pd
from decouple import config

# Variables
link = config("url")
print(link)
logger=logger_project('pryecto_seguridad')

def downloader(link):

    os.makedirs('raw_data/',exist_ok=True)

    try:
        # requesting file and saving

        req = requests.get(link)
        open('raw_data/datos_seguridad.csv','wb').write(req.content)
        logger.info('CSV file created')

    except:
        logger.debug('Warning, the request action could not be performed')
        pass

    return


def filtrado_general(df):

    #Creo una tabla general filtrada por los crimenes que seleccionamos para analizar

    filtro = [1,2,3,10,15,17,19,31]
    df['codigo_delito_snic_id'] = df['codigo_delito_snic_id'].astype(int)
    tabla_filtrada = df.loc[df['codigo_delito_snic_id'].isin(filtro),
    ['anio','provincia_id','provincia_nombre','codigo_delito_snic_id','codigo_delito_snic_nombre','cantidad_hechos','cantidad_victimas']]
    
    os.makedirs('data/',exist_ok=True)
    tabla_filtrada.to_csv('data/tabla_general.csv',index=False)
    
    logger.info('Tabla general filtrada por los crimenes seleccionados')

    return tabla_filtrada


def filtrado_provincial(filtrado_general,provincia):

    #Creo una tabla para cada provincia
    filtro = [provincia]
    tabla_filtrada = filtrado_general.loc[filtrado_general['provincia_nombre'].isin(filtro),
    ['anio','provincia_id','provincia_nombre','codigo_delito_snic_id','codigo_delito_snic_nombre','cantidad_hechos','cantidad_victimas']]
    
    tabla_filtrada.to_csv(f'data/{provincia}.csv', index=False)

    logger.info(f'Tabla {provincia} filtrada por los crimenes seleccionados')

    return tabla_filtrada



df = downloader(link)

df=pd.read_csv('raw_data/datos_seguridad.csv')
df['codigo_delito_snic_id'] = df['codigo_delito_snic_id'].astype(int)

nombres = df['provincia_nombre'].value_counts()
nombres = nombres.index.str.strip().tolist()
tabla_general=filtrado_general(df)


for provincia in nombres:
    filtrado_provincial(tabla_general,provincia)