from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains as action
from selenium.webdriver.common.keys import Keys
import time 
import math
import os

options = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "C:/Users/dylan/Desktop/temp"}
options.add_experimental_option("prefs", prefs)
#options.add_argument("--headless=new")

url = 'https://ssb.sju.edu/pls/PRODSSB/hzgkcdir.P_DirSearchNest'

def wait(seconds=5):
    time.sleep(seconds)

#User login: //*[@id="UserID"]
#Password: //*[@id="PIN"]
#Directory button = /html/body/form/table/tbody/tr[1]/td[1]
#Submit = /html/body/div[3]/form/p/input
#Email = //*[@id="i0116"]
#Next = //*[@id="idSIButton9"]
#Pwd= //*[@id="i0118"]
#Submit = //*[@id="idSIButton9"]
#Verify = //*[@id="idDiv_SAOTCS_Proofs"]/div/div/div/div[2]/div
#2FACode = //*[@id="idTxtBx_SAOTCC_OTC"]
#Verifybutton = //*[@id="idSubmit_SAOTCC_Continue"]
#Univdirectbutton = //*[@id="block-nestmain"]/ul/li[3]/a
#Opens a new tab
# driver.switch_to.window(driver.window_handles[1])

def __init__():
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
        def text(object):
            for i in range(len(object)):
                print(object[i].text)
        def click(object):
            action(driver).move_to_element(object).click(object).perform()
        driver.get(url)
        time.sleep(5.0)
        ## SJU Credentials are required to access the student directory. This portion of the code handles the grueling sign-in process.
        print("SJU Credentials Required.")
        print("Username:")
        username = 'df752850'#input()
        # Username must not contain @sju.edu
        username = username.rstrip('@sju.edu')
        print("Password:")
        password = 'DiFpvdb1!%_----'#input()
        usernamebox = driver.find_element(By.XPATH, '//*[@id="UserID"]')
        passwordbox = driver.find_element(By.XPATH, '//*[@id="PIN"]')
        usernamebox.send_keys(username)
        passwordbox.send_keys(password)
        submit = driver.find_element(By.XPATH, '//html/body/div[3]/form/p/input') 
        click(submit)
        wait()
        #time.sleep(120)
        #email = driver.find_element(By.XPATH, '//*[id="i0116"]') 
        #emailbox = driver.find_element(By.PARTIAL_LINK_TEXT, 'username@sju.edu')
        def send(content):
            input1 = driver.find_element(By.TAG_NAME,"input")
            input1.send_keys(content)
            input1.send_keys(Keys.ENTER)
        #email.send_keys(username + '@sju.edu')
        send(username + '@sju.edu')
        wait()
        #try:
        #input1 = driver.find_element(By.TAG_NAME,"input")
        #input1.send_keys(password)
        #input1.send_keys(Keys.ENTER)
        #except:
        input1 = driver.find_element(By.XPATH, '//*[@id="i0118"]')
        input1.send_keys(password)
        input1.send_keys(Keys.ENTER)
        #//*[@id="i0118"]
        send(password)
        wait()
        #time.sleep(120)
        #//*[@id="tilesHolder"]/div[1]/div/div[1]
        input1 = driver.find_element(By.XPATH, '//*[@id="tilesHolder"]/div[1]/div/div[1]')
        #input1.send_keys(Keys.ENTER)
        action(driver).move_to_element(input1).click(input1).perform()
        #time.sleep(120)
        #passwordbox = driver.find_element(By.XPATH, '//*[@id="i0118"]')
        #passwordbox.send_keys(password)
        #next = driver.find_element(By.XPATH, '//*[@id="idSIButton9"]')
        #click(next)
        #wait()
        #input1 = driver.find_element(By.TAG_NAME,"input")
        #input1.send_keys(Keys.ENTER)
        wait()
        verifybox = driver.find_element(By.XPATH, '//*[@id="idDiv_SAOTCS_Proofs"]/div/div/div/div[2]/div')
        click(verifybox)
        wait()
        twofacode = driver.find_element(By.XPATH, '//*[@id="idTxtBx_SAOTCC_OTC"]')
        print("A verification code is required to access the directory. Enter the 6-digit code here:")
        verificationcode = input()
        twofacode.send_keys(verificationcode)
        submitverification = driver.find_element(By.XPATH, '//*[@id="idSubmit_SAOTCC_Continue"]')
        click(submitverification)
        wait()
        #time.sleep(300)
        #//*[@id="block-nestmain"]/ul/li[3]/a
        directorybutton = driver.find_element(By.XPATH, '//*[@id="block-nestmain"]/ul/li[3]/a')
        click(directorybutton)
        wait()
        try:
            driver.switch_to.window(driver.window_handles[1])
        except:
            pass
        time.sleep(10)
        #wait()
        #time.sleep(300)
        #/html/body/form/table/tbody/tr[1]/td[1]/select
        directoryoption = driver.find_element(By.XPATH, '//html/body/form/table/tbody/tr[1]/td[1]/select')
        directoryoption1 = driver.find_elements(By.TAG_NAME, "select")
        directoryoption2 = driver.find_elements(By.CLASS_NAME, "dedefault")
        directoryoption3 = driver.find_elements(By.CSS_SELECTOR, "td.dedefault")
        #print(directoryoption)
        #print(directoryoption1)
        #print(directoryoption2)
        click(directoryoption)
        wait()
        time.sleep(20)
        #try:
        #    student = driver.find_element(By.XPATH, '//html/body/form/table/tbody/tr[1]/td[1]/select/option[2]')
        #    print(student)
        #    wait()
        #    click(student)
        directoryoption.send_keys(Keys.ARROW_DOWN)
        directoryoption.send_keys(Keys.ENTER)
        wait()
        maxhitsbutton = driver.find_element(By.XPATH,'//html/body/form/table/tbody/tr[3]/td[1]/select')
        click(maxhitsbutton)
        maxhitsbutton.send_keys(Keys.ARROW_DOWN)
        maxhitsbutton.send_keys(Keys.ARROW_DOWN)
        maxhitsbutton.send_keys(Keys.ENTER)
        search = driver.find_element(By.XPATH, '//html/body/form/pre/input')
        click(search)
        wait()
        #First object
        #/html/body/table[1]/tbody/tr[2]
        #Last object
        #/html/body/table[1]/tbody/tr[101]
        name = []
        ##Name
        #/html/body/table[1]/tbody/tr[2]/td[1]
        level = []
        ##Level
        #/html/body/table[1]/tbody/tr[2]/td[2]
        major = []
        ##Major
        #/html/body/table[1]/tbody/tr[2]/td[3]
        email = []
        ##Email
        #/html/body/table[1]/tbody/tr[2]/td[4]
        for i in range(2,101):
            try:
                namebox = driver.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[' + str(i) + ']/td[1]')
                name.append(namebox.text)
                levelbox = driver.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[' + str(i) + ']/td[2]')
                level.append(levelbox.text)
                majorbox = driver.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[' + str(i) + ']/td[3]')
                major.append(majorbox.text)
                emailbox = driver.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[' + str(i) + ']/td[4]')
                email.append(emailbox.text)
            except:
                print("Error grabbing pg 1 (line 180).")
        #print(name)
        #print(level)
        #print(major)
        #print(email)
        nextbutton = driver.find_element(By.XPATH, '//html/body/table[2]/tbody/tr/td/a/b')
        click(nextbutton)
        wait()
        def query_all():
            try:
                for i in range(2,101):
                    namebox = driver.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[' + str(i) + ']/td[1]')
                    name.append(namebox.text)
                    levelbox = driver.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[' + str(i) + ']/td[2]')
                    level.append(levelbox.text)
                    majorbox = driver.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[' + str(i) + ']/td[3]')
                    major.append(majorbox.text)
                    emailbox = driver.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[' + str(i) + ']/td[4]')
                    email.append(emailbox.text)
                nextbutton = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td[3]/a/b')
                click(nextbutton)
                wait(10)        
            except:
                print("List complete.")
                directory = {"Name": name, "Level": level, "Major": major, "Email": email}
                df = pd.DataFrame(data=directory)
                df.to_csv('directory.csv', index=False)
                quit()
            query_all()
        query_all()
    return name, level, major, email
__init__()