import tkinter
from tkinter import *
from tkinter.ttk import Treeview
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
from db import Database


root = Tk()
db = Database('absent.db')

url = "https://sschool.tp.edu.tw/edusso/link?school=323301"

# click the collapse
def click_collapse(target):
    ActionChains(chrome).move_to_element(target).perform()
    ActionChains(chrome).click(target).perform()

# populate the sqlite database to the router_tree_view    
def populate_list():
    for i in router_tree_view.get_children():
        router_tree_view.delete(i)
    for row in db.fetch():
        router_tree_view.insert('', 'end', values=row)

# option of the driver
options = Options()
options.add_argument("--disable-notifications")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)
chrome.get(url)

# input the username and password then click the submit the button
username = chrome.find_element_by_id('username')
password = chrome.find_element_by_id('password')
submit_btn = chrome.find_element_by_id('btnLogin')
username.send_keys('USERNAME')
password.send_keys('PASSWORD')
submit_btn.click()
time.sleep(1)

# close the notifying page after submit the passwd
close_btn = chrome.find_element_by_xpath('//*[@id="carouselModalCenter"]/div/div/div[1]/button')
close_btn.click()


# click the left side collapse to go into the purpose page
btn = chrome.find_element_by_xpath('//*[@id="LeftMenu"]/div/ul/li[2]/a')
click_collapse(btn)

absent_btn = chrome.find_element_by_xpath('//*[@id="collapse200"]/div/li[3]/a')
click_collapse(absent_btn)

# wait for the page
time.sleep(2)

soup = BeautifulSoup(chrome.page_source, 'html.parser')

# find header in html
list_header = []
header = soup.find("tr", {'class' : 'ui-jqgrid-labels'}).find_all("th")

for items in header:
    try:
        list_header.append(items.get_text())
    except:
        continue

header = [list_header[6], list_header[7], list_header[8], list_header[9], list_header[10], list_header[11], list_header[12], list_header[13], list_header[14], list_header[15], list_header[16]]

# find the neaded data
HTML_data = soup.find_all("table", {'role' : 'presentation'})[1].find_all("tr", {'role' : 'row'})

for element in HTML_data:
    sub_data = []
    for sub_element in element:
        try:
            sub_data.append(sub_element.get_text())
        except:
            continue
    if sub_data[6] != '':   # insert the non-null header to database
        db.insert(sub_data[6], sub_data[7], sub_data[8], sub_data[9], sub_data[10], sub_data[11], sub_data[12], sub_data[13], sub_data[14], sub_data[15], sub_data[16])

chrome.close()

 # setting the database_viewer
frame_router = Frame(root)
frame_router.grid(row=0, column=0, columnspan=5, rowspan=1, pady=10, padx=20)

# send the data from database to the viewer and designing
columns = ['id', 'date_', 'zero', 'morning', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']
router_tree_view = Treeview(frame_router, columns=columns, show='headings')
router_tree_view.column("id", width=40, anchor='center')
router_tree_view.heading("id", text="??????")
router_tree_view.column('date_', width=100, anchor='center')
router_tree_view.heading('date_', text='??????')
for col in range (2,len(columns)):
    router_tree_view.column(columns[col], width=40, anchor='center')
    router_tree_view.heading(columns[col], text=header[col-1])
router_tree_view.pack(side="left", fill="x")
scrollbar = Scrollbar(frame_router, orient='vertical')
scrollbar.configure(command=router_tree_view.yview)
scrollbar.pack(side="right", fill="y")
router_tree_view.config(yscrollcommand=scrollbar.set)

ct = []
for i in columns[2:]:
    ct.append(db.count_item(i))
db.insert('??????', sum(ct[0]), sum(ct[1]), sum(ct[2]), sum(ct[3]), sum(ct[4]), sum(ct[5]), sum(ct[6]), sum(ct[7]), sum(ct[8]), sum(ct[9]))

# count every item's number in database 
count_shi = 0
count_chi = 0
count_kuan = 0
count_sick = 0
count_gon = 0

for i in range (len(ct)):
    for j in range (5):
        if j==0:
            count_chi+=ct[i][j]
        if j==1:
            count_gon+=ct[i][j]
        if j==2:
            count_kuan+=ct[i][j]
        if j==3:
            count_sick+=ct[i][j]
        if j==4:
            count_shi+=ct[i][j]

# setting the label under the database_viewer          
shi = tkinter.Label(root, text="?????????"+str(count_shi)+"???",font = ("???????????????",13))
shi.grid(column=0, row=2, columnspan=1)

chi = tkinter.Label(root, text="?????????"+str(count_chi)+"???",font = ("???????????????",13))
chi.grid(column=1, row=2, columnspan=1)

kuan = tkinter.Label(root, text="?????????"+str(count_kuan)+"???",font = ("???????????????",13))
kuan.grid(column=2, row=2, columnspan=1)

sick = tkinter.Label(root, text="?????????"+str(count_sick)+"???",font = ("???????????????",13))
sick.grid(column=3, row=2, columnspan=1)

gon = tkinter.Label(root, text="?????????"+str(count_gon)+"???",font = ("???????????????",13))
gon.grid(column=4, row=2, columnspan=1)

sentence = tkinter.Label(root, text="?????? %d ???   "%sum(list(map(sum,ct))),font = ("???????????????",15))
sentence.grid(column=0, row=3, columnspan=5, pady=10, padx=20)

populate_list()

root.title('?????????????????????')

# run the main GUI
root.mainloop()
