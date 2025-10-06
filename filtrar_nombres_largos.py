# -*- coding: utf-8 -*-

# Importar la función para leer nombres del archivo ordenar_nombres.py
from ordenar_nombres import ordenar_nombres_alfabeticamente

def filtrar_nombres_largos(nombres, longitud_minima=4):
    """
    Filtra una lista de nombres completos para obtener solo aquellos cuyo
    primer nombre tenga más de la longitud mínima especificada.
    
    Args:
        nombres (list): Lista de nombres completos
        longitud_minima (int): Longitud mínima de caracteres del primer nombre (por defecto 4)
        
    Returns:
        list: Lista filtrada de nombres completos que cumplen la condición
    """
    nombres_filtrados = []
    
    for nombre_completo in nombres:
        primer_nombre = nombre_completo.split()[0]  # Obtener solo el primer nombre
        if len(primer_nombre) > longitud_minima:
            nombres_filtrados.append(nombre_completo)
    
    return nombres_filtrados

def mostrar_nombres_filtrados(nombres_originales, nombres_filtrados):
    """
    Muestra los resultados del filtrado de manera clara.
    """
    print("Filtrado de nombres por longitud del primer nombre:")
    print("=" * 50)
    print(f"Longitud mínima del primer nombre: más de 4 caracteres")
    print(f"Total de nombres originales: {len(nombres_originales)}")
    print(f"Total de nombres filtrados: {len(nombres_filtrados)}")
    print()
    
    print("Nombres que cumplen la condición:")
    print("-" * 40)
    for i, nombre in enumerate(nombres_filtrados, 1):
        primer_nombre = nombre.split()[0]
        print(f"{i:2d}. {nombre} (primer nombre: '{primer_nombre}' - {len(primer_nombre)} caracteres)")
    
    print()
    print("Nombres que NO cumplen la condición:")
    print("-" * 40)
    nombres_no_cumplen = []
    for nombre in nombres_originales:
        primer_nombre = nombre.split()[0]
        if len(primer_nombre) <= 4:
            nombres_no_cumplen.append(nombre)
    
    for i, nombre in enumerate(nombres_no_cumplen, 1):
        primer_nombre = nombre.split()[0]
        print(f"{i:2d}. {nombre} (primer nombre: '{primer_nombre}' - {len(primer_nombre)} caracteres)")

if __name__ == '__main__':
    # Leer nombres del archivo nombres.txt usando la función de ordenar_nombres.py
    archivo = "nombres.txt"
    nombres_originales = ordenar_nombres_alfabeticamente(archivo)
    
    if nombres_originales:
        # Filtrar nombres que tengan más de 4 caracteres
        nombres_filtrados = filtrar_nombres_largos(nombres_originales, longitud_minima=4)
        
        # Mostrar resultados
        mostrar_nombres_filtrados(nombres_originales, nombres_filtrados)
        
        print(f"\nResumen:")
        print(f"- Nombres originales: {len(nombres_originales)}")
        print(f"- Nombres con más de 4 caracteres: {len(nombres_filtrados)}")
        print(f"- Nombres con 4 caracteres o menos: {len(nombres_originales) - len(nombres_filtrados)}")
