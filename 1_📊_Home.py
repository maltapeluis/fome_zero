# ===========================================
# Importando as bibliotecas necessárias
# ===========================================
!pip install inflection
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


# criando uma função responsável por gerar um mapa geográfico das localizações do restaurantes registrados na plataforma Fome Zero
def rest_map(df5):
    cols = ['restaurant_name', 'cuisines', 'aggregate_rating', 'average_cost_for_two', 'latitude', 'longitude']
    
    df6 = df5.loc[:, cols].groupby(['restaurant_name', 'cuisines']).mean().reset_index()
    
    map = folium.Map()
    
    marker_cluster = MarkerCluster().add_to(map)
    
    MiniMap().add_to(map)
    
    folium.plugins.Fullscreen(position="topright", 
                              title="Expand me", 
                              title_cancel="Exit me", 
                              force_separate_button=True,).add_to(map)
        
    for index, location_info in df6.iterrows():
        rest_name, cozinha, custo_pra_dois = location_info[['restaurant_name', 'cuisines', 'average_cost_for_two']]
        
        (folium.Marker([location_info['latitude'], location_info['longitude']], 
                       icon=folium.Icon(icon = 'home', color="green"), 
                       popup = '<p><strong>Restaurante: </strong>'+ 
                       rest_name + '</p>\n<p><strong>Culinária: </strong>'+ 
                       cozinha + '</p>\n<p><strong>Valor médio pª dois: </strong>'+ 
                       str(custo_pra_dois)+' USD').add_to(marker_cluster))
    return map

# criando uma função para calcular algumas métricas gerais do negócio 
def overall_metrics(op, col):
    if op == 'nunique':
        resultado = df4[col].nunique()
    elif op == 'sum':
        resultado = df4[col].sum()
    else:
        raise ValueError('Parâmetro incorreto!')
    resultado = '{:,}'.format(resultado)
    return resultado

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
    page_title = 'home',
    page_icon = ':bar_chart:',
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
    
st.sidebar.markdown('### Dados Tratados')
treated_data = df4.to_csv()
st.sidebar.download_button(label = 'Download', data = treated_data)

st.title(':bar_chart: FOME ZERO!')
st.markdown('### O Melhor lugar para encontrar seu mais novo restaurante favorito!')
st.markdown('#### Temos as seguintes marcas dentro da nossa plataforma:')

# ===========================================
# Respondendo às questões - VISÃO GERAL
# ===========================================
filtro_pais = df4['country_name'].isin(country_options)
df5 = df4.loc[filtro_pais, :]

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        # Quantos restaurantes únicos estão registrados?
        resultado = overall_metrics('nunique', 'restaurant_id')
        col1.metric("Restaurantes registrados:", resultado)

    with col2:
        # Quantos países únicos estão registrados?
        resultado = overall_metrics('nunique', 'country_name')
        col2.metric("Países registrados:", resultado)
        
    with col3:
        # Quantas cidades únicas estão registradas?
        resultado = overall_metrics('nunique', 'city')
        col3.metric("Cidades registradas:", resultado)
        
    with col4:
        # Qual o total de avaliações feitas?
        resultado = overall_metrics('sum', 'votes')
        col4.metric("Nº de avaliações:", resultado)
        
    with col5:
        # Qual o total de tipos de culinária registrados?
        resultado = overall_metrics('nunique', 'cuisines')
        col5.metric("Variedade Culinária:", resultado)

with st.expander('Distribuição Geográfica dos Restaurantes', expanded = True):
    ## Gera um mapa dos restaurantes registrados no conjunto de dados
    map = rest_map(df5)    
    folium_static(map, width = 1024, height = 600)

with st.container():
    st.write('## FOME ZERO Growth Dashboard')
    st.markdown(
        """
    A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core
    business é facilitar o encontro e negociações entre os restaurantes e os clientes. 
    
    Este Growth Dashboard foi construído para acompanhar as métricas de crescimento da Fome Zero, do ponto de vista local ao global, provendo uma visão ampla do negócio e permitindo a tomada de decisões mais estratégicas. 
    
    ### Como utilizar esse Growth Dashboard?
         É possível filtrar os resultados pelos países nos quais os restaurantes parceiros estão localizados.
         
         Início: 
            - Visão geral do negócio, contendo as suas principais métricas e a distribuição dos restaurantes filiados ao redor do globo.
         Visão Cidades:
            - Panorama local, contendo as cidades com o maior número de restaurantes com avaliações próximas de 5.0, contrastadas com aquelas cujos restaurantes não desempenham bem. 
         Visão Países:
            - Aborda alguns indicadores agrupados pelos países nos quais os restaurantes parceiros estão localizados.
         Visão Cozinhas: 
            - Apresenta as médias de avaliação bem como o custo médio de um prato para dois dos restaurantes parceiros, agrupados pelo tipo de culinária ofertado. 
            - Aqui é possível filtrar os resultados por variedade culinária e determinar a quantidade de restaurantes a ser exibida.
    ### Contato
        linkedin.com/in/maltape/
        """)
