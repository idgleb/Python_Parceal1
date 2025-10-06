# -*- coding: utf-8 -*-

# Importar la función para leer nombres del archivo ordenar_nombres.py
from ordenar_nombres import ordenar_nombres_alfabeticamente

def contar_frecuencia_nombres(nombres):
    frecuencia = {}
    for nombre_completo in nombres:
        primer_nombre = nombre_completo.split()[0]
        if primer_nombre in frecuencia:
            frecuencia[primer_nombre] += 1
        else:
            frecuencia[primer_nombre] = 1
    return frecuencia

if __name__ == '__main__':
    # Leer nombres del archivo nombres.txt usando la función de ordenar_nombres.py
    archivo = "nombres.txt"
    nombres = ordenar_nombres_alfabeticamente(archivo)
    
    if nombres:
        resultado = contar_frecuencia_nombres(nombres)
        # Mostrar frecuencias
        print("\nFrecuencia de nombres:")
        print("=" * 30)
        frecuencias_ordenadas = sorted(resultado.items(), key=lambda x: (-x[1], x[0]))
        for nombre, frecuencia in frecuencias_ordenadas:
            print(f"{nombre}: {frecuencia}")
