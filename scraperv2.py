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
        #driver.get(information)
        print(driver.current_url)
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

#JSPath = 'document.querySelector("#SEARCH_RESULT_RECORDID_cdi_crossref_primary_10_5465_amd_2018_0084 > div.result-item-text.layout-fill.layout-column.flex > prm-brief-result > h3 > a > span > prm-highlight > span")'
#XPath = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[1]/prm-search-result-list/div/div[2]/div/div[1]/prm-brief-result-container/div[1]/div[3]/prm-brief-result/h3/a/span/prm-highlight/span'
#Element = '<span ng-if="::(!$ctrl.isEmailMode())" ng-bind-html="$ctrl.highlightedText" dir="auto">Artificial Intelligence in Organizations: New Opportunities for Phenomenon-Based Theorizing</span>'
#ButtonXPath = '//*[@id="SEARCH_RESULT_RECORDID_cdi_crossref_primary_10_46697_001c_67966"]/div[3]/div[2]/prm-search-result-availability-line/div/div/button'
#AbstractXPath = '/html/body/div[4]/div[1]/div/div[7]/div[3]/div/div/div[2]/article/div[4]/div/div[2]/div[2]/div[1]/div'
#KeywordXPath = '/html/body/div[4]/div[1]/div/div[7]/div[3]/div/div/div[2]/article/div[4]/div/div[6]/div/div[1]/div/text/div[2]/div/p[1]'

#NextPageXPath = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[1]/prm-search-result-list/div/div[2]/prm-page-nav-menu/div/div/div[1]/div[3]/a/prm-icon/md-icon'

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
        base_window = driver.window_handles[0]
        print(url)
        driver.get(url)
        #trial = driver.find_elements(By.TAG_NAME, 'prm-search-result-list')
        articles = driver.find_elements(By.XPATH, '//prm-brief-result-container')
        article_information = driver.find_elements(By.XPATH, '//span/prm-highlight/span')
        online_access = driver.find_elements(By.XPATH, '//prm-search-result-availability-line/div/div/button')
        for i in range(len(online_access)):
            #try:
                action(driver).move_to_element(online_access[i]).click(online_access[i]).perform()
                time.sleep(5.0)
                # Switching to open journal tab
                try:
                    driver.switch_to.window(driver.window_handles[1])
                except IndexError:
                    action(driver).move_to_element(online_access[i]).click(online_access[i]).perform()
                    driver.switch_to.window(driver.window_handles[1])
                abstract = driver.find_elements(By.XPATH, '//article/div[4]/div/div[2]/div[2]/div[1]/div')
                keyword = driver.find_elements(By.XPATH, '//div/div[6]/div/div[1]/div/text/div[2]/div/p[1]')
                if abstract and keyword:
                    print(keyword)
                    print(keyword[0].text.replace('Keywords: ', ''))
                    #print(abstract[0].text)
                    abstracts.append(abstract[0].text)
                    keywords.append(keyword[0].text.replace('Keywords: ', ''))
                else:
                    abstracts.append(None)
                    keywords.append(None)
                driver.close()
                driver.switch_to.window(base_window)
                time.sleep(5.0)
            #except IndexError:
            #    print(f"Index error at list number {i}")
            #    csvlist = {'Article Titles' : titles , 'Authors' : authors , 'Keywords' : keywords , 'Abstracts' : abstracts , 'Journal Origin' : journal_origin}
            #    print(csvlist)
            #    return csvlist
        # Switching to open journal tab
        #driver.switch_to.window(driver.window_handles[1])
        #abstract = driver.find_elements(By.XPATH, '//article/div[4]/div/div[2]/div[2]/div[1]/div')
        #keyword = driver.find_elements(By.XPATH, '//div/div[6]/div/div[1]/div/text/div[2]/div/p[1]')
        #keyword[0].text.lstrip('Keywords: ')
        #for j in range(0,100):
        #    if abstract[j].text != "":
        #        print(j)
            #print(abstract[j].text)
        #for handle in driver.window_handles:
        #    driver.switch_to.window(handle)
        #    print(driver.current_url)
        for i in range(int(len(article_information)/3)):
            titles.append(article_information[i*3].text)
            authors.append(article_information[i*3 + 1].text)
            journal_origin.append(article_information[i*3 + 2].text)
        #print(titles)
        #print(authors)
        #action(driver).move_to_element(element).double_click(highlighted_text[258]).perform()
        csvlist = {'Article Titles' : titles , 'Authors' : authors , 'Keywords' : keywords , 'Abstracts' : abstracts , 'Journal Origin' : journal_origin}
        print(csvlist)
        return csvlist
