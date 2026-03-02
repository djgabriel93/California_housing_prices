import streamlit as st
import pydeck as pdk
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


st.title("🏡 Previsão de Preços de Imóveis na Califórnia")

st.markdown("""
#### Este simulador faz parte do Projeto de previsão de preços de imóveis utilizando modelo de Machine Learning. [Clique aqui para acessar mais detalhes](https://github.com/djgabriel93/California_housing_prices)


""")


coluna1, coluna2 = st.columns(2)

# =========================================================
# 1. SELEÇÃO DE CONDADO (Gatilho para recarregar tudo)
# =========================================================
with coluna1:

    st.write("Insira as informações sobre a casa para prever o preço:")
    
    condados = list(gdf_geo["name"].sort_values())
    selecionar_condados = st.selectbox(label="Condado:", options=condados, index=18) 
    
    df_condado = gdf_geo.query("name == @selecionar_condados")
    
    # Variáveis baseadas no condado
    longitude = df_condado["longitude"].values[0]
    latitude = df_condado["latitude"].values[0]
    ocean_proximity = df_condado["ocean_proximity"].values[0]
    median_income = df_condado["median_income"].values[0]
    median_income_cat = df_condado["median_income_cat"].values[0]
    
    population_per_household = df_condado["population_per_household"].values[0]
    population = df_condado["population"].values[0]
    households = df_condado["households"].values[0]

# =========================================================
# 2. FRAGMENTO: CONTROLES DO IMÓVEL (Isolado do mapa)
# =========================================================
@st.fragment
def controles_do_imovel():
    rooms_per_household = st.select_slider("Nº de cômodos:", options=list(range(2, 11)), value=7)
    
    maximo_quartos = max(1, int(rooms_per_household * 0.4))
    opcoes_quartos = list(range(1, maximo_quartos + 1))
    
    if len(opcoes_quartos) == 1:
        st.markdown("**Nº de quartos permitidos:** 1")
        bedrooms_per_household = 1
    else:
        bedrooms_per_household = st.select_slider("Nº de quartos:", options=opcoes_quartos,value=2)
    
    housing_median_age = st.number_input("Idade do imóvel (em anos)", value=20, min_value=1, max_value=50) 
    
    botao_previsao = st.button("Prever o preço")
    
    if botao_previsao:
        total_bedrooms = bedrooms_per_household * households
        total_rooms = rooms_per_household * households
        bedrooms_per_room = bedrooms_per_household / rooms_per_household 
        population_per_room = population / total_rooms
        
        entrada_modelo = {
            'longitude': longitude,
            'latitude': latitude,
            'ocean_proximity': ocean_proximity,
            'median_income': median_income,
            'median_income_cat': median_income_cat,
            'bedrooms_per_room': bedrooms_per_room,
            'households': households,
            'housing_median_age': housing_median_age,
            'population_per_household': population_per_household,
            'population': population,
            'population_per_room': population_per_room,
            'rooms_per_household': rooms_per_household,
            'total_bedrooms': total_bedrooms,
            'total_rooms': total_rooms,
        }
        
        df_entrada_modelo = pd.DataFrame(entrada_modelo, index=[0])
        previsao_modelo = modelo.predict(df_entrada_modelo)
        
        # Usando st.success para deixar a mensagem verde e atrativa
        st.success(f"O preço estimado da casa é de: **US$ {previsao_modelo.item():,.2f}**")

# Chamamos a função do fragmento para renderizar na Coluna 1
with coluna1:
    controles_do_imovel()


# =========================================================
# 3. MAPA (Na coluna 2)
# =========================================================
with coluna2:
    view_state = pdk.ViewState(
            latitude=latitude,
            longitude=longitude,
            zoom=5,
            min_zoom=4,
            max_zoom=8,
    )
    
    camada_fundo = pdk.Layer(
        "GeoJsonLayer", 
        data=gdf_geo[["name", "geometry"]],
        pickable=True, 
        stroked=True,  
        filled=True,   
        get_fill_color=[0, 0, 255, 30], 
        get_line_color=[255, 255, 255],
        get_line_width=500, 
        auto_highlight=True,
    )
    
    camada_destaque = pdk.Layer(
        "GeoJsonLayer", 
        data=df_condado[["name", "geometry"]], 
        pickable=True,
        stroked=True,  
        filled=True,   
        get_fill_color=[255, 99, 71, 200], 
        get_line_color=[0, 0, 0],
        get_line_width=1500, 
    )
    
    configuracao_tooltip = {
        "html": "Condado: <b>{name}</b>",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white",
            "font-family": "sans-serif",
            "fontSize": "12px",       
            "padding": "5px 10px",    
            "borderRadius": "5px"     
        }
    }
    
    mapa = pdk.Deck(
        map_style='light', 
        initial_view_state=view_state,
        layers=[camada_fundo, camada_destaque], 
        tooltip=configuracao_tooltip 
    )
    
    st.pydeck_chart(mapa)

    
st.markdown("---") # Uma linha suave para separar os blocos visuais

st.markdown("Desenvolvido por [Gabriel Duarte](https://www.linkedin.com/in/djgabriel93)")