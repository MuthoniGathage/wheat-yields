import pandas as pd
import pycountry
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"/home/user/PycharmProjects/pythonProject/International wheat production statistics.csv")
print(df.info())
print(df.head(10))


# To get country codes from country using the pycountry library


def country_code(column):
    code = list()
    for country in column:
        try:
            countrycode = pycountry.countries.get(name=country).alpha_3
            code.append(countrycode)
        except:
            code.append("None")
    return code


df["iso_a3"] = country_code(df.Country)
print(df.head())

# A GeoDataframe
df_geo = gpd.GeoDataFrame(df)
print(df_geo.head(3))
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
print(world)
merge = pd.merge(world, df, on="iso_a3")
print(merge.head())

# Barplot for the year 1996

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 10))
sns.barplot(data=merge, x="Country", y="1996", ax=ax)
ax.tick_params(axis="x", labelrotation=90)
ax.set_ylabel("wheat yield")
ax.set_title("wheat yield by country in 1996")

# World map wheat yield 1996
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
merge.plot(column=merge["1996"], ax=ax, legend=True, cmap="turbo",
           legend_kwds={"label": "wheat yield", "orientation": "horizontal"},
           vmin=merge["1996"].min(), vmax=merge["1996"].max())

# Barplot for the year 2020

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
sns.barplot(data=merge, x="Country", y="2020[1]", ax=ax)
ax.tick_params(axis='x', labelrotation=90)
ax.set_ylabel("wheat yield")
ax.set_title("wheat yield by country in 2020")

# World map wheat yield 2020
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
merge.plot(column=merge["2020[1]"], ax=ax, legend=True, cmap='turbo',
           legend_kwds={'label': "wheat yield", 'orientation': "horizontal"},
           vmin=merge["2020[1]"].min(), vmax=merge["2020[1]"].max())

# Line Graph For The Entire Duration
fig, ax = plt.subplots(1, 1, figsize=(20, 12))
for i in range(10):
    temp = df.loc[i, :]
    labl = temp[1]
    wheat_data = temp[2:-1]
    ax.plot(wheat_data, label=labl)
    ax.tick_params(axis='x', labelrotation=90)
    ax.set_ylabel("wheat yield")
    ax.set_title("wheat yield for top 10 countries")
    ax.legend()