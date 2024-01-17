# coding: utf-8

from eve import Eve

app = Eve()

if __name__=='__main__':
    app.run(host='localhost', port=50001, debug=True)   #  データAPIを起動するポート番号．各自設定
