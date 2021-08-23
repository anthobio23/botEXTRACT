#!/usr/bin/python3

import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

class process: 

    def __init__():
        pass

    def load_file(fcode):

        """
        Carga automatica de los codigos de itendificaicon
        escritos en archivo txt.
        """

        with open(fcode, "r") as file:

            lCOD = [line.rstrip() for line in file]
            pass
        return lCOD
    pass

if __name__ == "__main__":
    pass
