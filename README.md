# 1. Problema de negócio
A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.

Você acaba de ser contratado como Cientista de Dados da empresa Fome Zero, e a sua principal tarefa nesse momento é ajudar o CEO a identificar pontos chaves da empresa, respondendo às seguintes perguntas:

## Contexto Geral

1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?

## Contexto Países

1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados?
4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos?
5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega?
7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas?
8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registrada?
9. Qual o nome do país que possui, na média, a maior nota média registrada?
10. Qual o nome do país que possui, na média, a menor nota média registrada?
11. Qual a média de preço de um prato para dois por país?

## Contexto Cidades

1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5?
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas?
7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas?
8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online?

## Contexto Restaurantes

1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de uma prato para duas pessoas?
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação?
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação?
6. Os restaurantes que aceitam pedido online são também, na média, os restaurantes que mais possuem avaliações registradas?
7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas?
8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)?

## Contexto Tipos de Culinária

1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação?
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação?
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação?
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação?
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação?
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a menor média de avaliação?
9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação?
10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a menor média de avaliação?
11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas?
12. Qual o tipo de culinária que possui a maior nota média? 
13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?


# 2. Premissas assumidas para a análise

1. Os valores de conversão das moedas de cada país para o dólar americano foram obtidos via google no dia 30/11/2023.
2. O modelo de negócio assumido foi o de Marketplace.
3. As 4 principais visões do negócio foram: Geral, Países, Cidades e Cozinhas.
4. Os dados referentes à latitude e longitude foram assumidos como corretos, devido a impraticidade em se verificar essas informações através do Google Maps.
5. De acordo com o autor, o conjunto de dados Zomato Restaurants é atualizado semanalmente. A versão utilizada na presente análise foi obtida no dia 11/11/2023.

# 3. Estratégia da solução

O Dashboard foi desenvolvido utilizando as métricas que refletem as 4 principais visões do modelo de negócio da empresa:
1. Visão Geral;
2. Visão Países;
3. Visão Cidades;
4. Visão Cozinhas.

Cada visão é representada pelo seguinte conjunto de métricas.

## 1. Visão Geral
  1. Restaurantes registrados;
  2. Países registrados;
  3. Cidades registradas;
  4. Nº de avaliações;
  5. Variedade Culinária;
  6. Distribuição geográfica dos restaurantes.

## 2. Visão Países
  1. Quantidade de restaurantes registrados por país;
  2. Quantidade de cidades registradas por país;
  3. Quantidade média de avaliações registradas por país;
  4. O valor médio de um prato para dois por país.

## 3. Visão Cidades
  1. Top 10 cidades com mais restaurantes;
  2. Top 7 cidades com média de avaliação acima de 4;
  3. Top 7 cidades com média de avaliação abaixo de 2,5;
  4. Top 10 cidades com a maior diversidade culinária.

## 4. Visão Cozinhas
  1. Melhores restaurantes dos tipos de culinária: italiana, americana, árabe, japonesa e caseira;
  2. Top n restaurantes, sendo 1 <= n <=20;
  3. Top n melhores tipos culinários, sendo 1 <= n <=20;
  4. Top n piores tipos culinários, sendo 1 <= n <=20;

# 4. Top 3 Insights de dados
1. O marketplace é tão utilizado no Ocidente quanto no Oriente, sendo 51,8% a porcentagem da quantidade de votos do primeiro;
2. Embora a média das notas dentre os países varie consideravelmente, esse fenômeno não ocorre se comparados os continentes. Com exceção da América do Sul, que possui uma média de 3, o restante dos continentes empata em 4.
3. Confirmando o que se espera, o valor médio de um prato para dois é menor para a América do Sul (USD 29), Ásia (USD 19) e África(USD 18). Nesses continentes, em média, o dólar é mais desvalorizado em comparação com a moeda local. A Europa (USD 55) registra o maior valor médio.

# 5. O produto final do projeto
Dashboard online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet. 
O painel pode ser acessado através desse link: https://fomezero-dashboard.streamlit.app/

# 6. Conclusão
O objetivo do projeto é criar um conjunto de gráficos e/ou tabelas que exibam as métricas do negócio da melhor forma possível para o CEO. 
Da visão da Empresa, podemos concluir que o marketplace é na prática, igualmente utilizado tanto no Ocidente quanto no Oriente. Essa informação sugere que é importante um estudo aprofundado nas mais variadas culturas dessas regiões de forma a criar perfis de usuários para um marketing abrangente, não exclusivo.

# 7. Próximo passos
1. Adicionar a possibilidade de o usuário escolher um tipo de culinária e receber a informação de qual o melhor restaurante naquela categoria. No momento, o dashboard se limita à cinco pré-estabelecidas;
2. Aprimorar o conjunto de dados, definindo um tratamento para as observações cuja a localização geográfica está no oceano;
3. Adicionar novas visões de negócio, como o contexto "Continentes" para uma visão ainda mais ampla do marketplace.
