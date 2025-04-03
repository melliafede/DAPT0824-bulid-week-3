from bs4 import BeautifulSoup
import requests
import pandas as pd

pd.options.display.max_rows = None        #Visualizza tutte le righe
pd.options.display.max_columns = None     #Visualizza tutte le colonne

headers = {"User-Agent": "Chrome/128.0"}
url_1 = "https://www.duelunecalzature.com/prodotti/donna/calzature-donna/ballerine-donna/"
url_2 = "https://www.duelunecalzature.com/prodotti/donna/calzature-donna/decollete-donna/"
url_3 = "https://www.duelunecalzature.com/prodotti/donna/calzature-donna/decollete-donna/?page=2"
url_4 = "https://www.duelunecalzature.com/prodotti/donna/calzature-donna/sandali-donna/"
url_5 = "https://www.duelunecalzature.com/prodotti/donna/calzature-donna/sandali-donna/?page=2"
url_6 = "https://www.duelunecalzature.com/prodotti/donna/calzature-donna/sandali-donna/?page=3"
url_7 = "https://www.duelunecalzature.com/prodotti/donna/calzature-donna/sandali-donna/?page=4"
url_8 = "https://www.duelunecalzature.com/prodotti/donna/calzature-donna/scarponcini-anfibi-donna/"
url_9 = "https://www.duelunecalzature.com/prodotti/donna/calzature-donna/stivaletti-tronchetti-donna/"
url_10 = "https://www.duelunecalzature.com/prodotti/donna/calzature-donna/stivaletti-tronchetti-donna/?page=2"
url_11 = "https://www.duelunecalzature.com/prodotti/donna/calzature-donna/stivali-donna/"
url_12 = "https://www.duelunecalzature.com/prodotti/donna/calzature-donna/stivali-donna/?page=2"
url_13 = "https://www.duelunecalzature.com/prodotti/donna/calzature-donna/scarpe-basse-donna/"
url_14 = "https://www.duelunecalzature.com/prodotti/donna/calzature-donna/sneakers-donna/"
url_15 = "https://www.duelunecalzature.com/prodotti/donna/calzature-donna/sneakers-donna/?page=2"
url_16 = "https://www.duelunecalzature.com/prodotti/uomo/calzature-uomo/doppia-fibbia-uomo/"
url_17 = "https://www.duelunecalzature.com/prodotti/uomo/calzature-uomo/goodyear-welted-uomo/"
url_18 = "https://www.duelunecalzature.com/prodotti/uomo/calzature-uomo/mocassini-slipon-uomo/"
url_19 = "https://www.duelunecalzature.com/prodotti/uomo/calzature-uomo/polacchine-uomo/"
url_20 = "https://www.duelunecalzature.com/prodotti/uomo/calzature-uomo/sandali-uomo/"
url_21 = "https://www.duelunecalzature.com/prodotti/uomo/calzature-uomo/sneakers-uomo/"
url_22 = "https://www.duelunecalzature.com/prodotti/uomo/calzature-uomo/sneakers-uomo/?page=2"
url_23 = "https://www.duelunecalzature.com/prodotti/uomo/calzature-uomo/stivaletti-uomo/"
url_24 = "https://www.duelunecalzature.com/prodotti/uomo/calzature-uomo/stringate-uomo/"

url_list = [url_1, url_2, url_3, url_4, url_5, url_6, url_7, url_8, url_9, url_10, url_11, url_12, url_13, url_14, url_15, url_16, \
            url_17, url_18, url_19, url_20, url_21, url_22, url_23, url_24]

genere_list = ["Donna"] * 15 + ["Uomo"] * 9

categorie_list = ["Ballerine", "Decollete_slingback", "Decollete_slingback", "Sandali_zeppe", "Sandali_zeppe", "Sandali_zeppe", \
                  "Sandali_zeppe", "Scarponcini", "Tronchetti", "Tronchetti", "Stivali", "Stivali", "Scarpe_basse", \
                  "Sneakers", "Sneakers", "Doppia_fibbia", "Goodyear", "Mocassini_slip_on", "Polacchini", "Sandali", "Sneakers", \
                  "Sneakers", "Stivaletti_scarponcini", "Stringate"]

d1 = dict(zip(url_list, genere_list))
d2 = dict(zip(url_list, categorie_list))

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
        prices = price.find_all("span", class_="woocommerce-Price-amount amount")

        prezzi = []

        for price in prices:
            price = float(price.find("bdi").get_text().split()[0].replace(",","."))
            prezzi.append(price)

        prezzo_originario = prezzi[0]
        if len(prezzi) > 1:
            prezzo_effettivo = prezzi[1]
        else:
            prezzo_effettivo = prezzo_originario


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
            taglia = float(span_size.get_text())
            taglie.append(taglia)


        prodotti.append({
            "Genere":d1[url],
            "Categoria":d2[url],
            "Nome": nome,
            "Prezzo_effettivo": prezzo_effettivo,
            "Prezzo_originario" : prezzo_originario,
            "Colore": colors,
            "Taglia": taglie
        })

    new_df = pd.DataFrame(prodotti)
    df =  pd.concat([df, new_df])

print(df)

#salvo in un csv
df.to_csv("prodotti_due_lune.csv", index=False)
