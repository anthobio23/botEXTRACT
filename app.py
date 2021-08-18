import os
import time
import requests
import random as rd
import pandas as pd
from bs4 import BeautifulSoup
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

    """
    El objeto DOM trabaja con los metodos lector_file, price_calc y extract_elemt
    para satisfacer la extraccion de datos de las paginas intime
    """

    def __init__(self):

        self.title = []
        self.desc = []
        self.sku = []
        self.price = []
        self.size = []
        self.img = []
        self.code = []

        pass

    def lector_file():

        """
        Carga automatica de los codigos,
        de identificacion escritos en file txt.
        """
    
        with open("COD.txt", "r") as file:
            l_COD = [line.rstrip() for line in file]
        return l_COD

    def load_xlsx(sheets):

        ds = pd.read_excel("scraping_data.xlsx",
                sheet_name=sheets,
                header=None,
                names=["produc", "Cant/char", "CodUniversal", 
                    "color", "color_comercial", "talla", "img",
                    "sku", "cantidad", "Precio", "Moneda", "Condicion",
                    "Desc", "link", "tipPublicacion", "formaenvio",
                    "costoenvio", "retiropersona", "garantia", "tiempogarantia",
                    "unidad_garantia", "Marca", "Modelo", "cant_pack", "genero",
                    "composicion", "material", "tipoBombacha", 
                    "apta_embarazadas"])
        
        return ds

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

    def extract_elemt(self, cod_model):

        box_items = driver.find_elements_by_xpath('//a[@class="product-image"]')
        time.sleep(rd.randint(2.0, 8.0))
  
        #items = box_items.find_element_by_class_name('product-image')
        print(len(box_items))
        if len(box_items) > 0:
            
            box_items[0].click()
            self.code.append(cod_model)

            time.sleep(rd.randint(2.0, 8.0))

            # get image major
            get_img = driver.find_element_by_xpath("//img[@class='image-0']")
            self.img.append(get_img.get_attribute("src"))
        #get_img1 = driver.find_element_by_xpath("//img[@class='image-1']")
        #self.img.append(get_img1.get_attribute("src"))

        # get image minus
        #URL_IMGS = driver.current_url
        #imgs = self.extract_imgs_box(url=URL_IMGS)

            box_prod_it = driver.find_elements_by_xpath('//div[@class="product-content__sheet-right"]')
            for i in box_prod_it:

                title = i.find_elements_by_xpath('//div[@class="product-content__sheet-right--name"]')
                self.title.append(title[0].text) # Recoger el titulo en el DOM.
           
                desc = i.find_elements_by_xpath('//div[@class="product-content__sheet-right--description"]')
                self.desc.append(desc[0].text) # Recoge la descripcion de los productos en el DOM.

                sku = i.find_elements_by_xpath('//div[@class="product-content__sheet-right--sku-reference"]')
                self.sku.append(sku[0].text)

                price = i.find_elements_by_xpath('//div[@class="product-content__sheet-right--price"]')
                self.price.append(self.price_calc(price[0].text))

                size = i.find_elements_by_xpath('//div[@class="sku-selector-container sku-selector-container-0"]')
                self.size.append(size[0].text)

                #box_color = i.find_elements_by_xpath('//div[@class="prateleira-similares__content"]')
                pass
            pass
        return self.title, self.desc, self.sku, self.price, self.size, self.img, self.code
    pass

title = []
desc = []
sku = []
price = []
size = []
code = []
img = []

_in = DOM()
cod_file = DOM.lector_file()

i = 0
while i < len(cod_file):

    
    buscador = driver.find_element_by_xpath('//input[@class="fulltext-search-box ui-autocomplete-input"]')
    time.sleep(rd.randint(2.0, 8.0))    
    
    buscador.send_keys(cod_file[i] + Keys.ENTER)
    time.sleep(rd.randint(2.0, 8.0))

    # variables de extraccion 
   
    tit, des, sk, pc, sz, im, model = _in.extract_elemt(cod_file[i])
    i = i + 1

    time.sleep(rd.randint(2.0, 8.0))
    driver.refresh()

    if i > len(cod_file):
        break
    else:
        continue
    pass

#print(tit)
#print(des)
#print(sk)
#print(pc)
#print(sz)
#print(im)
ds = DOM.load_xlsx("Sostenes")
ds["produc"] = tit
d["Desc"] = des 
ds["sku"] = sk
ds["img"] = im
ds["Precio"] = pc
ds["talla"] = sz
ds["Modelo"] = model
print(ds)
#df = pd.DataFrame(list(zip(title, desc, sku, price, size, code)),
#columns=["title", "descripcion", "sku", "price", "size", "code"])

#print(df.head(10))
ds.to_excel("intime_extract.xlsx", index=False)
