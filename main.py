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

#declarar listado de urls desde pandas as
def open_urlxls(name_web):
    df=pd.read_excel('data_urls.xlsx', sheet_name='URLS_DATA')
    url=df[df['name']==name_web]
    return list(url['URL_PASAR'])

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

    #precio de programa matricula
    precio_matric=html_page.get_price_matric
    if precio_matric:
        datos['precio_matric']=precio_matric
    else:
        datos['precio_matric']=None
    #define precio de arancel si estan separados
    precio_aran=html_page.get_precio_arancel
    if precio_aran:
        datos['precio_aran']=precio_aran
    else:
        datos['precio_aran']=None

    #define valor de inscipcion si existe
    precio_inscrip=html_page.get_precio_inscrip
    if precio_inscrip:
        datos['precio_ins']=precio_inscrip
    else:
        datos['precio_ins']=None

    #define la modalidad del programa si es que existe
    modalid_=html_page.get_modalidad
    if modalid_:
        datos['modalidad_prog']=modalid_
    else:
        datos['modalidad_prog']=None


    #define duracion del programa
    durac_prog=html_page.get_duracion
    if durac_prog:
        datos['duracion']=durac_prog
    else:
        datos['duracion']=None
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
    site='usboli'
    #links=url_posgrados_info(site)
    listado_url=open_urlxls(site)
    #mandar scraper masivo para pagina
    data=[]
    for j, x in enumerate(listado_url):
        print(f'va en el link numero {j}')
        try:
            data.append(dato_page(site,x))
        except:
            pass
    df=pd.DataFrame(data)
    df.to_csv('datos_base/datos_post_'+site+'.csv')
    #numero=14
    #print(listado_url[numero])
    #rint(dato_page(site, listado_url[numero]))