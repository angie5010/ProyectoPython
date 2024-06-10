import time  
import logging 

# Configuración de logger (parametro level: define el nivel de los mensajes que se loggean, será del nivel INFO y superiores)
# (parametro format, setea el formato de los mensajes a imprimir marca de tiempo (asctime), nivel (INFO o superiores) de mensaje (levelname) , message (mensaje personalizado))
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def medirTiempo(funcion):
    """Decorador que mide el tiempo de ejecución que requiere una función.

        Parametros: 
            funcion: Función a la que se le medirá el tiempo de ejecución
    """
    def wrapper(*args, **kwargs):
        # Guarda el tiempo actual como tiempo de inicio
        tiempoInicio = time.time()  
        # Ejecuta la función que se recibió como parámetro
        resultado = funcion(*args, **kwargs)  
        # Guarda el tiempo actual como tiempo de finalización
        tiempoFin = time.time()  
        # Calcula el tiempo transcurrido restando el tiempo de finalización con el tiempo de inicio
        tiempoTranscurrido = tiempoFin - tiempoInicio 
        # Registra el mensaje que se mostrará en los logs
        logging.info(f"La función {funcion.__name__} fue ejecutada en {tiempoTranscurrido:.4f} segundos")  
        # Devuelve el resultado de la ejecución de la función
        return resultado  
    # Devuelve el decorador
    return wrapper  

def registrarEjecucion(funcion):
    """Decorador para registrar la ejecución y finalización de una función.
    
        Parametros: 
            funcion: Función a la que se le registrará el inicio y el fin de ejecución
            """
    def wrapper(*args, **kwargs):
        # Registra en los logs un mensaje de la función cuando está a punto de ser ejecutada
        logging.info(f"Ejecutando la función {funcion.__name__}")  
        # Ejecuta la función recibida como parámetro
        resultado = funcion(*args, **kwargs)  
        # Registra en los logs un mensaje cuando se termina de ejecutar la función
        logging.info(f"Ejecución de la función {funcion.__name__} completada")  
        # Devuelve los datos de la función
        return resultado  
    # Devuelve el decorador
    return wrapper  
