import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import numpy as np

df1 = pd.read_csv('euro.csv')
df2 = pd.read_csv('100metu.csv')
df3 = pd.read_csv('camelia.csv')

merge_table = pd.merge(df1, df2, on ='Brand')
df4 = pd.merge(merge_table, df3, on='Brand')
df4.drop_duplicates(subset=['Title_euro'], inplace=True)
df4.drop_duplicates(subset=['Title_100metu'], inplace=True)
df4.drop_duplicates(subset=['Title_camelia'], inplace=True)


df4.to_csv("mergeddata.csv", index=False)

#Vidutine visu vaistu kaina pagal vaistines -> isvada kuri vaistine pigiausia##########################################


df4['Price_euro'] = df4['Price_euro'].str.replace(',', '.').astype(float)
avg_price_euro = round(df4['Price_euro'].mean(), 2)
print(f'Kainos vidurkis EURO vaistine {avg_price_euro} €')

df4['Price_camelia'] = df4['Price_camelia'].str.replace(',', '.').astype(float)
avg_price_camelia = round(df4['Price_camelia'].mean(), 2)
print(f'Kainos vidurkis Camelia vaistine {avg_price_camelia} €')

df4['Price_100metu'] = df4['Price_100metu'].astype(float)
avg_price_100metu = round(df4['Price_100metu'].mean(), 2)
print(f'Kainos vidurkis 100 metu vaistine {avg_price_100metu} €')


pharmacys = ['Camelia', '100metu', 'Euro']
# price_avg = [avg_price_camelia,avg_price_100metu,avg_price_euro]
#
# explode = (0, 0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
# fig, ax = plt.subplots()
# #ax.pie(price_avg,  explode=explode, labels=pharmacys, autopct='%1.1f%%', shadow=True, startangle=90)
# ax.pie(price_avg, explode=explode, labels=pharmacys, autopct='%1.1f%%', shadow=True, startangle=90)
# ax.legend(price_avg, title="Average Price EUR", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
# plt.show()
#
#
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

#Populiariausiu persalimo vaistu kainu skirtumas tarp vaistiniu#########################################################

# persalimo_vaistai = [GRIPEX, COLDREX, THERAFLU]
# brand = ("Theraflu", "Coldrex", "Gripex")
# pharmacy_price = {
#     'Price_euro': (17.56, 6.78, 7.20),
#     'Price_camelia': (6.99, 7.71, 7.89),
#     'Price_100metu': (5.17, 7.38, 5.03),
# }
#
# x = np.arange(len(brand))  # the label locations
# width = 0.25  # the width of the bars
# multiplier = 0
#
# fig, ax = plt.subplots(layout='constrained')
#
# for attribute, measurement in pharmacy_price.items():
#     offset = width * multiplier
#     rects = ax.bar(x + offset, measurement, width, label=attribute)
#     ax.bar_label(rects, padding=3)
#     multiplier += 1
#
# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax.set_ylabel('Price')
# ax.set_title('Price for popular cold brand')
# ax.set_xticks(x + width, brand)
# ax.legend(loc='upper left', ncols=3)
# ax.set_ylim(0, 30)
#
# plt.show()

################Kurioj vaistinej daugiausia nereceptiniu vaistu#########################################################

# a = df1['Price_euro'].count()
# print(a)
# b = df2['Price_100metu'].count()
# print(b)
# c = df3['Price_camelia'].count()
# print(c)
#
# df5 = [c,b,a]
# pharmacys = ['Camelia', '100metu', 'euro']
#
# plt.bar(pharmacys, df5)
# plt.title('Nereceptiniu vaistu kiekiai')
# plt.show()


##############Kuris brandas turi daugiausia vaistu######################################################################

































