import pymongo
import json
from bson.json_util import loads
import pprint

client = pymongo.MongoClient("localhost", 27017)
db = client["i2110707"]        # my_dbという新しいデータベースを作成 (my_dbが事前に存在しないことが前提)
col_nissin = db["nissin"]             # my_collectionという新しいコレクションを作成
col_nutrient = db["nutrient"]

pprint.pprint(list(col_nissin.find({})))
pprint.pprint(list(col_nutrient.find({})))

all_json = json.dumps(list(col_nissin.find({})), indent=5, ensure_ascii=False)
f = open('col_nissin.json', 'w', encoding='UTF-8')
f.write(all_json)