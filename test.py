import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import geopandas as gps
import json
import seaborn as sns
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from folium.plugins import FastMarkerCluster
from folium.plugins.search import Search


st.set_page_config(layout="wide")

with open('RegionalCATI_geoJSON.json', encoding='utf-8') as f:
    regional_cati = json.load(f)


df_unidades = pd.read_csv('UnidadesSAA.csv', sep=";", encoding='latin1')


df_unidades['Lat'] = df_unidades['Lat'].str.replace(',','.').astype(np.float64)
df_unidades['Long'] = df_unidades['Long'].str.replace(',','.').astype(np.float64)


# Carregar a imagem da empresa
image = Image.open('banner_mapa.png')
st.image(image, use_column_width=False, width=1432)


## Plotando os dados no mapa

# Criando as variáveis para o controle de layer
Cati_regional = folium.FeatureGroup(name='CATI Regional', show=False)
Cda_regional = folium.FeatureGroup(name='CDA Regional', show=False)
UDA = folium.FeatureGroup(name='uda', show=True)
IDA = folium.FeatureGroup(name='Ida', show=True)
CA = folium.FeatureGroup(name='CA', show=True)
APTA = folium.FeatureGroup(name='APTA', show=True)
IAC = folium.FeatureGroup(name='IAC', show=True)
IB = folium.FeatureGroup(name='IB', show=True)
IEA = folium.FeatureGroup(name='IEA', show=True)
IP = folium.FeatureGroup(name='IP', show=True)
IZ = folium.FeatureGroup(name='IZ', show=True)
fg = folium.FeatureGroup(name="Unidades de Atendimento")



# Carregando o container de mapa com a localização da região
#folium_map = folium.Map(location=[-22.5579361,-45.9650196],zoom_start=7, tiles='cartodbpositron')

# Defina sua chave da API do Google Maps aqui
google_maps_api_key = "AIzaSyA4x9yznHUzuWPV4lcnKyxzaC6FQ9m1V5k"

# Load the map with Google Maps
folium_map = folium.Map(
    location=[-22.5579361, -45.9650196],
    zoom_start=7,
    tiles="CartoDB positron"
    
)


#Cria grupos para nomear as unidades geocodificadas pelo FastMarkerCluster
fast_uda = FastMarkerCluster((df_unidades.Lat.values,df_unidades.Long.values)).add_to(UDA)
fast_ida = FastMarkerCluster((df_unidades.Lat.values,df_unidades.Long.values)).add_to(IDA)
fast_CA = FastMarkerCluster((df_unidades.Lat.values,df_unidades.Long.values)).add_to(CA)
fast_apta = FastMarkerCluster((df_unidades.Lat.values,df_unidades.Long.values)).add_to(APTA)
fast_iac = FastMarkerCluster((df_unidades.Lat.values,df_unidades.Long.values)).add_to(IAC)
fast_ib = FastMarkerCluster((df_unidades.Lat.values,df_unidades.Long.values)).add_to(IB)
fast_iea = FastMarkerCluster((df_unidades.Lat.values,df_unidades.Long.values)).add_to(IEA)
fast_ip = FastMarkerCluster((df_unidades.Lat.values,df_unidades.Long.values)).add_to(IP)
fast_iz = FastMarkerCluster((df_unidades.Lat.values,df_unidades.Long.values)).add_to(IZ)


# Plotando os polígonos da regional Cati
folium.features.GeoJson(data=regional_cati,
                        name='CATI Regional',
                             style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5, 'border': '2px solid black'},
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['CATI_Regio'],
                        aliases=["CATI Regional:"],
                        localize=True,
                        sticky=False,
                        labels=True,
                        style="""
                            background-color: #F0EFEF;
                            border: 2px solid black;
                            border-radius: 3px;
                            box-shadow: 3px;
                        """,
                        max_width=800,),
                            highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
                        ).add_to(Cati_regional)



