import requests
from bs4 import BeautifulSoup
import csv
import pandas_datareader as pdr
import pandas as pd
from requests_html import HTMLSession

csvfile = pd.read_csv("journals.csv")

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
#page = requests.get("https://sites.sju.edu/library/")  
#request = BeautifulSoup(page.content, "xml") 
#print(request)

session = HTMLSession()
#print(url(new_query_list[1]))

for i in range(len(csvfile)):
    r = session.get(url(new_query_list[i]))
    r.html.render(sleep=1, keep_page=False, scrolldown=1)
    try:
        top_result = r.html.find('mark'),#containing=str(csvfile.iat[0,0]))
        print(top_result)
        print(top_result[0][0])
        print(top_result[0][0].text)
        df['Queries'][i] = top_result[0][0].text
        #print(r.content)
    except IndexError:
        print(f"Journal {csvfile.iat[i,0]} not found")
    except AttributeError:
        print("AttributeError")
    except KeyboardInterrupt:
        print(df)
        quit()
#with open("scraper.png","wb") as fp:
#    fp.write(r.html.render())
#for i in range(len(csvfile)):
    #page = requests.get(url(csvfile.iat[i,0]))
    #request = BeautifulSoup(page.content, "html.parser")
    #print(request)
