# ===========================================
# Importando as bibliotecas necessárias
# ===========================================

# importando as bibliotecas necessárias
import pandas as pd
import inflection
import plotly.express as px
import folium
import streamlit as st
from PIL import Image
from folium.plugins import MarkerCluster
from folium.plugins import MiniMap
from streamlit_folium import folium_static

# ===========================================
# Definindo as funções a serem utilizadas
# ===========================================

def fig_creator(df5, column):

    if column in ['restaurant_name', 'city']:
        func = 'nunique'
    
        if column == 'restaurant_name':
            column_label = 'Nº de Restaurantes'
            title_text = 'Quantidade de Restaurantes Registrados por País'
        elif column == 'city':
            column_label = 'Nº de Cidades'
            title_text = 'Quantidade de Cidades Registradas por País'

    elif column in ['votes', 'average_cost_for_two']:
        func = 'mean'

        if column == 'votes':
            column_label = 'Média de Avaliações'
            title_text = 'A Quantidade Média de Avaliações Registradas por País'
        elif column == 'average_cost_for_two':
            column_label = 'Valor Médio de um Prato para Dois (USD)'
            title_text = 'O Valor Médio de um Prato para Dois por País'
        
    else:
        raise ValueError('Invalid argument for "column" parameter. Expected "restaurant_name", "city", "votes" or "average_cost_for_two".')
    
    cols = [column, 'country_name', 'continent']
    df6 = df5.loc[:, cols].groupby(['continent','country_name']).agg(func).sort_values(column, ascending = False).reset_index()

    if column in ['votes', 'average_cost_for_two']:
        df6.loc[:, column] = df6.loc[:, column].round(0)

    fig = (px.bar(df6,
                  x = 'country_name', y = column,
                  color = 'continent',
                  text_auto = True,
                  title = title_text, 
                  labels = {column : column_label, 'country_name':'Países', 'continent' : 'Continente'}))
    return fig

# criando uma função que realiza todas as etapas de limpeza e tratamento dos dados brutos
def clean_df(path):
    # carregando o conjunto de dados no dataframe df
    df = pd.read_csv(path)
    # aplicando a função no conjunto de dados, gerando o dataframe df1
    df1 = rename_columns(df)
    # removendo as linhas que contêm valores nulos em um novo dataframe
    df1.dropna(inplace = True)
    # utilizando somente o primeiro valor constado na coluna 'cuisines' e descartando o restante, para fins de análise
    df2 = df1.copy()
    df2.loc[:, "cuisines"] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])
    # descartando a coluna 'switch_to_order_menu' por conter somente o valor 0, não sendo útil para nenhuma análise posterior
    df2.drop(columns = 'switch_to_order_menu', axis = 1, inplace = True)
    # efetuando as alterações nos tipos dos dados das colunas, de acordo com o conteúdo que possuem
    df2.loc[:, 'restaurant_id'] = df2.loc[:, 'restaurant_id'].astype(int)
    df2.loc[:, 'has_table_booking'] = df2.loc[:, 'has_table_booking'].astype(bool)
    df2.loc[:, 'has_online_delivery'] = df2.loc[:, 'has_online_delivery'].astype(bool)
    df2.loc[:, 'is_delivering_now'] = df2.loc[:, 'is_delivering_now'].astype(bool)
    # Substituindo os códigos numéricos pelos nomes dos países a que se referem
    df2.loc[:, 'country_name'] = df2.loc[:, 'country_code'].apply(lambda x: country_name(x))
    # Criando uma nova coluna contendo os continentes de cada restaurante
    df2.loc[:, 'continent'] = df2.loc[:, 'country_name'].apply(lambda x: continent(x))
    # Criando uma nova coluna contendo a classificação de preço para cada valor contido na coluna 'price_range'
    df3 = df2.copy()
    df3.loc[:, 'price_label'] = df2.loc[:, 'price_range'].apply(lambda x: create_price_type(x))
    # Substituindo os códigos numéricos das cores pelos nomes das cores a que se referem
    df3.loc[:, 'rating_color'] = df3.loc[:, 'rating_color'].apply(lambda x: color_name(x))
    duplicates = df3.duplicated()
    df4 = df3.drop_duplicates(ignore_index = True)
    # Criando uma coluna no dataframe contendo o custo médio para dois, em U$D
    df5 = df4.copy()
    df5.loc[:, 'currency_factor'] = df4.loc[:, 'country_name'].apply(lambda x: currency_factor(x))
    df6 = df5.copy()
    df6.loc[:, 'average_cost_for_two_old'] = df5.loc[:, 'average_cost_for_two']
    df7 = df6.copy()
    df7.loc[:, 'average_cost_for_two'] = df6.loc[:, 'average_cost_for_two'] * df6.loc[:, 'currency_factor']
    df7.loc[:, 'average_cost_for_two']= df7.loc[:, 'average_cost_for_two'].round(2)
    # Dropando um outlier da coluna 'average_cost_for_two', referente ao restaurante d'Arry's Verandah Restaurant, no valor de U$D 93.103,06.
    # O índice desta linha é 356
    df7.drop(356, inplace = True)
    df4 = df7.copy()
    return df4

