import requests
from bs4 import BeautifulSoup
import csv

csvfile = csv.open("journals.csv")


def url(journal):
    return "https://sju.primo.exlibrisgroup.com/discovery/search?query=any,contains," + journal + "&tab=Everything&search_scope=MyInst_and_CI&vid=01USCIPH_INST:SJU&offset=0"


for i in range(csvfile):
    page = requests.get(url(csvfile.iat[i]))
    BeautifulSoup(page.content, "html.parser")