#query_journals()
#csvdf = pd.DataFrame(data=query_journals())
#print(csvdf)
#csvdf.to_csv('output.csv')

def debug_article(i):
    titles = []
    abstracts = []
    keywords = []
    authors = []
    journal_origin = []
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
        base_window = driver.window_handles[0]
        print(url)
        driver.get(url)
        #trial = driver.find_elements(By.TAG_NAME, 'prm-search-result-list')
        articles = driver.find_elements(By.XPATH, '//prm-brief-result-container')
        article_information = driver.find_elements(By.XPATH, '//span/prm-highlight/span')
        online_access = driver.find_elements(By.XPATH, '//prm-search-result-availability-line/div/div/button')
        action(driver).move_to_element(online_access[i]).click(online_access[i]).perform()
        time.sleep(5.0)
        # Switching to open journal tab
        driver.switch_to.window(driver.window_handles[1])
        abstract = driver.find_elements(By.XPATH, '//article/div[4]/div/div[2]/div[2]/div[1]/div')
        keyword = driver.find_elements(By.XPATH, '//div/div[6]/div/div[1]/div/text/div[2]/div/p[1]')
        if abstract and keyword:
            print(keyword)
            print(keyword[0].text)
            #print(abstract[0].text)
            abstracts.append(abstract[0].text)
            keywords.append(keyword[0].text)
        else:
            abstracts.append(None)
            keywords.append(None)
            print("Abstract/keywords not found")
        driver.close()
        driver.switch_to.window(base_window)
    # Switching to open journal tab
    #driver.switch_to.window(driver.window_handles[1])
    #abstract = driver.find_elements(By.XPATH, '//article/div[4]/div/div[2]/div[2]/div[1]/div')
    #keyword = driver.find_elements(By.XPATH, '//div/div[6]/div/div[1]/div/text/div[2]/div/p[1]')
    #keyword[0].text.lstrip('Keywords: ')
    #for j in range(0,100):
    #    if abstract[j].text != "":
    #        print(j)
        #print(abstract[j].text)
    #for handle in driver.window_handles:
    #    driver.switch_to.window(handle)
    #    print(driver.current_url)
    #print(titles)
    #print(authors)
    #action(driver).move_to_element(element).double_click(highlighted_text[258]).perform()
#debug_article(4)

#ButtonPage1 = /html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[1]/prm-search-result-list/div/div[2]/prm-page-nav-menu/div/div/div[1]/div[3]/a
#ButtonPage 2 = /html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[1]/prm-search-result-list/div/div[2]/prm-page-nav-menu/div/div/div[1]/div[3]/a/prm-icon/md-icon
#url = 'https://sju.primo.exlibrisgroup.com/discovery/search?query=issn,contains,1938-9590,AND&pfilter=rtype,exact,articles,AND&tab=Everything&search_scope=MyInst_and_CI&vid=01USCIPH_INST:SJU&mode=advanced&offset=10'

def next_page():
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
        global url
        driver.get(url)
        nextbutton = driver.find_elements(By.XPATH, '//prm-page-nav-menu/div/div/div[1]/div[3]/a/prm-icon/md-icon')
        #nextbutton = driver.find_elements(By.CLASS_NAME, 'prm-icon')
        print(nextbutton)
        print(driver.current_url)
        action(driver).move_to_element(nextbutton[0]).click(nextbutton[0]).perform()
        #action(driver).move_to_element(nextbutton[0]).click(nextbutton[0]).perform()
        print(driver.current_url)
        url = driver.current_url
        
next_page()
next_page()