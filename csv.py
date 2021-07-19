'''
This file's main purpose is to download the absent data as a csv file. 
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
import time
import os, sys

url = "https://sschool.tp.edu.tw/edusso/link?school=323301"


def click_collapse(target):
    ActionChains(chrome).move_to_element(target).perform()
    ActionChains(chrome).click(target).perform()

options = Options()
options.add_argument("--disable-notifications")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

if getattr(sys, 'frozen', False): 
    # executed as a bundled exe, the driver is in the extracted folder
    chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
    chrome = webdriver.Chrome(chromedriver_path, chrome_options=options)
else:
    # executed as a simple script, the driver should be in `PATH`
    chrome = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)

chrome.get(url)

username = chrome.find_element_by_id('username')
password = chrome.find_element_by_id('password')
submit_btn = chrome.find_element_by_id('btnLogin')
username.send_keys('**USERNAME**')
password.send_keys('**PASSWORD**')
submit_btn.click()
time.sleep(1)

close_btn = chrome.find_element_by_xpath('//*[@id="carouselModalCenter"]/div/div/div[1]/button')
close_btn.click()

btn = chrome.find_element_by_xpath('//*[@id="LeftMenu"]/div/ul/li[2]/a')
click_collapse(btn)

absent_btn = chrome.find_element_by_xpath('//*[@id="collapse200"]/div/li[3]/a')
click_collapse(absent_btn)

time.sleep(2)

chrome.minimize_window()

soup = BeautifulSoup(chrome.page_source, 'html.parser')

absent_list = []
list_header = []
header = soup.find("tr", {'class' : 'ui-jqgrid-labels'}).find_all("th")

for items in header:
    try:
        list_header.append(items.get_text())
    except:
        continue

HTML_data = soup.find_all("table", {'role' : 'presentation'})[1].find_all("tr", {'role' : 'row'})

for element in HTML_data:
    sub_data = []
    for sub_element in element:
        try:
            sub_data.append(sub_element.get_text())
        except:
            continue
    absent_list.append(sub_data)

total_rows = len(absent_list)

dataFrame = pd.DataFrame(data = absent_list, columns = list_header)

dataFrame.to_csv('absent.csv')
