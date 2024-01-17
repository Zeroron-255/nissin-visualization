# coding: utf-8

MONGO_URI = "mongodb://localhost/i2110707"  # "mongodb://接続先MongoDBのドメイン(localhost)/DB名(nobel_prize)"
X_DOMAINS = "*"               # このAPIへのアクセス許可ドメイン
HATEOAS = False               # Restful拡張の有無
PAGINATION = False            # ページ送りの有無
URL_PREFIX = "api"            # このAPIのURL接頭辞 http://localhost:50000/api 
DOMAIN = {"nutrient":{    # 公開するmongodbコレクション名
    "item_title": "nutrient",  # APIで取得できるJSONファイルにおけるkey
    "url":"nutrient",          # このAPIの公開用のURL．ここでは http://localhost:50000/api/winners
    "schema":{
    	    "nutrient":{"type":"list", "schema":{"nutrient":"string", "value":"string"}}
    	}
    },
    "nissin":{    # 公開するmongodbコレクション名
    "item_title": "nissin",  # APIで取得できるJSONファイルにおけるkey
    "url":"nissin",          # このAPIの公開用のURL．ここでは http://localhost:50000/api/winners
    "schema":{
            "id":{"type":"string"},
            "name":{"type":"string"},
            "category":{"type":"string"},
            "label":{"type":"string"},
            "url":{"type":"string"},
            "image":{"type":"string"},
            "main":{
            	"type":"dict", "schema":{
                    "price":{"type":"string"},
                    "capacity":{"type":"string"},
                    "region":{"type":"string"},
                    "JAN":{"type":"string"},
                    "packing":{"type":"string"},
                    "note":{"type":"string"}
                }
            },
            "nutrient_text":{"type":"string"},
            "nutrient":{"type":"list", "schema":{"nutrient":"string", "value":"string"}}
        }
    }
}
