# -*- coding: utf-8 -*-

# Importar las funciones de los archivos existentes
from contar_frecuencia_nombres import contar_frecuencia_nombres
from ordenar_nombres import ordenar_nombres_alfabeticamente

def exportar_frecuencias_a_archivo(frecuencias, archivo_salida):
    """
    Exporta el diccionario de frecuencias a un archivo de texto.
    Cada línea contiene un nombre y su frecuencia separados por dos puntos.
    
    Args:
        frecuencias (dict): Diccionario con nombres y sus frecuencias
        archivo_salida (str): Nombre del archivo de salida
    """
    try:
        with open(archivo_salida, 'w', encoding='utf-8') as archivo:
            
            for nombre, frecuencia in frecuencias.items():
                archivo.write(f"{nombre}: {frecuencia}\n")
        
        print(f"Frecuencias exportadas exitosamente a '{archivo_salida}'")
        return True
        
    except Exception as e:
        print(f"Error al exportar las frecuencias: {e}")
        return False

if __name__ == '__main__':
    # Leer nombres del archivo nombres.txt usando la función de ordenar_nombres.py
    archivo = "nombres.txt"
    nombres = ordenar_nombres_alfabeticamente(archivo)
    
    if nombres:
        # Calcular frecuencias
        frecuencias = contar_frecuencia_nombres(nombres)
        
        # Exportar a archivo
        archivo_salida = "frecuencia_nombres.txt"
        print("Exportando frecuencias de nombres a archivo....")
        print("=" * 30)
        if exportar_frecuencias_a_archivo(frecuencias, archivo_salida):
            print(f"Archivo '{archivo_salida}' creado exitosamente")
