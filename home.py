import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import math


from joblib import load

from notebooks.src.config import DADOS_GEO_MEDIAN, DADOS_LIMPOS, MODELO_FINAL

@st.cache_data
def carregar_dados_limpos():
    return pd.read_parquet(DADOS_LIMPOS)

@st.cache_data
def carregar_dados_geo():
    return gpd.read_parquet(DADOS_GEO_MEDIAN)

@st.cache_resource
def carregar_modelo():
    return load(MODELO_FINAL)

df = carregar_dados_limpos()
gdf_geo = carregar_dados_geo()
modelo = carregar_modelo()


st.title("🏡 Previsão de Preços de Imóveis na Califórnia")

st.markdown("""
#### Este simulador faz parte do Projeto de previsão de preços de imóveis utilizando modelo de Machine Learning.

Desenvolvido por [Gabriel Duarte](https://www.linkedin.com/in/djgabriel93)

""")


#Variáveis de Localização

condados = list(gdf_geo["name"].sort_values()) #lista de condados
selecionar_condados = condados = st.selectbox(label = "Região (condado)", options = condados, index = 18) #seleção do condado

#cálculo de latitude e longitude
longitude = gdf_geo.query("name == @selecionar_condados")["longitude"].values
latitude = gdf_geo.query("name == @selecionar_condados")["latitude"].values

#pega a categoria no dataframe baseado no condado selecionado
ocean_proximity = gdf_geo.query("name == @selecionar_condados")["ocean_proximity"].values

#cálculo de renda média baseado no condado
median_income = gdf_geo.query("name == @selecionar_condados")["median_income"].values
median_income_cat = gdf_geo.query("name == @selecionar_condados")["median_income_cat"].values


#Variáveis do imóvel

#population, households é a média do condado
population_per_household = gdf_geo.query("name == @selecionar_condados")["population_per_household"].values
population = gdf_geo.query("name == @selecionar_condados")["population"].values
households = gdf_geo.query("name == @selecionar_condados")["households"].values

#usuário seleciona quantidade de quartos e comodos

rooms_per_household = st.select_slider("nº de cômodos", [2,3,4,5,6,7,8,9, 10])

if rooms_per_household == 2:
    maximo = 3
else:
    maximo = 1 + math.ceil(rooms_per_household/2)
    
bedrooms_per_household = st.select_slider("nº de quartos", list(np.arange(1, maximo)))

#Cálculos
total_bedrooms = bedrooms_per_household * households
total_rooms = rooms_per_household * households
bedrooms_per_room = total_bedrooms / total_rooms 
population_per_room = population / total_rooms


#usuário seleciona a idade do imóvel
housing_median_age = st.number_input("Idade do imóvel (em anos)", value = 41, min_value=1, max_value = 50) 




entrada_modelo = {
    'longitude':longitude,
    'latitude':latitude,
    'ocean_proximity':ocean_proximity,
    'median_income':median_income,
    'median_income_cat':median_income_cat,
    'bedrooms_per_room':bedrooms_per_room,
    'households':households,
    'housing_median_age':housing_median_age,
    'population_per_household':population_per_household,
    'population':population,
    'population_per_room':population_per_room,
    'rooms_per_household':rooms_per_household,
    'total_bedrooms':total_bedrooms,
    'total_rooms':total_rooms,
    
}

df_entrada_modelo = pd.DataFrame(entrada_modelo, index =[0])

previsao_modelo = modelo.predict(df_entrada_modelo)

botao_previsao = st.button("Prever o preço")

if botao_previsao:
    st.write(f"Preco da casa é de US$ {previsao_modelo[0][0]:,.2f}")