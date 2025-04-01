from bs4 import BeautifulSoup
import requests
import pandas as pd

pd.options.display.max_rows = None  # Visualizza tutte le righe
pd.options.display.max_columns = None  # Visualizza tutte le colonne

headers = {"User-Agent": "Chrome/128.0"}
url_1 = "https://www.bata.com/it/donna/scarpe/mocassini/?start=0&sz=500"
url_2 = "https://www.bata.com/it/donna/scarpe/decollete/?start=0&sz=500"
url_3 = "https://www.bata.com/it/donna/scarpe/stringate/?start=0&sz=500"
url_4 = "https://www.bata.com/it/donna/scarpe/ballerine/?start=0&sz=500"
url_5 = "https://www.bata.com/it/donna/scarpe/sneakers/?start=0&sz=500"
url_6 = "https://www.bata.com/it/donna/scarpe/stivali-e-stivaletti/?start=0&sz=500"
url_7 = "https://www.bata.com/it/donna/scarpe/sandali/?start=0&sz=500"
url_8 = "https://www.bata.com/it/donna/scarpe/sport/?start=0&sz=500"
url_9 = "https://www.bata.com/it/donna/scarpe/zeppe/?start=0&sz=500"
url_10 = "https://www.bata.com/it/donna/scarpe/espadrillas/?start=0&sz=500"
url_11 = "https://www.bata.com/it/donna/scarpe/ciabatte-e-infradito/?start=0&sz=500"

url_list = [url_1, url_2, url_3, url_4, url_5, url_6, url_7, url_8, url_9, url_10, url_11]
categorie_list = ["Mocassini", "Decollete", "Stringate", "Ballerine", "Sneakers", "Stivali", "Sandali", "Sport",
                  "Zeppe", "Espadrillas", "Infradito"]

d = dict(zip(url_list, categorie_list))

df = pd.DataFrame()

for url in url_list:
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, "html.parser")
    products = soup.find_all("div", class_="tile-body cc-tile-body")
    print(len(products))

    products = soup.find_all("div", class_="tile-body cc-tile-body")

    prodotti = []

    for product in products:
        nome_tag = product.find("span", class_="cc-tile-product-name")
        nome = nome_tag.get_text(strip=True)

        price_tag = product.find("span", class_="cc-price")
        price = price_tag.get_text(strip=True)

        color_tag = product.find("div", class_="cc-color")
        color_links = color_tag.find_all("a")
        colors = []
        for color_link in color_links:
            color = color_link.get("title")
            colors.append(color)

        taglie = []
        taglie_soup = product.find("div", class_="cc-size-list")
        for taglia_soup in taglie_soup.find_all("a"):
            if "/" in taglia_soup.text.strip().replace(",", ".").split(" ")[0]:
                taglia = float(taglia_soup.text.strip().split("/")[0])
            else:
                taglia = float(taglia_soup.text.strip().replace(",", ".").split(" ")[0])
            taglie.append(taglia)

        prodotti.append({
            "Categoria":d[url],
            "Nome": nome,
            "Prezzo": price,
            "Colore": colors,
            "Taglia": taglie
        })

    new_df = pd.DataFrame(prodotti)
    df = pd.concat([df, new_df])

print(df)
