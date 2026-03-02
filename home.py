import streamlit as st
import pydeck as pdk
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


coluna1, coluna2 = st.columns(2)

with coluna1:

    #formulário para atualizar mapa somente se mudar o condado
    with st.form(key="formulario"):
    
        #Variáveis de Localização
        
        condados = list(gdf_geo["name"].sort_values()) #lista de condados
        selecionar_condados = st.selectbox(label = "Região (condado)", options = condados, index = 18) #seleção do condado
        
        df_condado = gdf_geo.query("name == @selecionar_condados")
        
        #cálculo de latitude e longitude
        longitude = df_condado["longitude"].values[0]
        latitude = df_condado["latitude"].values[0]
        
        #pega a categoria no dataframe baseado no condado selecionado
        ocean_proximity = df_condado["ocean_proximity"].values[0]
        
        #cálculo de renda média baseado no condado
        median_income = df_condado["median_income"].values[0]
        median_income_cat = df_condado["median_income_cat"].values[0]
        
        
        #Variáveis do imóvel
        
        #population, households é a média do condado
        population_per_household = df_condado["population_per_household"].values[0]
        population = df_condado["population"].values[0]
        households = df_condado["households"].values[0]
        
        #usuário seleciona quantidade de quartos e comodos
        
        # Usuário seleciona quantidade de cômodos (mínimo 2, máximo 10)
        rooms_per_household = st.select_slider("nº de cômodos", options=list(range(2, 11)), value=5)
        
        # Calcula 40% dos cômodos arredondando para baixo.
        # O max(1, ...) garante que, mesmo que o cálculo dê 0 (como no caso de 2 cômodos), o limite seja pelo menos 1.
        maximo_quartos = max(1, int(rooms_per_household * 0.4))
        
        # Cria a lista de opções para os quartos
        opcoes_quartos = list(range(1, maximo_quartos + 1))
        
        # Verificação para evitar o RangeError se houver apenas 1 opção
        if len(opcoes_quartos) == 1:
            st.markdown("**nº de quartos permitidos:** 1")
            bedrooms_per_household = 1
        else:
            bedrooms_per_household = st.select_slider("nº de quartos", options=opcoes_quartos)
        
        #Cálculos
        total_bedrooms = bedrooms_per_household * households
        total_rooms = rooms_per_household * households
        bedrooms_per_room = bedrooms_per_household / rooms_per_household 
        population_per_room = population / total_rooms
        
        
        #usuário seleciona a idade do imóvel
        housing_median_age = st.number_input("Idade do imóvel (em anos)", value = 20, min_value=1, max_value = 50) 
        
        
        
        
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
        
        
        botao_previsao = st.form_submit_button("Prever o preço")
        
    if botao_previsao:
        df_entrada_modelo = pd.DataFrame(entrada_modelo, index =[0])
        previsao_modelo = modelo.predict(df_entrada_modelo)
        st.write(f"Preco da casa é de US$ {previsao_modelo[0][0]:,.2f}")

with coluna2:
    view_state = pdk.ViewState(
            latitude=latitude,
            longitude=longitude,
            zoom=5,
            min_zoom=4,
            max_zoom=8,
    )
    
    # 1. Camada Base: Todos os condados (Fundo discreto)
    camada_fundo = pdk.Layer(
        "GeoJsonLayer", 
        data=gdf_geo[["name", "geometry"]],
        pickable=True, 
        stroked=True,  
        filled=True,   
        get_fill_color=[0, 0, 255, 30], # Opacidade bem baixa (30) para ficar sutil
        get_line_color=[255, 255, 255],
        get_line_width=500, 
        auto_highlight = True,
    )
    
    # 2. Camada de Destaque: Apenas o Condado Selecionado
    camada_destaque = pdk.Layer(
        "GeoJsonLayer", 
        data=df_condado[["name", "geometry"]], # Puxa apenas o condado que o usuário escolheu
        pickable=True,
        stroked=True,  
        filled=True,   
        get_fill_color=[255, 99, 71, 200], # Cor de destaque (Vermelho Tomate) com alta opacidade
        get_line_color=[0, 0, 0],
        get_line_width=1500, # Borda mais grossa
    )
    
    # Configuração do Tooltip
    configuracao_tooltip = {
        "html": "Condado: <b>{name}</b>",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white",
            "font-family": "sans-serif",
            "fontSize": "12px",       # Diminui o tamanho da letra
            "padding": "5px 10px",    # Reduz a "gordura" (espaço) ao redor do texto
            "borderRadius": "5px"     # (Bônus) Deixa as bordas da caixinha arredondadas
        }
    }
    
    # Juntando as duas camadas no mapa
    mapa = pdk.Deck(
        map_style='light', 
        initial_view_state=view_state,
        layers=[camada_fundo, camada_destaque], # A camada de destaque fica por último para aparecer por cima
        tooltip=configuracao_tooltip 
    )
    
    st.pydeck_chart(mapa)

    