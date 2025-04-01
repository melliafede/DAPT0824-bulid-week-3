from bs4 import BeautifulSoup
import requests
import pandas as pd

# pd.options.display.max_rows = None        #Visualizza tutte le righe
# pd.options.display.max_columns = None     #Visualizza tutte le colonne

headers = {"User-Agent": "Chrome/128.0"}
url_mocassino = "https://www.sarenza.it/store/product/list/view?gender=1&selling_price=30.0&selling_price=86.07&sort=newest&type=11&index=100&count=100"

url_list = [url_mocassino]
categorie_list = ["mocassino"]

d = dict(zip(url_list, categorie_list))

df = pd.DataFrame()

for url in url_list:
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, "html.parser")
    products = soup.find_all("li", class_="vignette")
    print(len(products))

    prodotti = []

    for product in products:

        nome = product.find("img").get("title")

        price = product.find("span", class_="mighty price" ).get_text().strip()

        # size_tag = product.find("div", class_="sizes")
        # sizes = size_tag.findall("span")
        # taglie = []
        # for size in sizes:
        #     taglia = size.get_text()
        #     taglie.append(taglia)

        prodotti.append({
            "Categoria" : d[url],
            "Nome": nome,
            "Prezzo": price
            # "Taglie": taglie
        })

    new_df = pd.DataFrame(prodotti)
    df =  pd.concat([df, new_df])

print(df)

