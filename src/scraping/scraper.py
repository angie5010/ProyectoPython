import requests 
import os  
from bs4 import BeautifulSoup 
import pandas as pd 

def fetch_page(url):

    """
    Función para obtener el contenido de una página.
    
    Parametros :
        url : URL de la pagina web de la que se va a obtener el contenido

    Retorna :
        str: Contenido de la página web en string

    Raises :
        System exit: Si la solicitud HTTP devuelve un codigo que no sea 200
    """
    # Se realiza una solicitud get a la url, si el status code da 200, devolvemos el content del sitio web, sino, arrojamos una excepción
    respuesta= requests.get(url) 
    if respuesta.status_code == 200: 
        return respuesta.content 
    else:
        raise Exception(f"Failed to fetch page: {url}") 

def parse_product(producto):
    """
    Función para analizar producto
    
    Parametros :
        producto (bs4.element.Tag) : Objeto BeautifulSoup con los datos del producto.

    Retorna :
        dict: Diccionario con Titulo (title), Descripción (description) y Precio (price) del producto

    """
    # Se encuentra el titulo del producto
    titulo= producto.find("a",class_="title").text.strip() 
    # Se encuentra la descripcion del producto
    descripcion = producto.find("p",class_="description").text.strip() 
    # Se encuentra el precio del producto
    precio = producto.find("h4",class_="price").text.strip() 
    # Se crea y se retorna un diccionario con los datos obtenidos
    return{  
        "title":titulo,
        "description":descripcion,
        "price":precio,
    }

def scrape(url):
    """
    Función de scraping para diferentes páginas
    
    Parametros :
        url (str) : URL de la pagina web a scraoear.

    Retorna :
        pd.DataFrame : DataFrame con los datos de los productos
    """
    # Obtenemos el contenido de la web con nuestra función
    contenido = fetch_page(url) 
    # Se utiliza BeautifulSoup para nalizar el contenido de la página
    contenidoAnalizado = BeautifulSoup(contenido, "html.parser") 
    # Se obtienen todos los divs que contengan una clase "thumbnail", las cuales serán los productos
    productos = contenidoAnalizado.find_all("div", class_="thumbnail") 
    #Se inicializa una lista para almacenar los datos
    datosProducto=[] 
    #Se itera por cada uno de los productos que se obtuvieron
    for producto in productos:
        # Analizamos con nuestra función el producto de la iteración actual
        informacionProducto = parse_product(producto) 
        # Agregamos los datos analizados a nuestra lista
        datosProducto.append(informacionProducto) 
    #se crea y se retorna nuestra lista de productos transformada en un dataframe
    return pd.DataFrame(datosProducto)


# Se define la URL para scrapear
url_base="https://webscraper.io/test-sites/e-commerce/allinone"
# Se llama a la función scrape para analizar la url base y se imprime este resultado
dataScrapeada = scrape(url_base)
print(dataScrapeada)
# Definimos los directorios a utilizar para guardar la información
directorioBase="./datos/no-procesados"
rutaAGuardar='datos/no-procesados/productos.csv'
# Crea el directorio de salida
os.makedirs(directorioBase, exist_ok=True)  
# Se guardan los datos en un archivo .csv sin índice
dataScrapeada.to_csv(rutaAGuardar, index=False) 