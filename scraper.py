import requests
from bs4 import BeautifulSoup
import csv
import pandas_datareader as pdr
import pandas as pd
from requests_html import HTMLSession

csvfile = pd.read_csv("journals.csv")
input = open("journals.csv", "rb")

global new_query_list
global new_journal_list
global query_results
new_query_list = []
new_journal_list = []
query_results = []

for i in range(len(csvfile)):
    new_url = str(csvfile.iat[i,0]).replace(" ", "%20")
    new_query_list.append(new_url)
    new_journal_list.append(str(csvfile.iat[i,0]))

df = {'Journals': new_journal_list, 'Queries': new_query_list}
def url(journal):
    return str("https://sju.primo.exlibrisgroup.com/discovery/search?query=any,contains," + journal + "&tab=Everything&search_scope=MyInst_and_CI&vid=01USCIPH_INST:SJU&offset=0")
#for i in range(len(new_query_list)):
#    url(new_query_list[i])
#page = requests.get(url(new_query_list[1]))   
#request = BeautifulSoup(page.content, "xml") 
#print(request)

session = HTMLSession()
r = session.get(url(new_query_list[1]))
r.html.render()

#for i in range(len(csvfile)):
    #page = requests.get(url(csvfile.iat[i,0]))
    #request = BeautifulSoup(page.content, "html.parser")
    #print(request)
