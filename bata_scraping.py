from bs4 import BeautifulSoup
import requests
import pandas as pd

pd.options.display.max_rows = None  # Visualizza tutte le righe
pd.options.display.max_columns = None  # Visualizza tutte le colonne

headers = {"User-Agent": "Chrome/128.0"}
url_1 = "https://www.bata.com/it/donna/scarpe/stivali-e-stivaletti/?start=0&sz=240&srule=TOP-SELLERS"
url_2 = "https://www.bata.com/it/donna/scarpe/decollete/?start=0&sz=96&srule=TOP-SELLERS"
url_3 = "https://www.bata.com/it/donna/scarpe/mocassini/?start=0&sz=72&srule=TOP-SELLERS"
url_4 = "https://www.bata.com/it/donna/scarpe/stringate/?srule=TOP-SELLERS"
url_5 = "https://www.bata.com/it/donna/scarpe/ballerine/?start=0&sz=120&srule=TOP-SELLERS"
url_6 = "https://www.bata.com/it/donna/scarpe/sneakers/?start=0&sz=144&srule=TOP-SELLERS"
url_7 = "https://www.bata.com/it/donna/scarpe/sport/?start=0&sz=192&srule=TOP-SELLERS"
url_8 = "https://www.bata.com/it/donna/scarpe/sandali/?start=0&sz=312&srule=TOP-SELLERS"
url_9 = "https://www.bata.com/it/donna/scarpe/zeppe/?start=0&sz=96&srule=TOP-SELLERS"
url_10 = "https://www.bata.com/it/donna/scarpe/espadrillas/?srule=TOP-SELLERS"
url_11 = "https://www.bata.com/it/donna/scarpe/ciabatte-e-infradito/?start=0&sz=96&srule=TOP-SELLERS"
url_12 = "https://www.bata.com/it/donna/scarpe/pantofole/?srule=TOP-SELLERS"
url_13 = "https://www.bata.com/it/uomo/scarpe/stivaletti/?start=0&sz=96&srule=TOP-SELLERS"
url_14 = "https://www.bata.com/it/uomo/scarpe/mocassini/?start=0&sz=120&srule=TOP-SELLERS"
url_15 = "https://www.bata.com/it/uomo/scarpe/stringate/?start=0&sz=72&srule=TOP-SELLERS"
url_16 = "https://www.bata.com/it/uomo/scarpe/sneakers/?start=0&sz=168&srule=TOP-SELLERS"
url_17 = "https://www.bata.com/it/uomo/scarpe/sport/?start=0&sz=144&srule=TOP-SELLERS"
url_18 = "https://www.bata.com/it/uomo/scarpe/sandali/?start=0&sz=48&srule=TOP-SELLERS"
url_19 = "https://www.bata.com/it/uomo/scarpe/espadrillas/?srule=TOP-SELLERS"
url_20 = "https://www.bata.com/it/uomo/scarpe/ciabatte-e-infradito/?start=0&sz=72&srule=TOP-SELLERS"
url_21 = "https://www.bata.com/it/uomo/scarpe/pantofole/?srule=TOP-SELLERS"

url_list = [url_1, url_2, url_3, url_4, url_5, url_6, url_7, url_8, url_9, url_10, url_11, url_12, url_13, url_14,
            url_15, url_16, url_17, url_18, url_19, url_20, url_21]

genere_list = ["Donna"] * 12 + ["Uomo"] * 9

categorie_list = ["Stivali_stivaletti", "Decollete", "Mocassini", "Stringate", "Ballerine", "Sneakers", "Sport",
                  "Sandali", "Zeppe", "Espadrillas", "Ciabatte_infradito", "Pantofole", \
                  "Stivaletti", "Mocassini", "Stringate", "Sneakers", "Sport", "Sandali", "Espadrillas",
                  "Ciabatte_infradito", "Pantofole"]

d1 = dict(zip(url_list, genere_list))
d2 = dict(zip(url_list, categorie_list))

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
        price = float(price_tag.get_text(strip=True).split()[0])

        price_original_tag = product.find("span", class_="cc-original-price")
        if price_original_tag is not None:
            price_original = float(price_original_tag.get_text(strip=True).split()[0])
        else:
            price_original = price

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
            "Genere": d1[url],
            "Categoria": d2[url],
            "Nome": nome,
            "Prezzo_effettivo": price,
            "Prezzo_originario": price_original,
            "Colore": colors,
            "Taglia": taglie
        })

    new_df = pd.DataFrame(prodotti)  # nuovo dataframe
    df = pd.concat([df, new_df])

print(df)
# salvo in un csv
df.to_csv("prodotti_bata_scraping.csv", index=False)
