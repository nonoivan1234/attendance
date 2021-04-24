README
===
## Introduction
- ### Background
    The application is based on ```Python 3.9.4``` . Main purpose is to scrape the absent data down from [臺北市高中校務行政系統](https://sschool.tp.edu.tw/Login.action).
- ### Method
    First, we are asked to login the site. Second, we have to go to the asking page to find my absent data then scrape it down. Third, store the data which is just scraped. Last, create a GUI frame to show the database with a ScrollBar beside, count the amount of absent classses in each sections a day, and count the different type of absent.
- ### Motivation
    In our school, who was absent before nead to check out the attendent in three days after you took a day off. However, I am usually forget to do that on time, although my mom always asks me to do that. So I decided to write a programe to check my attendent automatically, or she will blame on me every times I took a day off.
## Body
- ### Tools (imported in Python)
    - #### Tkinter
        To build a GUI application with Python quickly.
    - #### Selenium
        To stimulate mouse movements to click the non-button element in website.
        Notice: Selenium is based on its driver, so we have to download the driver on the [website](https://pypi.org/project/selenium/).
    - #### BeautifulSoup
        To scrape the website's html source and find the element of the website by its id, class, xpath, etc.
    - #### Time
        To use the function below to wait for the website finishing loading.
        ```python=
        time.sleep(sec) # Where sec is seconds to wait for the progress loding.
        ``` 
    - #### SQLite3
        To create a ```.db``` file to store the data. We will create a class named ```Database``` and define some functions to complete the purpose.
- ### Initial the code
    - #### Include the module
        In this case of application, we will have to create 2 Python Files named db.py and main.py. One is used to write a class named ```Database```, and define functions to fetch, insert, and count the item. Another one is used to write the main code and its GUI settings then run as main file.
        
        In db.py, we nead to import the ```sqlite3``` module. So, we write the code below.
        ```python=
        import sqlite3
        ```
        
        In main.py, we have to import Tkinter, Selenium, BeautifulSoup,  Time, and the class we just wrote in db.py. So, we write the code below.
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
