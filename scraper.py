import requests
from bs4 import BeautifulSoup
import csv

csvfile = csv.open("journals.csv")


class setup():
    def searchquery(journal):
        url = "https://sju.primo.exlibrisgroup.com/discovery/search?query=any,contains," + journal + "&tab=Everything&search_scope=MyInst_and_CI&vid=01USCIPH_INST:SJU&offset=0"

s = setup()

page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

print(soup)

print(page.text)

