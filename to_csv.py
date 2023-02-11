'''
This file's main purpose is to download the absent data as a csv file. 
'''
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
import time
import os, sys

url = "https://sschool.tp.edu.tw/edusso/link?school=323301"


def click_collapse(target):
    ActionChains(edge).move_to_element(target).perform()
    ActionChains(edge).click(target).perform()


if getattr(sys, 'frozen', False): 
    # executed as a bundled exe, the driver is in the extracted folder
    edgedriver_path = os.path.join(sys._MEIPASS, "msedgedriver.exe")
    edge = webdriver.Edge(edgedriver_path)
else:
    # executed as a simple script, the driver should be in `PATH`
    edge = webdriver.Edge(executable_path='./msedgedriver')

edge.get(url)

username = edge.find_element_by_xpath('//*[@id="standard-basic"]')
password = edge.find_element_by_xpath('//*[@id="standard-password-input"]')
submit_btn = edge.find_element_by_class_name('jss524')
username.send_keys('username')
password.send_keys('password')
submit_btn.click()
time.sleep(2)

close_btn = edge.find_element_by_xpath('//*[@id="carouselModalCenter"]/div/div/div[1]/button')
click_collapse(close_btn)

btn = edge.find_element_by_xpath('//*[@id="LeftMenu"]/div/ul/li[2]/a')
click_collapse(btn)

absent_btn = edge.find_element_by_xpath('//*[@id="collapse200"]/div/li[3]/a')
click_collapse(absent_btn)

time.sleep(2)

edge.minimize_window()

soup = BeautifulSoup(edge.page_source, 'html.parser')

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