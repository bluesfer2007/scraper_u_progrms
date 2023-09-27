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
from urllib.parse import urljoin



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
    

# def auxiliar para extraer nombres generar lista de etiqueta a obtener
def nombre_ucsg(site):
    new_site=site
    url='https://www.ucsg.edu.ec/posgrado/maestria/'
    html_page=page.HomePage(new_site, url)
    figure=html_page.figure_posgrado
    #elemento=figure.find_all('figure')
    return figure

def get_name_ucsg(figure):

    return figure.get_text(strip=True)

def get_url_ucsg(figure):
    url_base='https://www.ucsg.edu.ec'
    urls_figur=figure.select('a')
    urls_figur=[ urljoin(url_base, x.get('href')) for x in urls_figur]
    #url_completa=urljoin(url_base,urls_figur)
    return urls_figur

# datos ucsg caso especial
def generar_diccionario_ucsg(site, figure):
    datos={}
    new_site=site
    
    #nombre de programa
    titulo_programa=get_name_ucsg(figure)
    if titulo_programa:
        datos['nombre_programa']=titulo_programa
    else: 
        datos['nombre_programa']=None
    #precio de programa

    #nombre universidad
    datos['IES']=site

    url=get_url_ucsg(figure)
    if url:
        datos['url']=url
    else:
        datos['url']=None
    datos['fecha_consulta']=datetime.fromisoformat(str(datetime.now()))
    
    return datos


if __name__=='__main__':
    site='grego'
    #uasb=['https://www.uasb.edu.ec/programa/?tipoPrograma=maestria-profesional', 'https://www.uasb.edu.ec/programa/page/2/?tipoPrograma=maestria-profesional', 'https://www.uasb.edu.ec/programa/page/3/?tipoPrograma=maestria-profesional', 'https://www.uasb.edu.ec/programa/page/4/?tipoPrograma=maestria-profesional']
    links=url_posgrados_info(site)
    print(links)
    #data_urls=[]
    #for x in links:
    #    data_urls.append(url_posgrados_info(site, x))
    #urls_pro=url_posgrados_info(site,uasb[1])
    #flat_url=[x for j in data_urls for x in j]
    #print(len(flat_url))
    
    #print(valid_t)
    #data=[]
    #for j, x in enumerate(flat_url):
    #    print(f'va en el link numero {j}')
    #    try:
    #        data.append(dato_page(site,x))
    #    except:
    #        pass
    #df=pd.DataFrame(data)
    #df.to_csv('datos_base/datos_post_'+site+'.csv')
    #print(dato_page(site, urls[0]))
 

   