import requests
import reportes
from yaml import parse
import reportes.scraper_pos as page
import bs4
from bs4 import BeautifulSoup
from reportes.common_config import config
import re

def especi_medic(li):

    pass



if __name__=='__main__':
    new_site=config()["site_scraper"]["usfq"]
    url=config()['site_scraper']['usfq']['url_usfq']
    link=page.HomePage('usfq', url)
    url=[x for x in link.programs_links if re.findall(r'posgrado', x)]
    test_ti=page.InfoProgram('usfq',url[0])
    print(test_ti.creditos_pro, url[0])
    