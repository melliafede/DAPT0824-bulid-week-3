from bs4 import BeautifulSoup
import pandas as pd

file_path = "mocassini_bata.html"

with open(file_path, encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")

boxes = soup.find_all("div", class_="product-tile")

prodotti = []

for box in boxes:
    nome_tag = box.find("span", class_="cc-tile-product-name")
    print(type(nome_tag))
    nome = nome_tag.get_text(strip=True)

    price_tag = box.find("span", class_="cc-price")
    price = price_tag.get_text(strip=True)

    color_tag = box.find("div", class_="cc-color")
    color_links = color_tag.find("a" )
    colors = []
    for color_link in color_links:
        color = color_links.get("title")
        colors.append(color)

    prodotti.append({
        "Nome": nome,
        "Prezzo": price,
        "Colors":colors
    })

df = pd.DataFrame(prodotti)
print(df.head(10))
