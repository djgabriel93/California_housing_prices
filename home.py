import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd

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


st.title("Pevisão de preços dos imóveis da Califórnia 🏡")

st.write("Localizaçao")
longitude = st.number_input("Longitude", value = -122.33)
latitude = st.number_input("latitude", value = 37.88)
ocean_proximity = st.radio("Proximidade Oceano", df['ocean_proximity'].unique())

st.write("Renda")#
median_income = st.slider("Renda média (múltiplos de US$ 10mil)", 0.50, 15.0, 4.5, 0.5)
median_income_cat = st.slider("Renda média (categoria)", 1,5)

st.write("Características do imóvel")#
bedrooms_per_room = st.number_input("Quartos por cômodo", value = 0.146591)
households = st.number_input("Domicílios", value = 126)
housing_median_age = st.number_input("Idade do imóvel", value = 41)
population_per_household = st.number_input("Pessoas por domicílio", value = 2.555556)
population = st.number_input("População", value = 322)
population_per_room = st.number_input("Pessoas por cômodo", value = 0.365909)
rooms_per_household = st.number_input("Pessoas por domicílios", value = 6.984127)
total_bedrooms = st.number_input("Total de quartos", value = 129)
total_rooms = st.number_input("Total de cômodos", value = 880)


entrada


if st.button("Previsão"):
    st.balloons()