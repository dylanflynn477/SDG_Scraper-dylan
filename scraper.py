import requests
from bs4 import BeautifulSoup
import csv
import pandas_datareader as pdr
import pandas as pd

csvfile = pd.read_csv("journals.csv")
for i in range(len(csvfile)):
    new_url = str(csvfile.iat[i,0]).replace(" ", "%20")
    
    print(new_url)

def url(journal):
    return "https://sju.primo.exlibrisgroup.com/discovery/search?query=any,contains," + journal + "&tab=Everything&search_scope=MyInst_and_CI&vid=01USCIPH_INST:SJU&offset=0"


#for i in range(len(csvfile)):
    #page = requests.get(url(csvfile.iat[i,0]))
    #request = BeautifulSoup(page.content, "html.parser")
    #print(request)
