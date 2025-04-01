from bs4 import BeautifulSoup
import requests
import pandas as pd

pd.options.display.max_rows = None        #Visualizza tutte le righe
pd.options.display.max_columns = None     #Visualizza tutte le colonne

headers = {"User-Agent": "Chrome/128.0"}
url_ballerine = "https://www.duelunecalzature.com/prodotti/donna/calzature-donna/ballerine-donna/"

url_list = [url_ballerine]
categorie_list = ["Ballerine"]

d = dict(zip(url_list, categorie_list))

df = pd.DataFrame()

for url in url_list:
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, "html.parser")
    root = soup.find_all("div", class_="products")
    print(len(root))
    products = root[0].find_all("div", class_="info")

    prodotti = []

    for product in products:

        nome = product.find("div", class_="product-name")
        nome = nome.find("span", class_="roslindale uppercase").get_text()

        price = product.find("div", class_="info__price" )
        price = price.find("span", class_="woocommerce-Price-amount amount")
        price = price.find("bdi").get_text()

        altre_colorazioni = product.find("div", class_="info__altre-colorazioni")
        color_names = altre_colorazioni.find_all("div", class_="color-name")

        colors = []
        for color_name in color_names:
            color = color_name.find("span").get_text()
            colors.append(color)

        info_taglie = product.find("div", class_="info__taglie")
        lista_taglie = info_taglie.find("div", class_="lista-taglie")
        span_sizes = lista_taglie.find_all("span")

        taglie = []
        for span_size in span_sizes:
            taglia = span_size.get_text()
            taglie.append(taglia)


        prodotti.append({
            "Categoria" : d[url],
            "Nome": nome,
            "Prezzo": price,
            "Colore": colors,
            "Taglia": taglie
        })

    new_df = pd.DataFrame(prodotti)
    df =  pd.concat([df, new_df])

print(df)

