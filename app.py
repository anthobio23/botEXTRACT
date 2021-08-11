import time
import random as rd
import pandas as pd
from selenium.webdriver.firefox import options
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


PATH = "https://www.intime.cl/sostenes?PS=16&O=OrderByReleaseDateDESC"
driver_options = Options()
driver_options.add_argument('--headless')
driver_options.add_argument('--no-sandbox')
driver = webdriver.Firefox(executable_path = './geckodriver', 
                           options = driver_options)
driver.get(PATH)
assert len(driver.window_handles) == 1

def lector_file(l_COD):
    
    l_COD = []
    with open("COD.txt", "r") as file:
        for line in file:
            l_COD.append(line)
            pass
        pass
    return l_COD

def slow_typing(element, text):
    for character in text:
        element.send_keys(character)
        time.sleep(rd.randint(2.0, 8.0))
        pass
    pass

def search():
    buscador = driver.find_element_by_class_name("fulltext-search-box ui-autocomplete-input")
    slow_typing(buscador, "76895")
    pass





