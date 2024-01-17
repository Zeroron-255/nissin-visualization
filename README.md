# Visualization application of Nissin Foods products
This application visualizes the nutrientional content of Nissin Foods producsts in a radar chart.<br>
This radar chart guves a numerical value for the percentage of nutrients requirements per day.<br>
And, this radar chart only displays nutrients intersection to the selected products.
![visualization application image](https://github.com/Zeroron-255/nissin-visualization/assets/98586574/650ad6ca-db61-4f87-990e-514d73eb3372)

# api
Data API File

# app
Visualization application files

# nissin
### contains database

・prodict: information on each product obtained by scraping

・nutrient: information on nutrients requirements per day from "https://www.otsuka.co.jp/cmt/nutrition/1day/"

# scraping
### contains scraping program

・scraping.py: program for scraping from "https://www.nissin.com/jp/products/items/index.html"

・mongo.py: program for containing scraping data to mongodb
