# Demonstration
Demonstrate the final visualized result. Some statistics have been pixelated due to the personal information.
## Tkinter GUI

![image](https://user-images.githubusercontent.com/71141033/218176879-ee7f11e7-aff3-44e2-822e-d41e11879b83.png)

## CSV file

![image](https://user-images.githubusercontent.com/71141033/218178045-072379b3-49f7-4c5a-8f70-2516ab9b8652.png)


# Introduction
- ## Background
    The application is based on ```Python 3.9.4``` . Edge is based on ```vr.110```. Main purpose is to scrape the absent data down from [臺北市高中校務行政系統](https://sschool.tp.edu.tw/Login.action).
<!--- ## Motivation
    In our school, who was absent before nead to check out the attendence in three days after you took a day off. However, I usually forget to do that on time, although my mom always asks me to do it on time. So I decided to write a programe to check my attendence automatically.-->
- ## Method
    First, we are asked to login the site. Second, we have to go to the asking page to find my absent data then scrape it down. Third, store the data as a SQLite file which we just scraped. Last, create a GUI frame to show the database with a ScrollBar beside, count the amount of absent classses in each sections a day, and count the different type of absent.
- ## Warning
    It is possible that program error occur due to the wrong version of you browser.
# Body
- ## Requirements
    - ### Tkinter
        To build a GUI application with Python quickly.
    - ### Selenium
        To stimulate mouse movements to click the non-button element in website.
        Notice: Selenium is based on its driver, so we have to download the driver on the [website](https://pypi.org/project/selenium/).
    - ### BeautifulSoup
        To scrape the website's html source and find the element of the website by its id, class, xpath, etc.
    - ### Time
        To use the function below to wait for the website finishing loading.
        ```python=
        time.sleep(sec) # Where sec is seconds to wait for the progress loding.
        ``` 
    - ### SQLite3
        To create a ```.db``` file to store the data. We will create a class named ```Database``` and define some functions to complete the purpose.
    - ### Install them by pip
        Open your terminal and enter the code below.
        ```=
        pip install -r requirements.txt
        ```
- ## Initial the code
    - ### Include the module
        In this case of application, we will have to create 2 Python Files named ``````db.py`````` and ```main.py```. One is used to write a class named ```Database```, and define functions to fetch, insert, and count the item. Another one is used to write the main code and its GUI settings then run as main file.
        
        In ```db.py```, we nead to import the ```sqlite3``` module. So, we write the code below.
        ```python=
        import sqlite3
        ```
        In ```main.py```, we have to import Tkinter, Selenium, BeautifulSoup,  Time, and the class we just wrote in ```db.py```. So, we write the code below.
        ```python=
        import tkinter
        from tkinter import *
        from tkinter.ttk import Treeview
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.action_chains import ActionChains
        from bs4 import BeautifulSoup
        import time
        from db import Database
        ```
- ## Set up the ```Database```  in ```db.py```

    - ### Set up ```__init__``` settings
        In ```main.py``` we are going to use the function below to create the database. 
        
        ```python=13
        db = Database('absent.db')
        ```
        As you can see, we will input a database name ```db``` to call the function. So, we connect it first. Then we write ```.cursur()``` to excute the SQLite code. Third, we delete the existing table to prevent getting exsisting datas we already have. And, we create a table called ```tb``` which has 12 elements. The first item is auto increasing numbers to count the rows numbers. Last, commit it.
        ```python=3
        class Database:
            def __init__(self, db): 
                # create the table if not exists and delete the curerent database

                self.conn = sqlite3.connect(db)
                self.cur = self.conn.cursor()
                self.cur.execute(
                    "CREATE TABLE IF NOT EXISTS tb (id INTEGER PRIMARY KEY, date_ text, zero text, morning text, one text, two text, three text, four text, five text, six text, seven text, eight text)")
                self.cur.execute('DELETE FROM tb;',)
                self.conn.commit()
        ```
    - ### Define ```fetch()``` function
        What we want to do is fetch all the data from database. Then it should return a list with every rows' data.
        ```python=14
            def fetch(self):        
                # fetch the rows and return back

                self.cur.execute("SELECT * FROM tb")
                rows = self.cur.fetchall()
                return rows
        ```
    - ### Define ```insert()``` function
        Just write a ```insert``` code to do so. Then, commit it again.
        ```python=21
            def insert(self, date_, zero, morning, one, two, three, four, five, six, seven, eight):
                # insert the data to the database

                self.cur.execute("INSERT INTO tb VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (date_, zero, morning, one, two, three, four, five, six, seven, eight))
                self.conn.commit()
        ```
    - ### Define ```count_item()``` function
        In ```main.py``` we will call the function with a single coulumn. And what we nead to do is count the numbers of values which are __遲__, __公__, __曠__, __病__, or __事__. What we have to mention is the ```.fetchone()``` function will return a tupple back. So we will select the first data.
        ```python=28
            def count_item(self, column):
                # count every item, append in the list, and return back the list

                temp = []
                self.cur.execute('SELECT COUNT(%s) FROM tb WHERE %s = "遲";'%(column, column))
                temp.append(self.cur.fetchone()[0])
                self.cur.execute('SELECT COUNT(%s) FROM tb WHERE %s = "公";'%(column, column))
                temp.append(self.cur.fetchone()[0])
                self.cur.execute('SELECT COUNT(%s) FROM tb WHERE %s = "曠";'%(column, column))
                temp.append(self.cur.fetchone()[0])
                self.cur.execute('SELECT COUNT(%s) FROM tb WHERE %s = "病";'%(column, column))
                temp.append(self.cur.fetchone()[0])
                self.cur.execute('SELECT COUNT(%s) FROM tb WHERE %s = "事";'%(column, column))
                temp.append(self.cur.fetchone()[0])
                return temp
        ```
- ## Define functions in ```main.py```
    With included module named ```Database```. Each of the two finctions we have to set up is ```click_collapse()``` and ```populate_list()```.
    - ### Set up ```click_collapse()```
        What the main porpose is to click the collapse item in the html. So we are required to input the target item in web code. By using ```ActionChains()``` to stimulate the mouse what users will do.
        ```python=17
        # click the collapse
        def click_collapse(target):
            ActionChains(chrome).move_to_element(target).perform()
            ActionChains(chrome).click(target).perform()
        ```
    - ### Set up ```populate_list()```
        So we have to fetch all the data in ```db.py```. First, delete all the children in the router_tree_view. Then, fetch all the data in database and insert it.
        ```python=22
        # populate the sqlite database to the router_tree_view    
        def populate_list():
            for i in router_tree_view.get_children():
                router_tree_view.delete(i)
            for row in db.fetch():
                router_tree_view.insert('', 'end', values=row)
        ```
- ## Set up Selenium and login
    - ### Set up the options of Selenium
        By observing the website. We can simply get the login website of each scohhl is different. That is to say, we can just ```get``` the login page directly. 
        So just write down the target url
        ```python=15
        url = "https://ldap.tp.edu.tw/oauth/authorize?client_id=13&redirect_uri=https%3A%2F%2Fsschool.tp.edu.tw%2Fedusso%2Fauth&response_type=code&state=ds%3D323301&scope=user%20profile%20idno%20school%20group_info"
        ```
        Then the option of the Selenium is
        ```python=29
        # option of the driver
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)
        chrome.get(url)
        ```
        To keep our programe running smoothly. We will disable notifications and log. What we have to mention is the driver's path needs to be the related path.
    - ### Submit the login information
         By observing the web page, we can easily know that the textbox of the username's and the password's id is ```username``` and ```password``` . So just send the key to them, then click the submit button.
        ```python=36
        # input the username and password then click the submit the button
        username = chrome.find_element_by_id('username')
        password = chrome.find_element_by_id('password')
        submit_btn = chrome.find_element_by_id('btnLogin')
        username.send_keys('USERNAME')
        password.send_keys('PASSWORD')
        submit_btn.click()
        ```
