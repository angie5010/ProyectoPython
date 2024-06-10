import pandas as pd  
import os  
from ..decorators.decorators import medirTiempo, registrarEjecucion  

@registrarEjecucion  # Decorador nuestro para ejecucion y finalizacion de la funcion
@medirTiempo  # Decorador nuestro para medir el tiempo que utiliza la funcion
def cargarDatos(rutaDatos):
    """
    Función que carga los datos desde un archivo CSV o Excel, si no es cualquiera de estos tipos arrojará un error.

    Parametros :
        rutaDatos (str) : Ruta del archivo a cargar.

    Retorna :
        pd.DataFrame: DataFrame de los datos cargados.

    Arroja :
        ValueError: Error de formato de archivo no procesado.
    """
    # Define si los datos se van a leer con funcion read_csv, si el archivo tiene extensión .csv, o read_excel si el archivo tiene extension .xlsx, si no arroja un error con mensaje personalizado
    if rutaDatos.endswith('.csv'):
        datos = pd.read_csv(rutaDatos)  
    elif rutaDatos.endswith('.xlsx'):
        datos = pd.read_excel(rutaDatos)  
    else:
        raise ValueError("El formato de archivo no es compatible")  
    print("Datos cargados exitosamente") 
    # Devuelve el DataFrame con los datos que fueron cargados
    return datos  

@registrarEjecucion  # Decorador nuestro para ejecucion y finalizacion de la funcion
@medirTiempo  # Decorador nuestro para medir el tiempo que utiliza la funcion
def limpiarDatos(datos):
    """
    Función que limpia los datos.

    Parametros :
        datos (pd.DataFrame) : DataFrame con los datos que se van a limpiar.

    Retorna :
        pd.DataFrame: DataFrame con los datos ya limpios y procesados
    """
    # Limpia cualquier caracter adicional innecesario y convierte la columna precios al tipo float
    datos['price'] = datos['price'].replace(r'[\$,]', '', regex=True).astype(float)  
    print("Datos Limpiados Correctamente") 
    # Devuelve el DataFrame con los datos del precio con el formato adecuado
    return datos  

@registrarEjecucion  # Decorador nuestro para ejecucion y finalizacion de la funcion
@medirTiempo  # Decorador nuestro para medir el tiempo que utiliza la funcion
def analizarDatos(datos):
    """
    Función que hace un análisis básico de los datos

    Parametros :
        datos (pd.DataFrame) : DataFrame con los datos a utilizar

    """
    print("Análisis de datos básico:") 
    # Muestra datos de estadística descriptiva básicos del dataframe
    print(datos.describe())  
    print("\nProductos con los precios más altos:") 
    # Muestra los 5 productos con los precios más altos
    print(datos.nlargest(5, 'price'))  

@registrarEjecucion  # Decorador nuestro para ejecucion y finalizacion de la funcion
@medirTiempo  # Decorador nuestro para medir el tiempo que utiliza la funcion
def guardarDatosProcesados(datos, rutaSalida):
    """
    Función que guarda los datos limpios y procesados en un csv o Excel

    Parametros :
        datos (pd.DataFrame) : DataFrame con los datos a guardar.
        rutaSalida (str) : Ruta del archivo de salida.

    Arroja :
        ValueError: Si el formato del archivo no es soportado.
    """
    # Define si los datos se van a guardar (ambos sin índice) con funcion .to_csv, si el archivo tiene extensión .csv, o to_excel si el archivo tiene extension .xlsx, si no arroja un error con mensaje personalizado
    if rutaSalida.endswith('.csv'):
        datos.to_csv(rutaSalida, index=False)  
    elif rutaSalida.endswith('.xlsx'):
        datos.to_excel(rutaSalida, index=False) 
    else:
        raise ValueError("Formato de archivo no es compatible") 
    # Imprime un mensaje indicando que los datos se guardaron correctamente en la ruta de salida
    print(f"Datos procesados guardados en la ruta: {rutaSalida}")  

if __name__ == "__main__":
    # Define la ruta del archivo de datos a leer, y la ruta del archivo en el que se guardarán los datos
    directorioBase="./datos/procesados"
    rutaDatos = "datos/no-procesados/productos.csv"  
    rutaSalida = "datos/procesados/productos-limpios.csv" 
    # Cargamos los datos desde el archivo de origen
    datos = cargarDatos(rutaDatos)  
    # Limpiamos los datos (el campo precio) que obtuvimos
    datos = limpiarDatos(datos)  
    # Analizamos e imprimimos los datos
    analizarDatos(datos)  
     # Crea el directorio de salida si no existe
    os.makedirs(directorioBase, exist_ok=True) 
    # Guarda los datos limpios en el archivo
    guardarDatosProcesados(datos, rutaSalida)  
