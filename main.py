import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

bata_df = pd.read_csv("prodotti_bata_scraping.csv")
bata_df["Marca"] = "Bata"
due_lune_df = pd.read_csv("prodotti_due_lune.csv")
due_lune_df["Marca"] = "Due Lune"

df = bata_df._append(due_lune_df)

df["Sconto"] = round((df["Prezzo_originario"] - df["Prezzo_effettivo"]) / df["Prezzo_originario"] * 100, 2)

filter_uomo = df["Genere"] == "Uomo"
filter_donna = df["Genere"] == "Donna"
print(df[["Prezzo_effettivo", "Prezzo_originario", "Sconto"]])

print(df[filter_uomo].groupby(["Marca", "Categoria"])["Prezzo_effettivo"].agg(["min", "mean", "max"]).sort_values("Categoria"))

sns.boxplot(data= df[filter_uomo], x="Categoria", y="Prezzo_effettivo", hue="Marca", order=sorted(df[filter_uomo]["Categoria"].unique()))

plt.title("Box plot")
plt.xlabel("Categoria")
plt.ylabel("Prezzo effettivo")
plt.show()



#
# bata_df = bata_df.rename(columns={"Categoria": "Sotto-categoria"})
# due_lune_df = due_lune_df.rename(columns={"Categoria": "Sotto-categoria"})
#
# print("Bata donna:")
# # uniamo sandali e zeppe in una stessa categoria per confrontare con due lune
#
# mappatura = {
#     "Espadrillas": "Sandali",
#     "Zeppe": "Sandali",
#     "Sandali": "Sandali",
#     "Sandali_zeppe": "Sandali",
#     "Decollete": "Decollete",
#     "Decollete_slingback": "Decollete",
#     "Stivali_stivaletti": "Stivali",
#     "Stivali": "Stivali",
#     "Scarponcini": "Stivali",
#     "Tronchetti": "Stivali",
#     "Sneakers": "Sneakers",
#     "Sport": "Sport",
#     "Stringate": "Scarpe_basse",
#     "Mocassini": "Scarpe_basse",
#     "Ballerine": "Scarpe_basse",
#     "Scarpe_basse": "Scarpe_basse",
#     "Ciabatte_infradito": "Ciabatte",
#     "Pantofole": "Ciabatte"
#
# }
#
#
# bata_df["Categoria"] = bata_df["Sotto-categoria"].apply(lambda x: mappatura.get(x, "Sconosciuto"))
# due_lune_df["Categoria"] = due_lune_df["Sotto-categoria"].apply(lambda x: mappatura.get(x, "Sconosciuto"))
#
# bata_df_donna = bata_df.loc[bata_df["Genere"] == "Donna"]
# due_lune_df_donna = due_lune_df.loc[due_lune_df["Genere"] == "Donna"]
#
# print(sorted(bata_df_donna["Sotto-categoria"].unique()))
# print(sorted(bata_df_donna["Categoria"].unique()))
#
# print(sorted(due_lune_df_donna["Sotto-categoria"].unique()))
# print(sorted(due_lune_df_donna["Categoria"].unique()))
