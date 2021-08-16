import time
import random as rd
import pandas as pd
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

        pass

    def lector_file():

        """
        Carga automatica de los codigos,
        de identificacion escritos en file txt.
        """
    
        with open("COD.txt", "r") as file:
            l_COD = [line.rstrip() for line in file]
        return l_COD

    def load_xlsx(self, FILE, sheets):

        ds = pd.read_excel("scraping_data.xlsx",
                sheet_name=sheets, header=None,
                names=["produc", "Cant/char", "CodUniversal", 
                    "color", "colo_comercial", "talla", "img",
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

    def extract_elemt(self):

        box_items = driver.find_elements_by_xpath('//div[@class="section__prateleira-product"]')
        for iter in box_items:
            items = iter.find_element_by_class_name('product-image')
            items.click()
            pass

        # get image
        img = driver.find_element_by_class_name("image-0").get_attribute("src")

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

            box_color = i.find_elements_by_xpath('//div[@class="prateleira-similares__content"]')

            pass
        return self.title, self.desc, self.sku, self.price, self.size
    pass

title = []
desc = []
sku = []
price = []
size = []
code = []

buscador = driver.find_element_by_xpath('//input[@class="fulltext-search-box ui-autocomplete-input"]')
cod_file = DOM.lector_file()
for j in range(0, len(cod_file)):
    buscador.send_keys(str(cod_file[j]) + Keys.ENTER)
    time.sleep(rd.randint(2.0, 8.0))
    _in = DOM()

    # variables de extraccion 
    tit, des, sk, pc, sz = _in.extract_elemt()

    # listar todos los elementos extraidos
    title.append(tit)
    desc.append(desc)
    sku.append(sku)
    price.append(pc)
    size.append(sz)
    code.append(cod_file[j])


df = pd.DataFrame(list(zip(title, desc, sku, price, size, code)),
    columns=["title", "descripcion", "sku", "price", "size", "code"])

df.head(10)

