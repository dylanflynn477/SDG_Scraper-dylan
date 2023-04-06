from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains as action

# Declaring global variables
global url
global options
global journal_list
global journal_issn_list
global journal_eissn_list
global journal
global query_results
global csvfile

csvfile = pd.read_csv('scopusjournals.csv')

journal_list = []
journal_issn_list = []
journal_eissn_list = []
query_results = []
journal = ""

for i in range(len(csvfile)):
    journal_list.append(csvfile.iat[i,0])
    journal_issn_list.append(csvfile.iat[i,1])
    journal_eissn_list.append(csvfile.iat[i,2])
#print(journal_list)
test = '1938-9590'
url = 'https://sju.primo.exlibrisgroup.com/discovery/search?query=issn,contains,' + test + ',AND&tab=Everything&search_scope=MyInst_and_CI&vid=01USCIPH_INST:SJU&mode=advanced&offset=0'
#url = 'https://sju.primo.exlibrisgroup.com/discovery/search?query=issn,contains,2168-1007,AND&tab=Everything&search_scope=MyInst_and_CI&vid=01USCIPH_INST:SJU&mode=advanced&offset=0'

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
def query_journal(url):
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
        driver.get(url)
        print("Page URL:", driver.current_url)
        print("Page Title:", driver.title)
        #elements = driver.find_elements(By.TAG_NAME, 'prm-brief-result')
        elements = driver.find_elements(By.TAG_NAME, 'prm-brief-result-container')
        highlighted_text = driver.find_elements(By.TAG_NAME, 'span')
        information = action(driver).move_to_element(highlighted_text[256]).click(highlighted_text[256]).perform()
        #driver.get(information)
        print(driver.current_url)
        #print(driver.title)
        print(f"Results: {highlighted_text}")
        #for i in range(len(highlighted_text)):
        #    if highlighted_text[i].text == "Academy of Management discoveries.":
        #        print(i)
            #print(highlighted_text[i].text)
        print(highlighted_text[256].text)
        if elements == []:
            print(f"Journal {journal} not found.")
            return 0
        else:
            print(f"Journal {journal} successfully found.")
            return 1
query_journal(url)

def find_all():
    for i in range(len(csvfile)):
        #I want to add a way to pass through empty spots.
        #if str(journal_issn_list[i]) == "nan":
        #    if str(journal_eissn_list[i]) == "nan":
        #        pass
        global query_loop_results
        query_loop_results = []
        url = 'https://sju.primo.exlibrisgroup.com/discovery/search?query=issn,contains,' + str(journal_issn_list[i]) + ',AND&tab=Everything&search_scope=MyInst_and_CI&vid=01USCIPH_INST:SJU&mode=advanced&offset=0'
        journal = journal_list[i]
        if query_journal(url) == 0:
            url = 'https://sju.primo.exlibrisgroup.com/discovery/search?query=issn,contains,' + str(journal_eissn_list[i]) + ',AND&tab=Everything&search_scope=MyInst_and_CI&vid=01USCIPH_INST:SJU&mode=advanced&offset=0'
            if query_journal(url) == 0:
                query_loop_results.append("No")
            else:
                query_loop_results.append("Yes")
        else:
            query_loop_results.append("Yes")

    d = {'Journal' : journal_list, 'Journal Exists' : query_loop_results}
    df = pd.DataFrame(data=d)
    print(df)