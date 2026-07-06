import requests
from bs4 import BeautifulSoup
import csv
import pandas_datareader as pdr
import pandas as pd
from requests_html import HTMLSession

csvfile = pd.read_csv("scopusjournals.csv")

global new_query_list
global new_journal_list
global query_results
new_query_list = []
new_journal_list = []
query_results = []

journal_list = []

for i in range(len(csvfile)):
    journal_list.append(csvfile.iat[i,0])
    query_results.append("NaN")
#print(journal_list)
#print(query_results)

#for i in range(len(csvfile)):
    #new_url = str(csvfile.iat[i,0]).replace(" ", "%20")
#    new_url = str(csvfile.iat[i,1])
#    new_query_list.append(new_url)
#    new_journal_list.append(str(csvfile.iat[i,0]))

df = {'Journals': journal_list, 'Journal Exists': query_results}
d = pd.DataFrame(data=df)
def url(journal):
    #return str("https://sju.primo.exlibrisgroup.com/discovery/search?query=any,contains," + journal + "&tab=Everything&search_scope=MyInst_and_CI&vid=01USCIPH_INST:SJU&offset=0")
    return str("https://sju.primo.exlibrisgroup.com/discovery/search?query=issn,contains," + str(journal) + ",AND&tab=Everything&search_scope=MyInst_and_CI&vid=01USCIPH_INST:SJU&mode=advanced&offset=0")

session = HTMLSession()

#for i in range(len(csvfile)):
#    r = session.get(url(new_query_list[i]))
#    r.html.render(sleep=1, keep_page=False, scrolldown=1)
#    try:
#        top_result = r.html.find('mark')#,containing=str(csvfile.iat[i,0]))
#        print(top_result)
#        print(top_result[0])
#        print(top_result[0].text)
#        df['Queries'][i] = top_result[0].text
#        #print(r.content)
#    except IndexError:
#        print(f"Journal {csvfile.iat[i,0]} not found")
#    except AttributeError:
#        print("AttributeError")
#    except KeyboardInterrupt:
#        print(df)
#        quit()

for i in range(len(csvfile)):
    if str(csvfile.iat[i,1]) != "":
        print(csvfile.iat[i,1])
        r = session.get(url(csvfile.iat[i,1]))
        #print(url(csvfile.iat[i,1]))
        issnquery = str(csvfile.iat[i,1])
    else:
        print("Print-ISSN empty")
        print(csvfile.iat[i,2])
        r = session.get(url(csvfile.iat[i,2]))
        issnquery = str(csvfile.iat[i,2])
    r.html.render(sleep=1, keep_page=False, scrolldown=1)
    try:
        top_result = r.html.find('prm-brief-result')#,containing=str(csvfile.iat[i,0]))
        #print(top_result[0].text)
        if str(top_result[0].text) != "":
            df['Journal Exists'][i] = "Yes"
            print(f"Journal {csvfile.iat[i,0]} exists")
        #print(top_result[0][0])
        #print(top_result[0][0].text)
        #df['Queries'][i] = top_result[0][0].text
        #print(r.content)
    except IndexError:
        try:
            print(f"Print-ISSN empty for {csvfile.iat[i,0]}. Attempting with E-ISSN:")
            print(csvfile.iat[i,2])
            r = session.get(url(csvfile.iat[i,2]))
            issnquery = str(csvfile.iat[i,2])
            r.html.render(sleep=1, keep_page=False, scrolldown=1)
            top_result = r.html.find('prm-brief-result')#,containing=str(csvfile.iat[i,0]))
        #print(top_result[0].text)
            if str(top_result[0].text) != "":
                df['Journal Exists'][i] = "Yes"
                print(f"Journal {csvfile.iat[i,0]} exists (2nd attempt)")
        except IndexError:
            print(f"Journal {csvfile.iat[i,0]} not found")
            df['Journal Exists'][i] = "No"
    except AttributeError:
        print("AttributeError")
    except TypeError:
        print("TypeError")
    except KeyboardInterrupt:
        print(df)
        d.to_csv("results.csv")
        quit()
print(df)
d.to_csv("results.csv")
