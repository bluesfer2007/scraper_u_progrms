import requests
import reportes
from yaml import parse
import reportes.scraper_pos as page
import bs4
from bs4 import BeautifulSoup
from reportes.common_config import config
import re
import pandas as pd
from datetime import datetime



#dejar listado de posgrados que se encuentren
def url_posgrados_info(site):
    new_site=site
    url=config()['site_scraper'][site]['base_url']
    html_page=page.HomePage(new_site, url)
    url_padre_posgrdo=html_page.filt_posgrado
    nivel_url2=page.HomePage(site,url_padre_posgrdo)
    posgrados_links=nivel_url2.solo_posgrados
    return posgrados_links

#diccionario obtener datos de cada link de posgrado

def dato_page(site,url):
    datos={}
    new_site=site
    html_page=page.InfoProgram(new_site, url)
    #nombre de programa
    titulo_programa=html_page.titulo_espe
    if titulo_programa:
        datos['nombre_programa']=titulo_programa
    else: 
        datos['nombre_programa']=None
    #precio de programa
    precio=html_page.get_price
    if precio:
        datos['precio']=precio
    else:
        datos['precio']=None
    #nombre universidad
    datos['IES']=site
    datos['url']=url
    datos['fecha_consulta']=datetime.fromisoformat(str(datetime.now()))
    
    return datos
    




if __name__=='__main__':
    site='usfq'
    urls=url_posgrados_info(site)

    data=[]
    for j, x in enumerate(urls):
        print(f'va en el link numero {j}')
        try:
            data.append(dato_page(site,x))
        except:
            pass
    df=pd.DataFrame(data)
    df.to_csv('datos_base/datos_post_'+site+'.csv')
    #print(dato_page(site, urls[0]))

   