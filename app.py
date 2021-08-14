import time
import random as rd
import pandas as pd
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

class DOM():

    def __init__(self):
        pass

    def lector_file():
    
        with open("COD.txt", "r") as file:
            l_COD = [line.rstrip() for line in file]
        return l_COD

    def price_calc(self, value):

        """
        Calculo del precio real de los productos de un 30% 
        de descuento multiplicado por un factor del 1.9

        :parameters

        input: cadena de texto correspondiente a la etiqueta html
        de la pagina el cual contiene el precio en pesos chilenos 
        de los productos. 

        output: valor entero real del coste del producto
        """


        price_item = value.split("$ ")
        price_value = int(float(price_item[1]) * 1000 / 1)
        price_30off = price_value - price_value * .30
        price_tot = int(price_30off * 1.9)

        return price_tot

    def extract_elemt(self):

        box_items = driver.find_elements_by_xpath('//div[@class="section__prateleira-product"]')
        for iter in box_items:
            items = iter.find_element_by_class_name('product-image')
            items.click()
            pass

        # get image
        img = driver.find_element_by_class_name("image-0").get_attribute("src"))

        # get box items product
        box_prod_it = driver.find_elements_by_xpath('//div[@class="product-content__sheet-right"]')
        for i in box_prod_it:

            title = i.find_elements_by_xpath('//div[@class="product-content__sheet-right--name"]')
            title_1 = title[0].text # Recoger el titulo en el DOM.
            
            desc = i.find_elements_by_xpath('//div[@class="product-content__sheet-right--description"]')
            desc_1 = desc[0].text # Recoge la descripcion de los productos en el DOM.

            sku = i.find_elements_by_xpath('//div[@class="product-content__sheet-right--sku-reference"]')
            sku_1 = sku[0].text

            price = i.find_elements_by_xpath('//div[@class="product-content__sheet-right--price"]')
            price_1 = self.price_calc(price[0].text)

            size = i.find_elements_by_xpath('//div[@class="sku-selector-container sku-selector-container-0"]')
            size_1 = size[0].text

            

            box_color = i.find_elements_by_xpath('//div[@class="prateleira-similares__content"]')
#            for j in box_color:

#                img_items = j.find_elements_by_xpath("/")

#                print(img_items[0].get_attribute("src"))
  
        pass
    pass

def search():

    buscador = driver.find_element_by_xpath('//input[@class="fulltext-search-box ui-autocomplete-input"]')
    cod = DOM.lector_file()
    buscador.send_keys(str(cod[0]) + Keys.ENTER)
    time.sleep(rd.randint(2.0, 8.0))
    _in = DOM()
    _in.extract_elemt()
    pass

search()
