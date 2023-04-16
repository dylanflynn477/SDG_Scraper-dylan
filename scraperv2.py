from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains as action
import time 
import math
import os

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

#Page1NextPageXPath = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[1]/prm-search-result-list/div/div[2]/prm-page-nav-menu/div/div/div[1]/div[3]/a'
#NextPageXPath = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[1]/prm-search-result-list/div/div[2]/prm-page-nav-menu/div/div/div[1]/div[3]/a/prm-icon/md-icon'
#RequestableXPath = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[1]/prm-search-result-list/div/div[2]/div/div[1]/prm-brief-result-container/div[1]/div[3]/div[2]/prm-search-result-availability-line/div/div/button/span[2]/span'
#RequestableElement = '<span class="availability-status no_fulltext " ng-style="::$ctrl.getNgrsStyle()" ng-class="::{'text-rtl': $ctrl.switchToLtrString()}" translate="delivery.code.no_fulltext" translate-values="::$ctrl.getPlaceHolders($ctrl.result)" translate-compile="">Requestable</span>'
#SearchButton = '/html/body/primo-explore/div/prm-explore-main/div/prm-search-bar/div[1]/div/div[2]/div/prm-advanced-search/div/md-tabs/md-tabs-content-wrapper/md-tab-content/div/form/div[2]/md-card/div/div[2]/button/span'

def text(query):
    for i in range(len(query)):
        print(query[i].text)

# Next page query (useful in getting a certain page)
def next_page():
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
        global url
        driver.get(url)
        nextbutton = driver.find_elements(By.XPATH, '//prm-page-nav-menu/div/div/div[1]/div[3]/a/prm-icon/md-icon')
        #resultscount = driver.find_elements(By.XPATH, '//md-input-container/md-select/md-select-value/span')
        # 34 shows the results count.
        #resultscount[34].text
        if nextbutton:
            #nextbutton = driver.find_elements(By.CLASS_NAME, 'prm-icon')
            print(nextbutton)
            print(driver.current_url)
            # Double click element in case it doesn't register the first time, because the library website is trash
            oldurl = driver.current_url
            action(driver).move_to_element(nextbutton[0]).click(nextbutton[0]).perform()
            if driver.current_url == oldurl:
                action(driver).move_to_element(nextbutton[0]).click(nextbutton[0]).perform()
            print(driver.current_url)
            url = driver.current_url
        else:
            pass

def find_next_page():
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
        global url
        driver.get(url)
        #nextbutton = driver.find_elements(By.XPATH, '//div/div[1]/div[3]/a')
        nextbutton = driver.find_elements(By.XPATH, '//prm-page-nav-menu/div/div/div[1]/div[3]/a/prm-icon/md-icon')
        #resultscount = driver.find_elements(By.XPATH, '//md-input-container/md-select/md-select-value/span')
        # 34 shows the results count.
        #resultscount[34].text
        if nextbutton:
            #nextbutton = driver.find_elements(By.CLASS_NAME, 'prm-icon')
            print(nextbutton)
            print(driver.current_url)
            # Double click element in case it doesn't register the first time, because the library website is trash
            oldurl = driver.current_url
            action(driver).move_to_element(nextbutton[0]).click(nextbutton[0]).perform()
            time.sleep(1.0)
            if driver.current_url == oldurl:
                action(driver).move_to_element(nextbutton[0]).click(nextbutton[0]).perform()
            print(driver.current_url)
            url = driver.current_url
        else:
            pass
#find_next_page()

