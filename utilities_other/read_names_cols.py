import os
import requests
import bs4
from bs4 import BeautifulSoup

url='https://portal.inshosteddata.com/docs'

def get_r_s(url):
    r=requests.get(url)
    if r.status_code==200:
        s=BeautifulSoup(r.text,'lxml')
    return s

#metodo obtener todas la tablas de url
def tables_documentation(s):
     tables=s.find_all('table')
     return tables

def get_name_file(s):
    names=s.find_all('h2')
    name_list=[x.find('a') for x in names if x !=None]
    nombres=[]
    for i in name_list:
            try:
                nombres.append(i.get_text())
            except:
                 pass
    
    return nombres

#metodo para obtener los texto de cada columna para query sql
def get_text_rows_type(table):
     nombres_cols=[]
     tipo_cols=[]
     col_text=table.find_all('td')
     
     for i in range(0,len(col_text),3):
          nombres_cols.append(col_text[i].get_text())
     
     for x in range(1,len(col_text),3):
          tipo_cols.append(col_text[x].get_text())
     result=', '.join([f'{a} {b}' for a, b in zip(nombres_cols, tipo_cols)])
          
     return result

def save_in_disk(name,texto):
     with open('query_psql/'+name+'.txt','w') as f:
          for i in texto:
            f.write(i)

if __name__=='__main__':
    list_files=os.listdir('query_psql/')
    print(len(list_files))