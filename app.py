#Importing libreries and modules
from functions.logger_sec import logger_project
import requests
import os

import pandas as pd
from decouple import config

#Variables
link = config("url")
print(link)
#Creating a logger instance for the project 
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

#Creating a table with just important data, in this case just by selected crimes data 
def filtrado_general(df):


    filtro = [1,2,3,10,15,17,19,31]
    df['codigo_delito_snic_id'] = df['codigo_delito_snic_id'].astype(int)
    tabla_filtrada = df.loc[df['codigo_delito_snic_id'].isin(filtro),
    ['anio','provincia_id','provincia_nombre','codigo_delito_snic_id','codigo_delito_snic_nombre','cantidad_hechos','cantidad_victimas']]
    
    os.makedirs('data/',exist_ok=True)
    tabla_filtrada.to_csv('data/tabla_general.csv',index=False)
    
    logger.info('Tabla general filtrada por los crimenes seleccionados')

    return tabla_filtrada


#Creating a df with each province
def filtrado_provincial(filtrado_general,provincia):

    filtro = [provincia]
    tabla_filtrada = filtrado_general.loc[filtrado_general['provincia_nombre'].isin(filtro),
    ['anio','provincia_id','provincia_nombre','codigo_delito_snic_id','codigo_delito_snic_nombre','cantidad_hechos','cantidad_victimas']]
    
    tabla_filtrada.to_csv(f'data/{provincia}.csv', index=False)

    logger.info(f'Tabla {provincia} filtrada por los crimenes seleccionados')

    return tabla_filtrada

#Creating a df with ranking H
def ranking_h(tabla_general,año):
    filtro_año = [año]
    filtro_delito_id = [1]
    tabla_filtrada = tabla_general.loc[tabla_general['anio'].isin(filtro_año),
    ['anio','provincia_id','provincia_nombre','codigo_delito_snic_id','codigo_delito_snic_nombre','cantidad_hechos','cantidad_victimas']]
    tabla_filtrada = tabla_filtrada.loc[tabla_filtrada['codigo_delito_snic_id'].isin(filtro_delito_id),
    ['anio','provincia_id','provincia_nombre','codigo_delito_snic_id','codigo_delito_snic_nombre','cantidad_hechos','cantidad_victimas']]
    
    
    
    tabla_filtrada = tabla_filtrada.groupby('provincia_nombre')['cantidad_hechos'].sum()
    tabla_filtrada = tabla_filtrada.sort_values(ascending=False)
    tabla_filtrada = pd.DataFrame({'provincia_nombre': tabla_filtrada.index, 'cantidad_hechos': tabla_filtrada.values})


    logger.info('Tabla ranking_h creada')

    return tabla_filtrada

#Creating a df with ranking R
def ranking_r(tabla_general,año):

    filtro_año = [año]
    filtro_delito_id = [15,17,19]
    tabla_filtrada = tabla_general.loc[tabla_general['anio'].isin(filtro_año),
    ['anio','provincia_id','provincia_nombre','codigo_delito_snic_id','codigo_delito_snic_nombre','cantidad_hechos','cantidad_victimas']]
    tabla_filtrada = tabla_filtrada.loc[tabla_filtrada['codigo_delito_snic_id'].isin(filtro_delito_id),
    ['provincia_nombre','cantidad_hechos']]
    

    tabla_filtrada = tabla_filtrada.groupby('provincia_nombre')['cantidad_hechos'].sum()
    tabla_filtrada = tabla_filtrada.sort_values(ascending=False)
    tabla_filtrada = pd.DataFrame({'provincia_nombre': tabla_filtrada.index, 'cantidad_hechos': tabla_filtrada.values})

    #tabla_filtrada.to_csv('data/ranking_rob.csv', index=False)
    logger.info(f'Tabla ranking_rob creada')

    return tabla_filtrada



df = downloader(link)

df=pd.read_csv('raw_data/datos_seguridad.csv')
df['codigo_delito_snic_id'] = df['codigo_delito_snic_id'].astype(int)

# reading population data
poblacion = pd.read_csv('raw_data/poblacion.csv')
poblacion['poblacion'] = poblacion['poblacion'].str.replace('.', '')
poblacion['poblacion'] = poblacion['poblacion'].astype(int)
poblacion['poblacion'] = poblacion['poblacion']/100000

nombres = df['provincia_nombre'].value_counts()
nombres = nombres.index.str.strip().tolist()
tabla_general=filtrado_general(df)

for provincia in nombres:
    filtrado_provincial(tabla_general,provincia)

ranking_h = ranking_h(tabla_general,2021)
tasa_h = pd.merge(poblacion, ranking_h, on="provincia_nombre")
tasa_h["tasa_de_homicidios_por_población"] = tasa_h["cantidad_hechos"] / tasa_h["poblacion"]
tasa_h.to_csv('data/ranking_h.csv', index=False)

ranking_r = ranking_r(tabla_general,2021)
tasa_r = pd.merge(poblacion, ranking_r, on="provincia_nombre")
tasa_r["tasa_de_robos_por_población"] = tasa_r["cantidad_hechos"] / tasa_r["poblacion"]
tasa_r.to_csv('data/ranking_rob.csv', index=False)