# Solving for those journals that do NOT have online access. This process is significantly more complicated since it involves pulling information from a csv file.
def requestables():
    test = '1938-9590'
    url = 'https://sju.primo.exlibrisgroup.com/discovery/search?query=issn,contains,' + test + ',AND&pfilter=rtype,exact,articles,AND&tab=Everything&search_scope=MyInst_and_CI&vid=01USCIPH_INST:SJU&mode=advanced&offset=0'
    titles = []
    abstracts = []
    keywords = []
    authors = []
    journal_origin = []
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
        base_window = driver.window_handles[0]
        print(url)
        driver.get(url)
        time.sleep(1.0)
        # God awful code to figure out how many articles are in the journal
        results = driver.find_element(By.XPATH, '//prm-search-result-page-range/div/md-input-container/md-select/md-select-value')
        results = results.text
        results = results.lstrip("1-10 of ")
        results = results.rstrip(" Results")
        results = int(results)
        results = math.floor(results/10)
        # End God awful code
        for i in range(results+1):
            driver.get(url)
            time.sleep(5.0)
            #trial = driver.find_elements(By.TAG_NAME, 'prm-search-result-list')
            articles = driver.find_elements(By.XPATH, '//prm-brief-result-container')
            selectbutton1 = driver.find_elements(By.XPATH, '//div[2]/button[2]/prm-icon/md-icon')
            action(driver).move_to_element(selectbutton1[0]).click(selectbutton1[0]).perform()
            time.sleep(1.0)
            selectbutton2 = driver.find_elements(By.XPATH, '//md-toolbar/div[1]/md-checkbox/div[1]')
            action(driver).move_to_element(selectbutton2[0]).click(selectbutton2[0]).perform()
            time.sleep(1.0)
            optionsbutton = driver.find_elements(By.XPATH, '//div[4]/div[3]/button/prm-icon/md-icon')
            action(driver).move_to_element(optionsbutton[0]).click(optionsbutton[0]).perform()
            #print(selectbutton1)
            #print(selectbutton2)
            #article_information = driver.find_elements(By.XPATH, '//span/prm-highlight/span')
            #online_access = driver.find_elements(By.XPATH, '//prm-search-result-availability-line/div/div/button')
            time.sleep(1.0)
            exporttoexcel = driver.find_elements(By.XPATH, '//div/li[5]/button/span/div/span')
            action(driver).move_to_element(exporttoexcel[0]).click(exporttoexcel[0]).perform()
            time.sleep(1.0)
            filetype = driver.find_element(By.XPATH, '//div[1]/div[2]/md-input-container/md-select')
            action(driver).move_to_element(filetype).click(filetype).perform()
            time.sleep(1.0)
            csv = driver.find_elements(By.XPATH, '//md-select-menu/md-content/md-option[2]/div[1]/span')
            action(driver).move_to_element(csv[-1]).click(csv[-1]).perform()
            time.sleep(1.0)
            downloadbutton = driver.find_element(By.XPATH, '//prm-export-excel/div/md-content/form/div[2]/div/button/span')
            action(driver).move_to_element(downloadbutton).double_click(downloadbutton).perform()
            driver.get(url)
            time.sleep(5.0)
            nextbutton = driver.find_elements(By.XPATH, '//prm-page-nav-menu/div/div/div[1]/div[3]/a/prm-icon/md-icon')
            #resultscount = driver.find_elements(By.XPATH, '//md-input-container/md-select/md-select-value/span')
            # 34 shows the results count.
            #resultscount[34].text
            if nextbutton != []:
                #nextbutton = driver.find_elements(By.CLASS_NAME, 'prm-icon')
                print(nextbutton)
                print(driver.current_url)
                # Double click element in case it doesn't register the first time, because the library website is trash
                oldurl = driver.current_url
                action(driver).move_to_element(nextbutton[0]).click(nextbutton[0]).perform()
                time.sleep(5.0)
                if driver.current_url == oldurl:
                    action(driver).move_to_element(nextbutton[0]).click(nextbutton[0]).perform()
                print(driver.current_url)
                url = driver.current_url
            time.sleep(5.0)
#requestables()

def merge():
    titles = []
    abstracts = []
    keywords = []
    authors = []
    journal_origin = []
    filepath = 'C:/Users/dylan/OneDrive/Desktop/AIB'
    dir_list = os.listdir(filepath)
    print(dir_list)
    print(len(dir_list))
    for i in range(len(dir_list)):
        excelcsv = pd.read_csv('C:/Users/dylan/OneDrive/Desktop/AIB/' + str(dir_list[i]))
        for j in range(len(excelcsv)):
            titles.append(excelcsv.iat[j,0])
            authors.append(excelcsv.iat[j,1])
            keywords.append(excelcsv.iat[j,2])
            journal_origin.append(excelcsv.iat[j,4])
            abstracts.append(excelcsv.iat[j,5])
    df = {"Title" : titles, "Authors" : authors , "Keywords" : keywords, "Journal" : journal_origin, "Abstract" : abstracts}
    csvdf = pd.DataFrame(data=df)
    print(csvdf)
    print(len(dir_list))
    csvdf.to_csv('output.csv',index=False)

# Solving for those journals that DO have online access.
merge()

