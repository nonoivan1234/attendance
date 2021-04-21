from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
import time
from tkinter import *
from db import Database

root = Tk()
db = Database('absent.db')
                
url = "https://ldap.tp.edu.tw/oauth/authorize?client_id=13&redirect_uri=https%3A%2F%2Fsschool.tp.edu.tw%2Fedusso%2Fauth&response_type=code&state=ds%3D323301&scope=user%20profile%20idno%20school%20group_info"


def click_collapse(target):
    ActionChains(chrome).move_to_element(target).perform()
    ActionChains(chrome).click(target).perform()
    
def populate_list():
    parts_list.delete(0,END)
    for row in db.fetch():
        parts_list.insert(END, row)

options = Options()
options.add_argument("--disable-notifications")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)
chrome.get(url)

username = chrome.find_element_by_id('username')
password = chrome.find_element_by_id('password')
submit_btn = chrome.find_element_by_id('btnLogin')
username.send_keys('sssh10930148')
password.send_keys('A131892440')
submit_btn.click()
time.sleep(1)

close_btn = chrome.find_element_by_xpath('//*[@id="carouselModalCenter"]/div/div/div[1]/button')
close_btn.click()

btn = chrome.find_element_by_xpath('//*[@id="LeftMenu"]/div/ul/li[2]/a')
click_collapse(btn)

absent_btn = chrome.find_element_by_xpath('//*[@id="collapse200"]/div/li[3]/a')
click_collapse(absent_btn)

time.sleep(2)

soup = BeautifulSoup(chrome.page_source, 'html.parser')

list_header = []
header = soup.find("tr", {'class' : 'ui-jqgrid-labels'}).find_all("th")

for items in header:
    try:
        list_header.append(items.get_text())
    except:
        continue

db.insert(list_header[6], list_header[8], list_header[9], list_header[10], list_header[11], list_header[12], list_header[13], list_header[14], list_header[15], list_header[16], list_header[17])

HTML_data = soup.find_all("table", {'role' : 'presentation'})[1].find_all("tr", {'role' : 'row'})
  
for element in HTML_data:
    sub_data = []
    if element:
        for sub_element in element:
            try:
                sub_data.append(sub_element.get_text())
            except:
                continue
        if not sub_data[6]:
            db.insert(sub_data[6], sub_data[8], sub_data[9], sub_data[10], sub_data[11], sub_data[12], sub_data[13], sub_data[14], sub_data[15], sub_data[16], sub_data[17])
    
# Price List (List Box)
parts_list = Listbox(root, height=50, width=50, border=0)
parts_list.grid(pady=20, padx=20)

populate_list()

root.geometry('350x700')

root.mainloop()