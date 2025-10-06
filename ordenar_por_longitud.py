# -*- coding: utf-8 -*-

# Importar la función para leer nombres del archivo ordenar_nombres.py
from ordenar_nombres import ordenar_nombres_alfabeticamente

def ordenar_por_longitud_descendente(nombres):
    """
    Ordena una lista de nombres por longitud del primer nombre de forma descendente
    (de mayor a menor longitud del primer nombre).
    
    Args:
        nombres (list): Lista de nombres completos
        
    Returns:
        list: Lista ordenada por longitud del primer nombre descendente
    """
    # Ordenar por longitud del primer nombre descendente (de mayor a menor)
    nombres_ordenados = sorted(nombres, key=lambda nombre: len(nombre.split()[0]), reverse=True)
    return nombres_ordenados

def mostrar_nombres_por_longitud(nombres_ordenados):
    """
    Muestra los nombres ordenados por longitud del primer nombre de manera clara.
    """
    print("Nombres ordenados por longitud del primer nombre (descendente):")
    print("=" * 60)
    
    for i, nombre in enumerate(nombres_ordenados, 1):
        primer_nombre = nombre.split()[0]
        longitud_primer_nombre = len(primer_nombre)
        print(f"{i:2d}. {nombre} (primer nombre: '{primer_nombre}' - {longitud_primer_nombre} caracteres)")
    
    print()
    print("Estadísticas de longitud del primer nombre:")
    print("-" * 40)
    
    # Calcular estadísticas del primer nombre
    longitudes_primer_nombre = [len(nombre.split()[0]) for nombre in nombres_ordenados]
    longitud_maxima = max(longitudes_primer_nombre)
    longitud_minima = min(longitudes_primer_nombre)
    longitud_promedio = sum(longitudes_primer_nombre) / len(longitudes_primer_nombre)
    
    print(f"Longitud máxima del primer nombre: {longitud_maxima} caracteres")
    print(f"Longitud mínima del primer nombre: {longitud_minima} caracteres")
    print(f"Longitud promedio del primer nombre: {longitud_promedio:.1f} caracteres")
    
    # Agrupar por longitud del primer nombre
    print()
    print("Distribución por longitud del primer nombre:")
    print("-" * 45)
    longitudes_unicas = sorted(set(longitudes_primer_nombre), reverse=True)
    for longitud in longitudes_unicas:
        nombres_con_longitud = [nombre for nombre in nombres_ordenados if len(nombre.split()[0]) == longitud]
        print(f"{longitud} caracteres: {len(nombres_con_longitud)} nombres")
        for nombre in nombres_con_longitud:
            primer_nombre = nombre.split()[0]
            print(f"  - {nombre} (primer nombre: '{primer_nombre}')")

if __name__ == '__main__':
    # Leer nombres del archivo nombres.txt usando la función de ordenar_nombres.py
    archivo = "nombres.txt"
    nombres_originales = ordenar_nombres_alfabeticamente(archivo)
    
    if nombres_originales:
        # Ordenar por longitud descendente
        nombres_ordenados = ordenar_por_longitud_descendente(nombres_originales)
        
        # Mostrar resultados
        mostrar_nombres_por_longitud(nombres_ordenados)
        
        print(f"\nResumen:")
        print(f"- Total de nombres: {len(nombres_ordenados)}")
        print(f"- Nombres ordenados de mayor a menor longitud")
