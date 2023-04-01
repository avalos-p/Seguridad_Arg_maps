import folium
import pandas as pd
import os 
from functions.logger_sec import logger_project


logger=logger_project('pryecto_seguridad_mapas')


geojson_data = 'raw_data/ProvinciasArgentina.geojson'
raw_data_h = pd.read_csv('data/ranking_h.csv')
raw_data_rob = pd.read_csv('data/ranking_rob.csv')
logger.info('GeoJson and CSV files working')


data_h = raw_data_h[['provincia_nombre', 'tasa_de_homicidios_por_población']]
data_rob = raw_data_rob[['provincia_nombre', 'tasa_de_robos_por_población']]

geojson_data = geojson_data.replace("Tierra del Fuego","Tierra del Fuego, Antártida e Islas del Atlántico Sur")
geojson_data = geojson_data.replace("Capital Federal","Ciudad Autónoma de Buenos Aires")


h = folium.Map(location=[-38.4161, -63.6167], zoom_start=4)
r = folium.Map(location=[-38.4161, -63.6167], zoom_start=4)


def map_maker(h,geo_data,data,var):
    col = 'PuBu' 
    #col = 'PuBuGn'

    folium.Choropleth(
        geo_data=geo_data,
        name='choropleth',
        data=data,
        columns=['provincia_nombre', f'tasa_de_{var}_por_población'],
        key_on='feature.properties.nombre',
        fill_color=col,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'Tasa de {var} por Provincia por Población'
    ).add_to(h)

    folium.LayerControl().add_to(h)

    logger.info(f'{var} MAP created')

    h.save(f'maps/mapa_{var}.html')
    logger.info(f'{var} MAP saved')

    return

map_maker(r,geojson_data,data_rob,'robos')
map_maker(h,geojson_data,data_h,'homicidios')