def query_journals():
    titles = []
    abstracts = []
    keywords = []
    authors = []
    journal_origin = []
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
        base_window = driver.window_handles[0]
        #try:
        for j in range(0,28):
            global url
            driver.get(url)
            time.sleep(5.0)
            #trial = driver.find_elements(By.TAG_NAME, 'prm-search-result-list')
            articles = driver.find_elements(By.XPATH, '//prm-brief-result-container')
            article_information = driver.find_elements(By.XPATH, '//span/prm-highlight/span')
            online_access = driver.find_elements(By.XPATH, '//prm-search-result-availability-line/div/div/button')
            #requestable = driver.find_elements(By.XPATH, '//prm-search-result-availability-line/div/div/button/span[2]/span')
            #requestable = driver.find_elements(By.CLASS_NAME, 'availability-status')
            #print(online_access)
            #print(requestable)
            #text(requestable)
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
            for i in range(int(len(article_information)/3)):
                titles.append(article_information[i*3].text)
                authors.append(article_information[i*3 + 1].text)
                journal_origin.append(article_information[i*3 + 2].text)
            driver.get(url)
            time.sleep(5.0)
            nextbutton = driver.find_elements(By.XPATH, '//prm-page-nav-menu/div/div/div[1]/div[3]/a/prm-icon/md-icon')
            print(nextbutton)
            oldurl = driver.current_url
            action(driver).move_to_element(nextbutton[0]).click(nextbutton[0]).perform()
            time.sleep(1.0)
            if driver.current_url == oldurl:
                action(driver).move_to_element(nextbutton[0]).click(nextbutton[0]).perform()
            print(driver.current_url)
            url = driver.current_url
        #print(titles)
        #print(authors)
        #action(driver).move_to_element(element).double_click(highlighted_text[258]).perform()
        csvlist = {'Article Titles' : titles , 'Authors' : authors , 'Keywords' : keywords , 'Abstracts' : abstracts , 'Journal Origin' : journal_origin}
        print(titles)
        print(authors)
        print(keywords)
        print(abstracts)
        print(journal_origin)
        print(csvlist)
        return csvlist
        #except:
        #    csvlist = {'Article Titles' : titles , 'Authors' : authors , 'Keywords' : keywords , 'Abstracts' : abstracts , 'Journal Origin' : journal_origin}
        #    print(csvlist)
        #   csvdf = pd.DataFrame(data=csvlist)
        #    csvdf.to_csv('output.csv')
        #    return csvlist

#query_journals()

#csvdf = pd.DataFrame(data=query_journals())
#print(csvdf)
#csvdf.to_csv('output.csv')

#SelectButton1XPath = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[1]/prm-search-result-list/div/div[1]/div[2]/button[2]/prm-icon/md-icon'
#SelectButton2XPath = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[1]/prm-search-result-list/div/prm-search-result-tool-bar/div/md-toolbar/div[1]/md-checkbox/div[1]'
#SelectOptions = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[1]/prm-search-result-list/div/prm-search-result-tool-bar/div/md-toolbar/div[4]/div[3]/button/prm-icon/md-icon'
#ExportToExcel = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[1]/prm-search-result-list/div/prm-search-result-tool-bar/div/div/div/md-content/prm-action-list/md-nav-bar/div/nav/ul/div/li[5]/button/span/div/span'    
#FileType = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[1]/prm-search-result-list/div/prm-search-result-tool-bar/div/div/div/md-content/prm-action-list/prm-action-container/prm-export-excel/div/md-content/form/div[1]/div[2]/md-input-container/md-select'
#XLSX = '/html/body/div[5]/md-select-menu/md-content/md-option[1]/div[1]/span'
#csv = '/html/body/div[5]/md-select-menu/md-content/md-option[2]/div[1]/span'
#csv2 = '/html/body/div[5]/md-select-menu/md-content/md-option[2]'
#downloadbutton = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[1]/prm-search-result-list/div/prm-search-result-tool-bar/div/div/div/md-content/prm-action-list/prm-action-container/prm-export-excel/div/md-content/form/div[2]/div/button/span'
#results = '/html/body/primo-explore/div[1]/prm-explore-main/ui-view/prm-search/div/md-content/div[1]/prm-search-result-list/div/div[1]/div[3]/prm-search-result-page-range/div/md-input-container/md-select/md-select-value'

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
#results = '/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[1]/prm-search-result-list/div/div[1]/div[3]/prm-search-result-page-range/div/md-input-container/md-select/md-select-value'

def next_page():
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
        global url
        driver.get(url)
        nextbutton = driver.find_elements(By.XPATH, '//prm-page-nav-menu/div/div/div[1]/div[3]/a/prm-icon/md-icon')
        resultscount = driver.find_elements(By.XPATH, '//md-input-container/md-select/md-select-value/span')
        # 34 shows the results count.
        #resultscount[34].text
        if nextbutton:
            #nextbutton = driver.find_elements(By.CLASS_NAME, 'prm-icon')
            print(nextbutton)
            print(driver.current_url)
            # Double click element in case it doesn't register the first time, because the library website is trash
            oldurl = driver.current_url
            action(driver).move_to_element(nextbutton[0]).click(nextbutton[0]).perform()
            if driver.current_url == oldurl:
                action(driver).move_to_element(nextbutton[0]).click(nextbutton[0]).perform()
            print(driver.current_url)
            url = driver.current_url
        else:
            pass    
#next_page()
#next_page()