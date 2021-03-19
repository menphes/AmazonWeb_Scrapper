import requests
from bs4 import BeautifulSoup
import json, os

# # Função que Verifica se há Proxima Pagina de Resultados
def verificadorProxPagina(site):
    # # Estrutura do Amazon.com (2021-03-17)
    listaPaginas = []
    #listaPaginas = soup.find_all("div", {"class": "a-text-center"})
    if soup.select('div[class="a-text-center"]') != None:
        listaPaginas = soup.select('div[class="a-text-center"]')
    elif soup.select('div[class="a-section a-spacing-none s-result-item s-flex-full-width s-widget"]') != None:
        listaPaginas = soup.select('div[class="a-section a-spacing-none s-result-item s-flex-full-width s-widget"]')
    else:
        print('Não há Mais Paginas de Resultados.')
    
    if len(listaPaginas) != 0:
        urlProxPagina = listaPaginas[0].find("li", {"class": "a-last"})
        url = urlProxPagina.find("a")
        if url != None:
            urlPage = r"https://www.amazon.com.br"+str(url['href'])
        else:
            urlPage = None
    else:
        urlPage = None
    return urlPage

# # Pede o Input dos Termos que devem ser pesquisados
query = input('Qual Termos a ser Pesquisado?')
# # Remove espaços em branco e inclui '+' no lugar
query = query.replace(' ', '+').lower()

# # Estrutura URL de Pesquisa do Amazon
urlPage = f'https://www.amazon.com.br/s?k={query}&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss'
# # Define que Primeira URL será a Pagina Inicial
pageInicial = True

# # Inicia Dicionario que retornaram os resultados
searchResults = {}

# # Executa código enquanto houver proxima Pagina
while urlPage != None:
    page = requests.get(urlPage, verify=False)
    soup = BeautifulSoup(page.text, 'html.parser')

    urlPage = verificadorProxPagina(soup)

    # # Estrutura de Web Scrapping do Amazon.com (2021-03-17)
    table = soup.find("div", {"class": "s-main-slot s-result-list s-search-results sg-row"})
    items = table.find_all("div", {"class": "s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col sg-col-12-of-16"})
    
    if len(items) == 0:
        items = table.find_all("div", {"class": "sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20"})
    
    for item in items:
        try:
            nota = float(str(item.find("span", {"class": "a-icon-alt"}).text.strip())[:3].replace(',', '.'))
        except:
            nota = None

        try:
            nomeItem = item.find("span", {"class": "a-size-medium a-color-base a-text-normal"}).text.strip().replace(r'"','')
        except:
            nomeItem = item.find("span", {"class": "a-size-base-plus a-color-base a-text-normal"}).text.strip().replace(r'"','')

        try:
            preco = str(item.find("span", {"class": "a-offscreen"}).text.strip())[3:]
        except:
            preco = None
        
        try:
            searchResults[nomeItem] = {"Preço": "R$" + preco, "Nota": nota}
        except:
            pass

print('Foram encontrados ' + str(len(searchResults)) + ' itens para sua pesquisa!')
arq = str(os.getcwd()) + f"\\retornoQueryAmazon_{query}.json"
file = open(arq, "w")
dump = json.dumps(searchResults, indent=3, sort_keys=True, ensure_ascii=False)
file.write(str(dump))
file.close()
