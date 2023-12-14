import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine
import seaborn as sns

#import data from SQLdb
engine = create_engine('postgresql://postgres:Reggaere@localhost:5432/vaistines')
df1 = pd.read_sql('SELECT * from euro', engine)
df2 = pd.read_sql('SELECT * from metu', engine)
df3 = pd.read_sql('SELECT * from camelia', engine)

#merge tables
merge_table = pd.merge(df1, df2, on='brand')
df4 = pd.merge(merge_table, df3, on='brand')

#drop duplicates from merged table
df4.drop_duplicates(subset=['title_euro'], inplace=True)
df4.drop_duplicates(subset=['title_100metu'], inplace=True)
df4.drop_duplicates(subset=['title_camelia'], inplace=True)

#create new csv file with merged table data
df4.to_csv("mergeddata.csv", index=False)

# PLOT: average prices of all medicine by pharmacies


df4['price_euro'] = df4['price_euro'].str.replace(',', '.').astype(float)
avg_price_euro = round(df4['price_euro'].mean(), 2)
print(f'Kainos vidurkis EURO vaistine {avg_price_euro} €')

df4['price_camelia'] = df4['price_camelia'].str.replace(',', '.').astype(float)
avg_price_camelia = round(df4['price_camelia'].mean(), 2)
print(f'Kainos vidurkis Camelia vaistine {avg_price_camelia} €')

df4['price_100metu'] = df4['price_100metu'].astype(float)
avg_price_100metu = round(df4['price_100metu'].mean(), 2)
print(f'Kainos vidurkis 100 metu vaistine {avg_price_100metu} €')


pharmacys = ['Camelia', '100metu', 'Eurovaistine']
price_avg = [avg_price_camelia,avg_price_100metu,avg_price_euro]

#plot type pie
explode = (0, 0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
fig, ax = plt.subplots()
title = plt.title('Average prices of all medicine by pharmacies', fontweight="bold", fontsize=15)
title.set_ha("center")
ax.pie(price_avg, explode=explode, labels=pharmacys, autopct='%1.1f%%', shadow=True, startangle=90, colors=['indianred','cornflowerblue','yellowgreen'])
ax.legend(price_avg, title="Average Price EUR", loc="upper left", bbox_to_anchor=(0.85, 1.025))
plt.savefig("Average prices of all medicine by pharmacies.png", bbox_inches="tight")
plt.show()


# Price for most popular cold medicine brands ##########################################################################

brand = ("Fervex", "Coldrex", "Gripex")
pharmacy_price = {
    'Eurovaistine': (7.35, 6.78, 7.20),
    'Camelia': (8.55, 7.71, 7.89),
    '100 metu': (6.52, 7.38, 5.03),
}

x = np.arange(len(brand))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')
for attribute, measurement in pharmacy_price.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1


ax.set_ylabel('Price €', fontweight="bold")
ax.set_title('Price for most popular cold medicine brands', fontweight="bold", fontsize=15)
ax.set_xticks(x + width, brand, fontweight="bold", rotation=45)
ax.legend(loc='upper left', ncols=3)
ax.set_ylim(0, 30)
plt.savefig("Price for most popular cold medicine brands", bbox_inches="tight")

plt.show()



# # Amount of over-the-counter medicine##################################################

a = df1['price_euro'].count()
b = df2['price_100metu'].count()
c = df3['price_camelia'].count()

df5 = [c, b, a]
pharmacys = ['Camelia', '100metu', 'Euro']

plt.bar(pharmacys, df5, color='maroon')
plt.title('Amount of over-the-counter medicine', fontweight="bold", fontsize=15)
plt.savefig("Amount of over-the-counter medicine.png", bbox_inches="tight")
plt.show()



#############Price for the most popular nasal sprays

brand = ("Olydex", "Nasometin", "Olynth")
pharmacy_price = {
    'Eurovaistine': (6.10, 7.37, 4.03),
    'Camelia': (4.99, 7.29, 5.09),
    '100Metu': (5.01, 7.37, 3.28),
}

x = np.arange(len(brand))
width = 0.25
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in pharmacy_price.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

ax.set_ylabel('Price', fontweight="bold")
ax.set_title('Price for the most popular nasal sprays', fontweight="bold")
ax.set_xticks(x + width, brand, fontweight="bold")
ax.legend(loc='upper left', ncols=3)
ax.set_ylim(0, 30)
plt.savefig("Price for the most popular nasal sprays.png", bbox_inches="tight")

plt.show()

##########Amount of medicine by manufacturer

count = df4.groupby('manufacturer')['title_camelia'].count().head(15)

count.plot(kind='bar', figsize=(15, 10), width=0.9, color='lime')
plt.title('Amount of medicine by manufacturer', fontsize=30, fontweight="bold")
plt.ylabel('amount', fontsize=10, fontweight="bold")
plt.ylabel('manufacturer', fontsize=10, fontweight="bold")
plt.xticks(rotation=20, fontsize=10, fontweight="bold")
plt.savefig("Amount of medicine by manufacturer.png", bbox_inches="tight")
plt.show()







