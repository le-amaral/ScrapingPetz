# Importar as bibliotecas necessárias
import requests  # Para fazer requisições HTTP
from bs4 import BeautifulSoup  # Para fazer parsing do HTML
import pandas as pd  # Para criar e manipular DataFrames do Pandas


# Inicializar uma lista vazia para armazenar os dados raspados
data = []

# Lista de URLs das páginas a serem raspadas
links = [
    "https://adotar.com.br/animais/es-serra/adocao/cao",
    "https://adotar.com.br/animais/es-vitoria/adocao/cao",
    "https://adotar.com.br/animais/es-vila-velha/adocao/cao",
    "https://adotar.com.br/animais/es-cariacica/adocao/cao",
    "https://adotar.com.br/animais/es-guarapari/adocao/cao",
    "https://adotar.com.br/animais/es-serra/adocao/gato",
    "https://adotar.com.br/animais/es-vitoria/adocao/gato",
    "https://adotar.com.br/animais/es-vila-velha/adocao/gato",
    "https://adotar.com.br/animais/es-cariacica/adocao/gato",
    "https://adotar.com.br/animais/es-guarapari/adocao/gato",
]
# Configurações de cabeçalho para a solicitação HTTP
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}
# Loop através das URLs
for link in links:

    # Faz uma solicitação HTTP GET para a URL atual com o cabeçalho definido
    requisicao = requests.get(link, headers=headers)

    # Analisa o conteúdo HTML da página usando BeautifulSoup
    site = BeautifulSoup(requisicao.text, "html.parser")

    # Encontra todos os elementos com a classe 'listaAnimaisDados'
    div_elements = site.find_all('div', class_='listaAnimaisDados')
   
   # Determina o tipo de animal com base no final da URL
    tipo_animal = "Cachorro" if "/cao" in link else "Gato"

    # Extrai a região através da URL
    regiao = link.split('/')[-3].replace('-', ' ').title()

    # Loop através dos elementos encontrados
    for div_element in div_elements:
        # Extrai o nome do animal
        nome_animal = div_element.contents[0].strip()

        # Encontra as tags "br" dentro do elemento
        br_tags = div_element.find_all('br')
        if len(br_tags) >= 2:
            # Extrai informações de gênero/porte e idade
            genero_porte = br_tags[0].next_sibling.strip()
            idade = br_tags[1].next_sibling.strip()

         # Adiciona os dados à lista 'data' como uma lista
        data.append([tipo_animal, nome_animal, regiao, genero_porte, idade])

        # Cria um DataFrame do Pandas com os dados coletados
        df = pd.DataFrame(
            data, columns=["Tipo", "Nome", "Região", "Gênero/Porte", "Idade"])

        # Salva o DataFrame em um arquivo Excel chamado "animais_adocao.xlsx"
        df.to_excel("animais_adocao.xlsx", index=False)
