Attendence
===
# Introduction
- ## Background
    The application is based on ```Python 3.9.4``` . Main purpose is to scrape the absent data down from [臺北市高中校務行政系統](https://sschool.tp.edu.tw/Login.action).
- ## Motivation
    In our school, who was absent before nead to check out the attendence in three days after you took a day off. However, I am usually forget to do that on time, although my mom always asks me to do that. So I decided to write a programe to check my attendence automatically, or she will blame on me every times I took a day off.
- ## Method
    First, we are asked to login the site. Second, we have to go to the asking page to find my absent data then scrape it down. Third, store the data which is just scraped. Last, create a GUI frame to show the database with a ScrollBar beside, count the amount of absent classses in each sections a day, and count the different type of absent.
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
- ## Set up Selenium and login