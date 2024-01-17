import pymongo
import json
from bson.json_util import loads
import pprint

nissin_json = open("./information.json", "r")
all_list = json.load(nissin_json)

nutrient_json = open("./nutrient.json", "r")
nutrient = json.load(nutrient_json)

pprint.pprint(nutrient)

client = pymongo.MongoClient("localhost", 27017)
db = client["nissin"]        # my_dbという新しいデータベースを作成 (my_dbが事前に存在しないことが前提)
col_nissin = db["product"]             # my_collectionという新しいコレクションを作成
col_nutrient = db["nutrient"]

col_nissin.drop()
col_nutrient.drop()

for i in range(len(all_list)):
    for j in range(len(all_list[i])):
        for k in range(len(all_list[i][j])):
            col_nissin.insert_one(all_list[i][j][k])

col_nutrient.insert_one({"nutrient":nutrient})

client.close()