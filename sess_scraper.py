# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 01:30:13 2022

@author: Amin
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs
import csv
import pandas as pd
import logging
import os
import time
import codecs
import random
import string
import numpy as np
#HOME = "C:/Users/Amin/Desktop/tmp"
HOME = os.path.join(os.path.dirname(__file__))

logging.basicConfig(level=logging.INFO,filename=os.path.join(HOME,'sesslog.txt'),format=' %(asctime)s - %(name)s - %(message)s')
chars = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
url = "https://sess.sku.ac.ir/X3/SessWay/Script/Login.aspx"
firefox_driver_path = os.path.join(HOME,"geckodriver.exe")
USERNAME = "s981901102"
PASSWORD = "@minahmadpour80"
s = Service(firefox_driver_path)
options = Options()
options.headless=True
driver = webdriver.Firefox(service=s,options=options)
driver.get(url)
logging.info("Headless Firefox Initialized")
assert "ورود به سیستم" in driver.title

def login(driver,USERNAME,PASSWORD):
    username_field = driver.find_element(By.NAME,'edId')
    password_field = driver.find_element(By.ID,"edPass")
    login_btn = driver.find_element(By.ID,"edEnter")
    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    login_btn.click()
    assert "امين احمدپورمعرفي"==driver.find_element(By.ID,"edflname").text
    
def go_to_class_schedule(driver):
    
    driver.implicitly_wait(3)
    ParentForm = driver.find_element(By.ID,"ParentForm").find_elements(By.CSS_SELECTOR,"*")[55]
    ParentForm.click()
    driver.implicitly_wait(2)
    Education = driver.find_element(By.CLASS_NAME,"nav__list").find_elements(By.TAG_NAME,"li")[18]
    Education.click()
    courses_schedule = driver.find_elements(By.CLASS_NAME,"link")[26]
    assert "PerformStd('Pcl')" in courses_schedule.get_attribute("onclick")
    driver.implicitly_wait(5)
    driver.execute_script("window.scrollTo(0, 678)") 
    ActionChains(driver).move_to_element(courses_schedule).click().perform()

def get_section_courses(driver,dept_value):
    year_select = driver.find_element(By.NAME,"edSemester")
    department_select = Select(driver.find_element(By.NAME,"edDepartment"))
    department_select.select_by_value(str(dept_value))
    assert "مشاهده" in driver.find_element(By.ID,"edDisplay").get_attribute("value")
    driver.find_element(By.ID,"edDisplay").click()
    courses_table = driver.find_elements(By.CLASS_NAME,"ptext")[3].find_elements(By.TAG_NAME,"tr")
    driver.implicitly_wait(5)
    logging.info("section {} has {} classes.".format(dept_value,len(courses_table)))
    return len(courses_table)
        
def save_to_file(driver):
    
    file_path = os.path.join(HOME,'files',"{}.html".format("".join(random.sample(chars,8))))
    f = codecs.open(file_path, "w", "utf−8")
    f.write(driver.page_source)
    
def get_course(driver,course):
    
    driver.implicitly_wait(2)
    get_section_courses(driver,str(deptid))
    elem = driver.find_elements(By.CLASS_NAME,"ptext")[3].find_elements(By.TAG_NAME,"tr")[course]
    ActionChains(driver).move_to_element(elem).click().perform()
    #assert "مشخصات کلاس" in driver.find_element(By.CLASS_NAME,"title_of_page").text
    logging.info("getting info about %s "%(driver.find_element(By.ID,"edName").text))
    driver.implicitly_wait(2)
    time.sleep(3)
    driver.refresh()
    save_to_file(driver)
    driver.find_element(By.ID,"edRet").click()
    driver.implicitly_wait(2)
    assert "ليست کلاس هاي تعريف شده" in driver.find_element(By.CLASS_NAME,"title_of_page").text
    driver.refresh()
    
if __name__=="__main__":
    #departments = pd.read_excel("C:/Users/Amin/Desktop/tmp/sku_schedule.xlsx",encoding='utf-8-sig')
    dept_values = np.load(os.path.join(HOME,'ex.npy')).tolist()
    login(driver,USERNAME,PASSWORD)
    go_to_class_schedule(driver)
    for deptid in dept_values:
        n=get_section_courses(driver,deptid)
        for course in range(3,n):
            get_course(driver,course)
        dept_values.pop(0)
        np.save('ex',dept_values)
