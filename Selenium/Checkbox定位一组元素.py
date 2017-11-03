#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author  : Soner
@version : 
@Time    : 2017/11/3/0003 16:32
@license : Copyright(C), Your Company 
'''
from selenium import webdriver
from time import sleep
import os

driver = webdriver.Chrome()
file_path = "file://" + os.path.abspath("Checkbox.html")
driver.get(file_path)

inputs = driver.find_elements_by_tag_name("input")

for i in inputs:
    if i.get_attribute("type") == "checkbox":
        i.click()
    sleep(2)

sleep(2)
driver.quit()