# Plotando as unidades
for _, v in df_unidades.iterrows():
    popup = """
    Unidade : <b>%s</b><br>
    Município : <b>%s</b><br>
    """ % (v['Unidade'],v['Município_base'])



    if v['Unidade'] =='IDA':
        folium.Marker(location=[v['Long'], v['Lat']],
                            icon = folium.Icon(icon = 'glyphicon glyphicon-info-sign',
                                               color="red",
                                               icon_color="white",
                                               prefix = "glyphicon"),
                            tooltip=popup
                            ).add_to(fast_ida)


    elif v['Unidade'] == 'UDA':
        folium.Marker(location=[v['Long'], v['Lat']],
                            icon = folium.Icon(icon = 'glyphicon glyphicon-info-sign',
                                               color="red",
                                               icon_color="white",
                                               prefix = "glyphicon"),
                            tooltip=popup
                            ).add_to(fast_uda)


    elif v['Unidade'] == 'CA':
        folium.Marker(location=[v['Long'], v['Lat']],
                            icon = folium.Icon(icon = 'glyphicon glyphicon-home',
                                               color="blue",
                                               icon_color="white",
                                               prefix = "glyphicon"),
                            tooltip=popup
                            ).add_to(fast_CA)

    elif v['Unidade'] == 'APTA':
        folium.Marker(location=[v['Long'], v['Lat']],
                            icon = folium.Icon(icon = 'glyphicon glyphicon-info-sign',
                                               color="red",
                                               icon_color="white",
                                               prefix = "glyphicon"),
                            tooltip=popup
                            ).add_to(fast_apta)

    elif v['Unidade'] == 'IAC':
        folium.Marker(location=[v['Long'], v['Lat']],
                            icon = folium.Icon(icon = 'glyphicon glyphicon-info-sign',
                                               color="red",
                                               icon_color="white",
                                               prefix = "glyphicon"),
                            tooltip=popup
                            ).add_to(fast_iac)

    elif v['Unidade'] == 'IB':
        folium.Marker(location=[v['Long'], v['Lat']],
                            icon = folium.Icon(icon = 'glyphicon glyphicon-info-sign',
                                               color="red",
                                               icon_color="white",
                                               prefix = "glyphicon"),
                            tooltip=popup
                            ).add_to(fast_ib)

    elif v['Unidade'] == 'IEA':
        folium.Marker(location=[v['Long'], v['Lat']],
                            icon = folium.Icon(icon = 'glyphicon glyphicon-info-sign',
                                               color="red",
                                               icon_color="white",
                                               prefix = "glyphicon"),
                            tooltip=popup
                            ).add_to(fast_iea)

    elif v['Unidade'] == 'IP':
        folium.Marker(location=[v['Long'], v['Lat']],
                            icon = folium.Icon(icon = 'glyphicon glyphicon-info-sign',
                                               color="red",
                                               icon_color="white",
                                               prefix = "glyphicon"),
                            tooltip=popup
                            ).add_to(fast_ip)

    elif v['Unidade'] == 'IZ':
        folium.Marker(location=[v['Long'], v['Lat']],
                            icon = folium.Icon(icon = 'glyphicon glyphicon-info-sign',
                                               color="red",
                                               icon_color="white",
                                               prefix = "glyphicon"),
                            tooltip=popup
                            ).add_to(fast_iz)




# Defina o título do menu lateral
st.sidebar.title("Menu Lateral")

# Adicione uma opção no menu lateral para controlar as camadas do mapa
if st.sidebar.checkbox("Controle de Camadas", True):

      # Personalize o estilo do menu
    st.markdown(
        """
        <style>
            .sidebar .sidebar-content {
                background-color: #48CC8D; /* Cor de fundo da barra lateral */
            }
            .sidebar .sidebar-content .block-container {
                background-color: #ffffff; /* Cor de fundo dos blocos do menu */
                color: #48CC8D; /* Cor do texto do menu */
            }
            .sidebar .sidebar-content .stCheckbox {
                color: #48CC8D; /* Cor da caixa de seleção */
            }
        </style>
        """,
        unsafe_allow_html=True
    )


    # Crie o controle de camadas e adicione-o ao mapa
    layer_options = ["CATI Regional", "CDA Regional", "CA", "IAC", "IEA", "IP", "IZ", "IDA", "UDA"]
    selected_layers = st.sidebar.multiselect("Selecione as camadas", layer_options, default=["CATI Regional", "CDA Regional", "CA"])
    for layer in selected_layers:
        if layer == "CATI Regional":
            folium_map.add_child(Cati_regional)
        elif layer == "CDA Regional":
            folium_map.add_child(Cda_regional)
        elif layer == "CA":
            folium_map.add_child(CA)
        elif layer == "IAC":
            folium_map.add_child(IAC)
        elif layer == "IEA":
            folium_map.add_child(IEA)
        elif layer == "IP":
            folium_map.add_child(IP)
        elif layer == "IZ":
            folium_map.add_child(IZ)
        elif layer == "IDA":
            folium_map.add_child(IDA)
        elif layer == "UDA":
            folium_map.add_child(UDA)



st_data = st_folium(folium_map, width=1980)
