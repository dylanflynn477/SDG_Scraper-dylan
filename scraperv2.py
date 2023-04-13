from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains as action
import time 

# Declaring global variables
global url
global options
global journal_list
global journal_issn_list
global journal_eissn_list
global journal
global query_results
global abstract
global keywords
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
url = 'https://sju.primo.exlibrisgroup.com/discovery/search?query=issn,contains,' + test + ',AND&pfilter=rtype,exact,articles,AND&tab=Everything&search_scope=MyInst_and_CI&vid=01USCIPH_INST:SJU&mode=advanced&offset=0'
#url = 'https://sju.primo.exlibrisgroup.com/discovery/search?query=issn,contains,2168-1007,AND&pfilter=rtype,exact,articles,AND&tab=Everything&search_scope=MyInst_and_CI&vid=01USCIPH_INST:SJU&mode=advanced&offset=0'

## 256 and 258 are the numbers that work when running a query. I don't know why that is, but they do.

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
def query_journal(url):
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
        driver.get(url)
        print("Page URL:", driver.current_url)
        print("Page Title:", driver.title)
        #elements = driver.find_elements(By.TAG_NAME, 'prm-brief-result')
        elements = driver.find_elements(By.TAG_NAME, 'prm-brief-result-container')
        #highlighted_text = driver.find_elements(By.TAG_NAME, 'span')
        #print(highlighted_text[258].text)
        #information = action(driver).move_to_element(highlighted_text[258]).double_click(highlighted_text[258]).perform()
        #information = action(driver).move_to_element(highlighted_text[258]).click(highlighted_text[258]).perform()
        #driver.get(information)
        print(driver.current_url)
        #print(driver.title)
        #print(f"Results: {highlighted_text}")
        #for i in range(len(highlighted_text)):
        #    if highlighted_text[i].text == "Academy of Management discoveries.":
        #        print(i)
            #print(highlighted_text[i].text)
        #print(highlighted_text[256].text)
        if elements == []:
            print(f"Journal {journal} not found.")
            return 0
        else:
            print(f"Journal {journal} successfully found.")
            return 1
#query_journal(url)

def find_all_journals():
    global query_loop_results
    query_loop_results = []
    for i in range(len(csvfile)):
        try:
            #I want to add a way to pass through empty spots.
            #if str(journal_issn_list[i]) == "nan":
            #    if str(journal_eissn_list[i]) == "nan":
            #        pass
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
            print(query_loop_results)
        except KeyboardInterrupt:
            print(journal_list)
            print(query_loop_results)
            d = {'Journal' : journal_list, 'Journal Exists' : query_loop_results}
            df = pd.DataFrame(data=d)
            print(df)


    d = {'Journal' : journal_list, 'Journal Exists' : query_loop_results}
    df = pd.DataFrame(data=d)
    print(df)

#find_all_journals()

JSPath = 'document.querySelector("#SEARCH_RESULT_RECORDID_cdi_crossref_primary_10_5465_amd_2018_0084 > div.result-item-text.layout-fill.layout-column.flex > prm-brief-result > h3 > a > span > prm-highlight > span")'
XPath = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[1]/prm-search-result-list/div/div[2]/div/div[1]/prm-brief-result-container/div[1]/div[3]/prm-brief-result/h3/a/span/prm-highlight/span'
Element = '<span ng-if="::(!$ctrl.isEmailMode())" ng-bind-html="$ctrl.highlightedText" dir="auto">Artificial Intelligence in Organizations: New Opportunities for Phenomenon-Based Theorizing</span>'
ButtonXPath = '//*[@id="SEARCH_RESULT_RECORDID_cdi_crossref_primary_10_46697_001c_67966"]/div[3]/div[2]/prm-search-result-availability-line/div/div/button'
AbstractXPath = '/html/body/div[4]/div[1]/div/div[7]/div[3]/div/div/div[2]/article/div[4]/div/div[2]/div[2]/div[1]/div'

def text(query):
    for i in range(len(query)):
        print(query[i].text)

def query_journals():
    titles = []
    abstracts = []
    keywords = []
    authors = []
    journal_origin = []
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
        print(url)
        driver.get(url)
        #trial = driver.find_elements(By.TAG_NAME, 'prm-search-result-list')
        articles = driver.find_elements(By.XPATH, '//prm-brief-result-container')
        article_information = driver.find_elements(By.XPATH, '//span/prm-highlight/span')
        online_access = driver.find_elements(By.XPATH, '//prm-search-result-availability-line/div/div/button')
        action(driver).move_to_element(online_access[0]).click(online_access[0]).perform()
        time.sleep(5.0)
        # Switching to open journal tab
        driver.switch_to.window(driver.window_handles[1])
        abstract = driver.find_elements(By.XPATH, '//article/div[4]/div/div[2]/div[2]/div[1]/div')
        print(abstract[0].text)
        abstracts.append(abstract[0].text)
        #for j in range(0,100):
        #    if abstract[j].text != "":
        #        print(j)
            #print(abstract[j].text)
        #for handle in driver.window_handles:
        #    driver.switch_to.window(handle)
        #    print(driver.current_url)
        """
        for i in range(int(len(article_information)/3)):
            titles.append(article_information[i*3].text)
            authors.append(article_information[i*3 + 1].text)
            journal_origin.append(article_information[i*3 + 2])
        #print(titles)
        #print(authors)
        #action(driver).move_to_element(element).double_click(highlighted_text[258]).perform()
        csvlist = {'Article Titles' : titles , 'Authors' : authors , 'Keywords' : keywords , 'Abstracts' : abstracts , 'Journal Origin' : journal_origin}
        print(csvlist)
        return csvlist
        """
query_journals()