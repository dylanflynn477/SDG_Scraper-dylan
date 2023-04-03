from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Declaring global variables
global url
global options
global journal_list
global query_results

url = 'https://sju.primo.exlibrisgroup.com/discovery/search?query=issn,contains,0022-2380,AND&tab=Everything&search_scope=MyInst_and_CI&vid=01USCIPH_INST:SJU&mode=advanced&offset=0'
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
    driver.get(url)
    print("Page URL:", driver.current_url)
    print("Page Title:", driver.title)
    #elements = driver.find_elements(By.TAG_NAME, 'prm-brief-result')
    elements = driver.find_elements(By.TAG_NAME, 'prm-brief-result-container')
    print(f"Results: {elements}")
