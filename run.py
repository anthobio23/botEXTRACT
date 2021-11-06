#!/usr/bin/python3

import os
import time
import requests
import random as rd
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

# modulo personal
from component import process
print("Module component imported ", __name__)

URL = "https://www.intime.cl/sostenes?PS=16&O=OrderByReleaseDateDESC"
driver_options = Options()
#driver_options.add_argument('--headless')
#driver_options.add_argument('--no-sandbox')
driver = webdriver.Firefox(executable_path = './geckodriver', 
                           options = driver_options)
driver.get(URL)
assert len(driver.window_handles) == 1

class DOM(): 

    """
    El objeto DOM trabaja con los metodos lector_file, price_calc y extract_elemt
    para satisfacer la extraccion de datos de las paginas intime
    """

    def __init__(self):

        """
        inicializamos con la construccion de listas para la extraccion de items.
        """

        self.title = []
        self.desc = []
        self.sku = []
        self.price = []
        self.size = []
        self.img = []
        self.code = []
        self.comp = []

        pass

    def price_calc(self, value):

        """
        Calculo del precio real de los productos de un 30% 
        de descuento multiplicado por un factor del 1.9

        :parameters
        :value: parametro de tipo strings

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

    def extract_imgs_box(self, url):

        r = requests.get(url)
        html = r.content
        soup = BeautifulSoup(html, "html.parser")

        fichaProducto = soup.find_all("div", 
                class_="product__img-preview imgPreview slick-initialized slick-slider slick-vertical")
        i = 0
        for element in fichaProducto:
            print(element.find("img", class_="slick-slide slick-active").get("src"))
            i+=1
            pass
        pass
    
    # lista de elemetos
    sku_ls = []
    size_ls = []

    def extract_elemt(self, cod_model):
      
        #recuperamos la cantidad de box por items para excrapear.
        box_items = driver.find_elements_by_xpath('//a[@class="product-image"]')
        print(len(box_items))

        if len(box_items) > 0:

            time.sleep(rd.randint(2.0, 8.0))
            box_items[0].click()

            print("Codigo de modelo a extraer: ", cod_model)
            self.code.append(cod_model)
            time.sleep(rd.randint(2.0, 10.0))
            # get image major
            get_img = driver.find_element_by_xpath("//img[@class='image-0']")
            self.img.append(get_img.get_attribute("src"))
    
            box_prod_it = driver.find_elements_by_xpath('//div[@class="product-content__sheet-right"]')
            
            for i in box_prod_it:
                
                title = i.find_elements_by_xpath('//div[@class="product-content__sheet-right--name"]')
                self.title.append(title[0].text) # Recoger el titulo en el DOM.
 #               print(self.title)
          
                desc = i.find_elements_by_xpath('//div[@class="product-content__sheet-right--description"]')
                self.desc.append(desc[0].text) # Recoge la descripcion de los productos en el DOM.
 #               print(self.desc)

                sku = i.find_elements_by_xpath('//div[@class="product-content__sheet-right--sku-reference"]')
                self.sku.append(sku[0].text) # Recoge el codigo sku de los productos en el DOM.
                self.sku_ls.append(self.sku[0].split("\n")[1])
  #              print(self.sku_ls)

                price = i.find_elements_by_xpath('//div[@class="product-content__sheet-right--price"]')
                self.price.append(self.price_calc(price[0].text)) # Recoge el precio de los preductos en el DOM.
   #             print(self.price)

                size = i.find_elements_by_xpath('//div[@class="sku-selector-container sku-selector-container-0"]')
                self.size.append(size[0].text) # Recoge las tallas (Crear funcion para organizarla)
                size = self.size[0].split("\n")
                self.size_ls.append([size[iter] for iter in range(1, len(size))])
    #            print(self.size_ls)

                divcomp = i.find_elements_by_xpath('//div[@class="product__details-composition i-despegable"]')
                divcomp[0].click() # hace click sobre el div de composicion

                span_comp = i.find_elements_by_xpath(".//span[@class='product__composition-element']")
                if len(span_comp) > 0:
                    self.comp.append(span_comp[0].text) # Recoge la composicion de los productos.
   #               print(self.comp)
                else:
                    None
                    pass
                pass
            pass
        return self.title, self.desc, self.sku_ls, self.price, self.size_ls, self.img, self.code, self.comp

    def forms_search(self, *args):

        """
        el metodo corresponde a las busqueda por codigo en la tiendas intime

        :paramaters

        por orden de posicion, llamaremos al metodo mediante la instancia DOM
        introduciremos el file con los codigos de los articulos a raspar.
        seguidamente del xpath correspondiente al buscador donde se introduciran 
        luego los codigos.

        :input
        0: archivo tipo .txt el mismo sera abierto por la instancia creada 
        sobre el mismo metodo, es decir lector_file().

        1: xpath extraido del codigo html de la pagina web.

        :output
        intoduce el codigo sobre el buscador y va hacia adelante del mismo.
        """
       
        # llamaremos al metodo para leer nuestro codigos.
        # luego iteraremos sobre la lista creada.
        cod_file = process.load_file(args[0])
 #       i = 0
        for i in range(0, len(cod_file)):
    
            # llamada a selenium para que busqua el objeto buscador con el xpath.
            search = driver.find_element_by_xpath(str(args[1]))
            time.sleep(rd.randint(2.0, 8.0))    
            # introducimos el codigo mediante la misma iteracion 
            # daremos un ENTER con selenium
            search.send_keys(cod_file[i] + Keys.ENTER)
            time.sleep(rd.randint(2.0, 8.0))
              
#           i = i + 1
            time.sleep(rd.randint(2.0, 8.0))
            driver.refresh()

            scrap = self.extract_elemt(cod_file[i])
            # enviar cada codigo iterado para extraer cada elemento de la pagina
#            if i >= len(cod_file):
#                break
#            else: 
#                continue
            pass
        return scrap
    pass


# variables de extraccion 
path_code = "COD.txt"
xpath = "//input[@class='fulltext-search-box ui-autocomplete-input']"
_in = DOM()

# clear data
tit, des, sk, pc, sz, im, cod, comp = _in.forms_search(path_code, xpath)

#print(tit)
#print(des)
#print(sk)
#print(pc)
#print(sz)
#print(im)
#print(cod)
#print(comp)

ds = pd.DataFrame({"Composition": comp})
#ds = pd.read_excel("plantilla.xlsx")
#ds["Titulo"] = tit
#ds["Descripcion"] = des 
#ds["SKU"] = sk
#ds["Imagenes"] = im
#ds["Precio"] = pc
#ds["Talla"] = sz
#ds["Modelo"] = cod
#ds["Composicion"] = comp


print(ds.head(10))
ds.to_excel("comp.xlsx", index=True)
