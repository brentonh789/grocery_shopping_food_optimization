import requests
import pandas as pd
import os
from pandas.io.json import json_normalize 
from dotenv import load_dotenv

load_dotenv()

#create api query to pull food data
API_KEY = os.getenv('API_KEY')
str_http = ('https://api.nal.usda.gov/fdc/v1/foods/search?api_key=')
str_query = '&query=Beef&brandOwner=Tyson'
get_query = str_http + API_KEY + str_query

#convert api respones to json
response = requests.get(get_query)
response_json = response.json()

#flatten data
df_foods = pd.json_normalize(data=response_json, record_path=['foods'])
df_nutrition =  pd.json_normalize(data=response_json, record_path=['foods','foodNutrients'],meta=[['totalHits'],['totalHits','fdcId']])
df_nutrition = df_nutrition.rename(columns={'totalHits.fdcId':'fdcId'})
df_food_nutrition = pd.merge(df_foods, df_nutrition, how='inner', on='fdcId')

print(df_food_nutrition.head(5))