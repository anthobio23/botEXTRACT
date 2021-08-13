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
#driver_options.add_argument('--headless')
#driver_options.add_argument('--no-sandbox')
driver = webdriver.Firefox(executable_path = './geckodriver', 
                           options = driver_options)
driver.get(PATH)
time.sleep(rd.randint(5.0, 8.0))
#assert len(driver.window_handles) == 1

class DOM:

    def lector_file():
    
        with open("COD.txt", "r") as file:
            l_COD = [line.rstrip() for line in file]
        return l_COD

    def extract_elemt():

        box_items = driver.find_elements_by_xpath('//div[@class="section__prateleira-product"]')
        for iter in box_items:
            items = iter.find_element_by_class_name('product-image')
            items.click()
            pass

        box_prod_it = driver.find_elements_by_xpath('//div[@class="product-content__sheet-right"]')
        for i in box_prod_it:

            title = i.find_elements_by_xpath('//div[@class="product-content__sheet-right--name"]')

            print(title[0].text) # funciona, recoge el texto plano del DOM dentro de un div

#            desc = i.find_element_by_xpath('//div[@class="product-content__sheet-right--description"]/div').text()
#            print(desc)
          
        pass
    pass

def search():

    buscador = driver.find_element_by_xpath('//input[@class="fulltext-search-box ui-autocomplete-input"]')
    cod = DOM.lector_file()
    buscador.send_keys(str(cod[0]) + Keys.ENTER)
    time.sleep(rd.randint(2.0, 8.0))
    DOM.extract_elemt()
    pass

search()
