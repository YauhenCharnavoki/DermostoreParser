import requests
from bs4 import BeautifulSoup
import csv
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument ('-u')
url = parser.parse_args (sys.argv[1:]).u

headers = {
    "Accept": "*/*",
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}

req = requests.get(url, headers=headers)
src = req.text

soup = BeautifulSoup(src, "lxml")

product_name = soup.find("h1", class_="productName_title").text
brand_name = soup.find("div", class_="productBrandLogo").find("img").get("title")
price = soup.find("p", class_="productPrice_price").text.strip()
main_image_url = list(map(lambda x: x.find("img").get("src"), soup.find_all("button", class_="athenaProductImageCarousel_thumbnailWrapper")))
product_overview_block = soup.find_all("div", class_="athenaProductPageSynopsisContent")[0].text
how_to_use_block = soup.find_all("div", class_="athenaProductPageSynopsisContent")[1].text.strip()

with open("task.csv", mode="a", encoding="utf-8") as file:
    fieldnames=[
        "Product name", "Brand name", "Price", 
        "Main image url", "Product overview block", "How to use block"
        ]
    file_writer = csv.DictWriter(file, delimiter = ",", lineterminator="\r", fieldnames=fieldnames)
    file_writer.writeheader()
    file_writer.writerow({
        "Product name": product_name, "Brand name": brand_name, "Price": price, "Main image url": main_image_url, 
        "Product overview block": product_overview_block, "How to use block": how_to_use_block
        })
