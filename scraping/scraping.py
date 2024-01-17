from bs4 import BeautifulSoup
import requests
import re
import math
import pprint
import pymongo
import json
from bson.json_util import loads

HEADERS = {"User-Agent": "Mozilla/5.0"}
main_response = requests.get("https://www.nissin.com/jp/products/items/index.html", headers=HEADERS)
main_soup = BeautifulSoup(main_response.content, "lxml")
main_table = main_soup.select_one("div.ns-items-list")

# all_list : 3次元 list
# category - label - element{辞書}
all_list = list()

nutrient_text_list = {}

# 正規表現を用いて<h2>タグ区切りで分割　https://qiita.com/4geru/items/8feebc0fc14d54fc30f6
category_split = re.split(r"<h2(.*?)</h2>|</div>\Z", str(main_table))[1:-1]
for i in range(math.floor(len(category_split) / 2)):
    # 各カテゴリー名
    category_name = category_split[i * 2][category_split[i * 2].find(">")+1:]
    print(category_name)
    # labelごとに element list を格納する list
    label_list = list()
    category = category_split[i * 2 + 1]
    # 正規表現を用いて<h3>タグ区切りで分割
    label_split = re.split(r"<h3(.*?)</h3>|\Z", str(category))[1:-1]
    for j in range(math.floor(len(label_split) / 2)):
        # 各ラベル名
        label_name = label_split[j * 2][label_split[j * 2].find("<em>")+4:label_split[j*2].find("</em>")]
        print(category_name + "-" + label_name)
        label = label_split[j * 2 + 1]
        soup = BeautifulSoup(label, "lxml")
        li_list = soup.find_all("li")
        # 各商品ごとに辞書形式で情報を格納
        element_list = list()
        for element in li_list:
            a = element.select_one("a")
            #
            # 情報の抽出
            #
            id = a.get("href").replace("./", "")
            url = "https://www.nissin.com/jp/products/items/" + id
            image = a.find("img").get("src")
            text = a.find("strong").text
            #
            # URL先のデータ取得
            #
            response = requests.get(url , headers=HEADERS)
            soup = BeautifulSoup(response.content, "lxml")
            table = soup.select_one("div.ns-single-body--item")
            #
            # 主要な情報
            #
            main = table.select_one(".ns-single-body-main").select_one(".dl-table.item-spec")
            main_list = {"price":None, "capacity":None, "region":None, "JAN":None, "packing":None, "note":None}
            main_list_label = ["価格", "price", "内容量", "capacity", "発売地域", "region", "JANコード", "JAN", "荷", "packing", "note"]
            for dl in main.select("dl")[0:]:
                flag = True
                for i in range(5):
                    if main_list_label[i * 2] in str(dl.select_one("dt").text):
                        main_list[main_list_label[i * 2 + 1]] = dl.select_one("dd").text
                        flag = False
                        break
                if flag:
                    main_list[main_list_label[10]] = re.sub(r"(\n)|(\t)|(\s)", "", dl.select_one("dt").text) + re.sub(r"(\n)|(\t)|(\s)", "", dl.select_one("dd").text)
                    if len(main_list[main_list_label[10]]) == 0:
                        # pprint.pprint(dl.select_one("img")["alt"])
                        main_list[main_list_label[10]] = dl.select_one("img")["alt"]
            #
            # 栄養成分表示
            #
            nutrients = table.select_one("#nutrients")
            if nutrients == None:
                nutrients = table.select_one(".ns_products_item-single-nutrients.js-products-items-panel")
                if nutrients != None:
                    print("##W id #nutrients not found: " + str({"url":url, "image":image, "text":text}))
            # 格納変数
            element_text = None
            element_nutrient_list = list()
            if nutrients == None:
                print("##E utrient table not found: " + str({"url":url, "image":image, "text":text}))
                element_nutrient_list = None # 存在しない場合はNone
            else:
                element_text = nutrients.select_one("h2").text
                for nutrient_table in nutrients.select("table")[0:]:
                    breakdown_list = list()
                    for tr in nutrient_table.select("tr")[0:]:
                        tr = BeautifulSoup(str(tr).replace("エネルギー", "熱量").replace("たん白質", "たんぱく質").replace("たん白質", "たんぱく質").replace("ナトリウム", "食塩相当量"), "lxml")
                        if (0 < len(breakdown_list)) & ("is-breakdown" not in str(tr)):
                            element_nutrient_list.append(breakdown_list)
                            breakdown_list = list()
                        if "with-breakdown" in str(tr):
                            element_nutrient_list.append({"nutrient":tr.select_one("th").text, "value":re.sub(r"(\n)|(\t)|(\s)|[^\d.]", "", tr.select_one("td").text), "unit":re.sub(r"(\n)|(\t)|(\s)|[0-9.]", "", tr.select_one("td").text)})
                            if tr.select_one("th").text not in nutrient_text_list:
                                nutrient_text_list[tr.select_one("th").text] = 0
                        elif "is-breakdown" not in str(tr):
                            element_nutrient_list.append({"nutrient":tr.select_one("th").text, "value":re.sub(r"(\n)|(\t)|(\s)|[^\d.]", "", tr.select_one("td").text), "unit":re.sub(r"(\n)|(\t)|(\s)|[0-9.]", "", tr.select_one("td").text)})
                            if tr.select_one("th").text not in nutrient_text_list:
                                nutrient_text_list[tr.select_one("th").text] = 0
            #
            # 追加
            #
            element_list.append({"id":id, "name":text, "category":category_name, "label":label_name, "url":url, "image":image, "main":main_list, "nutrient_text":element_text, "nutrient":element_nutrient_list})
        label_list.append(element_list)

    # all_listの追加
    all_list.append(label_list)

all_json = json.dumps(all_list, indent=5, ensure_ascii=False)
f = open('information.json', 'w', encoding='UTF-8')
f.write(all_json)

pprint.pprint(nutrient_text_list)
