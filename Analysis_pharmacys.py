import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine

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

#PLOT: average prices of all medicine by pharmacies


df4['price_euro'] = df4['price_euro'].str.replace(',', '.').astype(float)
avg_price_euro = round(df4['price_euro'].mean(), 2)
print(f'Kainos vidurkis EURO vaistine {avg_price_euro} €')

df4['price_camelia'] = df4['price_camelia'].str.replace(',', '.').astype(float)
avg_price_camelia = round(df4['price_camelia'].mean(), 2)
print(f'Kainos vidurkis Camelia vaistine {avg_price_camelia} €')

df4['price_100metu'] = df4['price_100metu'].astype(float)
avg_price_100metu = round(df4['price_100metu'].mean(), 2)
print(f'Kainos vidurkis 100 metu vaistine {avg_price_100metu} €')


pharmacys = ['Camelia', '100metu', 'Euro']
price_avg = [avg_price_camelia,avg_price_100metu,avg_price_euro]

#plot type pie
explode = (0, 0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
fig, ax = plt.subplots()
title = plt.title('average prices of all medicine by pharmacies', fontweight="bold", fontsize=15)
title.set_ha("center")
ax.pie(price_avg, explode=explode, labels=pharmacys, autopct='%1.1f%%', shadow=True, startangle=90, colors=['indianred','cornflowerblue','yellowgreen'])
ax.legend(price_avg, title="Average Price EUR", loc="upper left", bbox_to_anchor=(0.85, 1.025))
plt.savefig("average prices of all medicine by pharmacies.png", bbox_inches="tight")
plt.show()


# data= {'Price_euro': 8.47, 'Price_camelia': 8.07, 'Price_100metu': 7.9  }
# courses = list(data.keys())
# values = list(data.values())
# plt.figure(figsize=(12, 6))
# fig = plt.figure(figsize=(10, 5))
# # creating the bar plot
# plt.bar(courses, values, color='maroon', width=0.4)
# plt.xlabel("Pharmacies")
# plt.ylabel("Avarage Price")
# plt.title("Pharmacies Average Price")
# plt.show()

# Price for most popular cold medicine brands ##########################################################################

persalimo_vaistai = ['GRIPEX', 'COLDREX', 'THERAFLU']
brand = ("Theraflu", "Coldrex", "Gripex")
pharmacy_price = {
    'Eurovaistine': (17.56, 6.78, 7.20),
    'Camelia': (6.99, 7.71, 7.89),
    '100 metu': (5.17, 7.38, 5.03),
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



# # Amount of over-the-counter drugs##################################################

a = df1['price_euro'].count()
print(a)
b = df2['price_100metu'].count()
print(b)
c = df3['price_camelia'].count()
print(c)

df5 = [c,b,a]
pharmacys = ['Camelia', '100metu', 'Euro']

plt.bar(pharmacys, df5, color='maroon')
plt.title('Amount of over-the-counter drugs', fontweight="bold", fontsize=15)
plt.savefig("Amount of over-the-counter drugs.png", bbox_inches="tight")
plt.show()


# ###Kuris brandas turi daugiausia vaistu


fig = plt.figure(figsize=(50, 10)) #create a figure with a 12 width, 4 length
ax1 = plt.subplot(131) #subplot with 1 row, 3 columns the 1st one
ax2 = plt.subplot(132) #subplot with 1 row, 3 columns the 2nd one
ax3 = plt.subplot(133) #subplot with 1 row, 3 columns the 3rd one
df4.plot(kind='scatter', x='brand', y='price_euro', ax=ax1, figsize=(40, 6))
df4.plot(kind='scatter', x='brand', y='price_camelia', ax=ax2, figsize=(40, 6))
df4.plot(kind='scatter', x='brand', y='price_100metu', ax=ax3, figsize=(40, 6))
plt.savefig("output.png", bbox_inches="tight")
plt.show()








