from pymongo import MongoClient
import csv
import pandas as pd

mongoclient = MongoClient("mongodb://localhost:27017/")
db = mongoclient['apssensor']
collection = db['sensor']

# def csv_to_json(filename):
#     data = pd.read_csv(filename)
#     return data.to_dict(orient="records")

df = pd.read_csv("aps_failure.csv")
data = df.to_dict(orient="records")
collection.insert_many(data)

# db.collection.insert_many(csv_to_json("aps_failure.csv"))
# print(csv_to_json("aps_failure.csv"))