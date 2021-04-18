import requests
import csv
from bs4 import BeautifulSoup

url_principal = "https://docs.microsoft.com/en-us/power-bi/"

#Función que obtiene las url hijas de la página principal de documentación
def obtener_links(p_url):
    #Inicializamos la lista de salida
    lista_urls = []
    # Realizamos la llamada a requests
    response = requests.get(p_url)
    # Almacenamos el contenido de las web
    webpage = response.content
    # Creamos un objeto BeautifulSoup con el contenido
    soup = BeautifulSoup(webpage, "html.parser")
    # Buscamos los links y los almacenamos en una lista
    for i in soup.find_all('li'):
        for url in i.find_all('a'):
            hijo = url['href']
            #Descartamos las urls que no se basen en la url relativa de nuestro interes
            if not hijo.startswith("https"):
                lista_urls.append(p_url+hijo)
    #Quitamos duplicamos de la lista
    lista_urls = list(dict.fromkeys(lista_urls))
    return lista_urls

#Esta función obtiene el título, tiempo estimado de lectura y fecha de actualización de los artículos de documentación
def obtener_info(url):
    # Realizamos la llamada a requests
    response = requests.get(url)
    # Almacenamos el contenido de las web
    webpage = response.content
    # Creamos un objeto BeautifulSoup con el contenido
    soup = BeautifulSoup(webpage, "html.parser")
    # Buscamos los datos que queremos extraer y los almacenamos en una tupla
    try:
        # Tiempo de lectura
        tiempo = soup.find("li", {"class": "readingTime"}).string
        # Fecha de modificación
        fecha = soup.find("time").string
        # Título del artículo
        titulo = soup.title.string
        # Almacenamos los datos en una tupla
        resultado = (titulo, fecha, tiempo, url)
        return resultado
    except(ConnectionError, Exception):
        resultado_error=(None,None,None,url)
        return resultado_error

#Llamamos a la función que obtiene las urls y metemos los resultados en una lista
salida=obtener_links(url_principal)

#Para cada url de la lista llamamos a la función que obtiene la info que buscamos.
#Guardamos la información en una lista de tuplas
lista=[]
for web in salida:
    tupla=obtener_info(web)
    if tupla[0]!=None:
        lista.append(tupla)

#Guardamos la salida en un fichero
with open('D:/powerbidoc.csv','w', newline='') as out:
    csv_out=csv.writer(out,delimiter=';')
    csv_out.writerow(['Artículo','Fecha','Tiempo','URL'])
    for row in lista:
        csv_out.writerow(row)