# definindo uma função para renomear as colunas do dataframe original, formatando-as para substituição dos espaços por '____' , letras maiúsculas desnecessárias
def rename_columns(dataframe):
  df = dataframe.copy()
  title = lambda x: inflection.titleize(x)
  snakecase = lambda x: inflection.underscore(x)
  spaces = lambda x: x.replace(" ", "")
  cols_old = list(df.columns)
  cols_old = list(map(title, cols_old))
  cols_old = list(map(spaces, cols_old))
  cols_new = list(map(snakecase, cols_old))
  df.columns = cols_new
  return df

# criando uma função que retorna para cada código numérico de país recebido, o seu respectivo nome
# dicionário contendo os códigos numéricos como chave e os nomes dos seus respectivos países como valores
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

def country_name(country_id):
  return COUNTRIES[country_id]

# criando uma função que nomeia os intervalos de preço em 'barato', 'normal', 'caro' e 'gourmet'
def create_price_type(price_range):
  if price_range == 1:
    return "cheap"
  elif price_range == 2:
    return "normal"
  elif price_range == 3:
    return "expensive"
  else:
    return "gourmet"

# criando uma função que retorna para cada código de cor, o seu respectivo nome
# dicionário que relaciona os códigos de cores, como chave, e seus respectivos nomes, nos valores
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

def color_name(color_code):
  return COLORS[color_code]

# criando uma função que retorna para cada país, o seu respectivo fator de conversão de moeda:
# dicionário que relaciona os países aos fatores de conversão de suas respectivoas moedas para U$D: 
currency_factor_dict = {
    "India": 0.012,
    "Australia": 0.67,
    "Brazil": 0.21,
    "Canada": 1,
    "Indonesia": 0.000065,
    "New Zeland": 0.62,
    "Philippines": 0.074,
    "Qatar": 0.27,
    "Singapure": 1,
    "South Africa": 0.054,
    "Sri Lanka": 0.0030,
    "Turkey": 0.035 ,
    "United Arab Emirates": 0.27,
    "England": 1.27,
    "United States of America": 1,
    }

def currency_factor(country_name):
  return currency_factor_dict[country_name]

# criando uma função que retorna para cada país, o seu respectivo continente:
# O intuito disto é puramente visual, a ser aplicado nos gráficos da VISÃO PAÍSES
continent_dict = {
      'Philippines': 'Asia', 
      'Singapure': 'Asia', 
      'India': 'Asia', 
      'Indonesia': 'Asia', 
      'Sri Lanka': 'Asia', 
      'United Arab Emirates': 'Asia', 
      'Qatar': 'Asia', 
      'Turkey': 'Asia',
      'United States of America': 'North America',
      'Canada': 'North America', 
      'Brazil': 'South America', 
      'Australia': 'Oceania', 
      'South Africa': 'Africa',
      'New Zeland': 'Europe',
      'England': 'Europe'
      }

def continent(country_name):
  return continent_dict[country_name]

# ===========================================
# Configurando a página do Streamlit
# ===========================================

df4 = clean_df('dataset/zomato.csv')

st.set_page_config(
    page_title = 'Países',
    page_icon = ':earth_africa:',
    layout = 'wide'
)

# Textos a serem exibidos na barra lateral
image_path = ('images/logo.png')
image = Image.open( image_path)
st.sidebar.image( image, width = 50)

st.sidebar.markdown('## Filtros')

# Definindo segundo filtro a ser aplicado na barra lateral, na forma de uma lista suspensa
country_options = st.sidebar.multiselect(
    'Escolha os Paises que Deseja visualizar os Restaurantes',
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
    default = ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia', 'Turkey'],)

st.title(':earth_africa: VISÃO PAÍSES')
# ===========================================
# Respondendo às questões - VISÃO GERAL
# ===========================================

filtro_pais = df4['country_name'].isin(country_options)
df5 = df4.loc[filtro_pais, :]

with st.container():
    
    fig = fig_creator(df5, 'restaurant_name')
    st.plotly_chart(fig, use_container_width = True, theme = None)

with st.container():

    fig = fig_creator(df5, 'city')
    st.plotly_chart(fig, use_container_width = True, theme = None)
    
with st.container():    
    col1, col2 = st.columns(2)
    
    with col1:
        
        fig = fig_creator(df5, 'votes')
        st.plotly_chart(fig, use_container_width = True, theme = None)
    
    with col2:
                
        fig = fig_creator(df5, 'average_cost_for_two')
        st.plotly_chart(fig, use_container_width = True, theme = None)
