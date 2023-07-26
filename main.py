import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from tabulate import tabulate

url = "https://raw.githubusercontent.com/wesm/pydata-book/2nd-edition/datasets/usda_food/database.json"
response = requests.get(url)
if response.status_code == 200:
    with open("./usda_food/database.json", "wb") as file:
        file.write(response.content)
        print("File downloaded successfully.")
else:
   print("Failed to download the file.")
with open("./usda_food/database.json", "r") as file:
    db = json.load(file)
print("Number of records in the database:", len(db))
sns.set_style("whitegrid")
print("Type of database:", type(db))
print("Type of first element:", type(db[0]))
# db is a list of dictionaries
print("keys of the first dictionary:" , db[0].keys())
print("First nutrient of the first record:", db[0]['nutrients'][0])
print("Second nutrient of the first record:", db[0]['nutrients'][1])

nutrients = pd.DataFrame(db[0]['nutrients'])
# Extract the nutrients data from the first record
nutrients = nutrients[['description', 'group', 'units', 'value']]
# Select specific columns from the nutrients DataFrame
print(nutrients.head(10))

info_keys = ['description', 'group', 'id', 'manufacturer']
# Specify the columns to include in the 'info' DataFrame
info = pd.DataFrame(db, columns=info_keys)
# Create the 'info' DataFrame with the specified columns
print(info[:5])
# Display the first 5 rows of the 'info' DataFrame

info.info()

df = pd.DataFrame(db)
print("keys of the first dictionary:" , db[0].keys())

table = tabulate([df.iloc[0]], headers='keys', tablefmt='psql')
#To print all records from your DataFrame df in a table format
print(table)

plt.figure(figsize=(12, 8))
_ = sns.barplot(x=pd.value_counts(info.description)[:15], y=pd.value_counts(info.description)[:15].index)
_ = plt.xlabel("Counts")
plt.show()

print(db[0]['nutrients'][0]['value'])
# for analysis of nutrients
nutrients =[]
for i in db:
    fnut = pd.DataFrame(i['nutrients'])
    fnut["id"] = i['id']
    nutrients.append(fnut)
print(type(nutrients))
nutrients = pd.concat(nutrients,ignore_index=True)
nutrients = nutrients[["description", "group", "units", "value", "id"]]
print(type(nutrients))
print(nutrients.head(20))

print(nutrients.duplicated().sum())
nutrients = nutrients.drop_duplicates()
col_mapping = {'description': 'food', 'group': 'fgroup'}
info = info.rename(columns=col_mapping, copy=False)
info.info()

col_mapping = {'description': 'nutrient', 'group': 'nutgroup'}
nutrients = nutrients.rename(columns=col_mapping, copy=False)
nutrients.info()

ndata = pd.merge(nutrients,info,on='id', how='outer')
ndata.info()
print(ndata.iloc[30000])

result = ndata.groupby(['nutrient', 'fgroup'])['value'].quantile(0.5)
print(result.index.values)

_ = result['Protein'].sort_values().plot(kind="barh", figsize=(15, 10),title="Median Protein values by nutrient group")
plt.show()

by_nutrient = ndata.groupby(['nutgroup','nutrient'])
get_max = lambda x: x.loc[x.value.idxmax()]
get_min = lambda x: x.loc[x.value.idxmin()]
max_foods = by_nutrient.apply(get_max)[['value','food']]
max_foods.food = max_foods.food.str[:50]
print(max_foods)

max_foods_amino = max_foods.loc['Amino Acids']['food']
print(max_foods_amino)
#print(max_foods.loc['Amino Acids']['food'])

