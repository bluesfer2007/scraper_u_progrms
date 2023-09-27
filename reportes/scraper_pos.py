import os
import pandas as pd
import requests
import bs4
from bs4 import BeautifulSoup
from reportes.common_config import config
from urllib.parse import urljoin

import re
#from reportes import config_s as cf

class Scraper:
    def __init__(self, new_site_uid, url):
        self.__config=config()['site_scraper'][new_site_uid] #la variable define el sitio a scrapear
        self._url_base=self.__config['base_url']
        self._queries=self.__config['query']
        self._html=None

        self._visit(url)

    def _select(self, query_str):
        return self._html.select(query_str)
    
    def _visit(self, url):
        response=requests.get(url, headers={"User-Agent": "xy"})
        response.raise_for_status()
        self._html=bs4.BeautifulSoup(response.text, 'lxml')

#iniciar clase copn metodos para usar queries y obtener datos
#esto es una super clase que hereda los metodos de Scraper
class HomePage(Scraper):
    #esto es el iniciador de la super clase es decir necesita los
    #atributos de la clase original para poderse iniciar
    def __init__(self, new_site_uid, url):
        super().__init__(new_site_uid, url)

    #obtener los links de la pagina web
    @property
    def programs_links(self):
        links_list=[]
        for link in self._select(self._queries['program_links']):
            if link and link.has_attr('href'):
                links_list.append(link)
        return set(urljoin(self._url_base,link['href']) for link in links_list)
    
    @property
    def programs_link_uasb(self):
        links_list=[]
        for link in self._select(self._queries['program_links']):
            if link and link.has_attr('href'):
                links_list.append(link)
        return set(urljoin(self._url_base,link['href']) for link in links_list)



    
    @property
    def filt_posgrado(self):
        urls=self.programs_links
        url_posgrado=[x for x in urls if re.findall(self._queries['es_posgrado'], x)]
        return url_posgrado[0]
    
    @property
    def solo_posgrados(self):
        urls=self.programs_link_uasb
        urls_pos=[x for x in urls if self._queries['texto_pos'] in x]
        return urls_pos
    
    #nombre posgrados y modalidad
    @property
    def figure_posgrado(self):
        figure_text=self._select(self._queries['titles_program'])
        #texto=[x.get_text(strip=True) for x in figure_text]
        #texto=[x.select('a') for x in figure_text]
        
        return figure_text

    
#nueva clase para obtener el contenido de cada link_programa
class InfoProgram(Scraper):
    def __init__(self, new_site_uid, url):
        super().__init__(new_site_uid, url)


    @property
    def titulo_espe(self):
        result=self._select(self._queries['titles_program'])
        return result[0].get_text(strip=True) if len(result) else ''
    
    @property
    def get_price(self):
        result=self._select(self._queries['price_progra'])
        if len(result)>0:
            result=result[0].get_text()
        else:
            result=['<h1>no hay precio</h1>']
        return result
    
    @property 
    def get_duracion(self):
        result=self._select(self._queries['duracion_prog'])
        year=result[0].get_text()
        return year
    
    @property 
    def creditos_pro(self):
        result=self._select(self._queries['creditos_pro'])
        creditos=[x.get_text(strip=True) for x in result]
        return creditos