#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unicodedata

def normalizar_para_ordenar(texto):
    """
    Normaliza un texto para ordenación alfabética correcta,
    manejando acentos y tildes apropiadamente.
    """
    # Remover acentos pero mantener la letra base
    texto_normalizado = unicodedata.normalize('NFD', texto)
    # Filtrar solo caracteres que no sean marcas diacríticas
    texto_sin_acentos = ''.join(c for c in texto_normalizado 
                               if unicodedata.category(c) != 'Mn')
    return texto_sin_acentos.lower()

def ordenar_nombres_alfabeticamente(archivo_entrada):
    """
    Lee nombres de un archivo y los ordena alfabéticamente.
    Incluye manejo robusto de errores para diferentes escenarios.
    """
    try:
        # Verificar si el archivo existe
        import os
        import sys
        import string

        # Impresión segura (evita UnicodeEncodeError en consolas Windows)
        def safe_print(text: str) -> None:
            encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
            try:
                print(text)
            except UnicodeEncodeError:
                print(text.encode(encoding, errors="replace").decode(encoding, errors="replace"))
        if not os.path.exists(archivo_entrada):
            print(f"[ERROR] El archivo '{archivo_entrada}' no existe.")
            return []
        
        # Verificar si el archivo está vacío
        if os.path.getsize(archivo_entrada) == 0:
            print(f"[ERROR] El archivo '{archivo_entrada}' está vacío.")
            return []
        
        # Leer el archivo con codificación UTF-8 para manejar acentos
        with open(archivo_entrada, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
        
        # Verificar si se pudieron leer líneas
        if not lineas:
            safe_print(f"[ERROR] No se pudieron leer líneas del archivo '{archivo_entrada}'.")
            return []
        
        # Limpiar líneas vacías y espacios en blanco
        nombres = [linea.strip() for linea in lineas if linea.strip()]
        
        # Verificar si hay nombres válidos después de la limpieza
        if not nombres:
            safe_print(f"[ERROR] El archivo '{archivo_entrada}' no contiene datos válidos.")
            safe_print("   El archivo puede contener solo líneas vacías o espacios en blanco.")
            return []
        
        # Validar que los nombres tengan formato válido (al menos un carácter alfanumérico)
        nombres_validos = []
        nombres_invalidos = []
        
        for nombre in nombres:
            nombre_limpio = nombre.strip()
            
            # Reglas estrictas para formato "Nombre Apellido":
            # - Solo letras, espacios y acentos (sin números, símbolos, barras invertidas)
            # - Al menos 2 palabras separadas por espacios
            # - Cada palabra debe tener al menos 2 letras
            tiene_barras = "\\" in nombre_limpio
            solo_letras_espacios = all(c.isalpha() or c.isspace() or c in "áéíóúüñÁÉÍÓÚÜÑ" for c in nombre_limpio)
            palabras = [palabra.strip() for palabra in nombre_limpio.split() if palabra.strip()]
            palabras_validas = all(len(palabra) >= 2 and palabra.isalpha() for palabra in palabras)
            
            es_valido = (
                bool(nombre_limpio)
                and not tiene_barras
                and solo_letras_espacios
                and len(palabras) >= 2
                and palabras_validas
            )

            if es_valido:
                nombres_validos.append(nombre_limpio)
            else:
                nombres_invalidos.append(nombre)
        
        # Mostrar advertencias sobre nombres inválidos si los hay
        if nombres_invalidos:
            safe_print(f"[ADVERTENCIA] Se encontraron {len(nombres_invalidos)} líneas con datos inválidos:")
            safe_print("   (Strings extraños, formato incorrecto, o solo espacios/saltos de línea)")
            for nombre_invalido in nombres_invalidos[:5]:  # Mostrar máximo 5 ejemplos
                safe_print(f"   - '{str(nombre_invalido)}'")
            if len(nombres_invalidos) > 5:
                safe_print(f"   ... y {len(nombres_invalidos) - 5} más.")
            safe_print("")
            
            # Si hay nombres válidos, mostrar mensaje de éxito parcial
            if nombres_validos:
                safe_print(f"[INFO] Sin embargo, se encontraron {len(nombres_validos)} nombres válidos que serán procesados.")
                safe_print("")
        
        # Verificar si quedan nombres válidos después del filtrado
        if not nombres_validos:
            print(f"[ERROR] No se encontraron nombres válidos en el archivo '{archivo_entrada}'.")
            return []
        
        # Ordenar usando la función de normalización personalizada
        nombres_ordenados = sorted(nombres_validos, key=normalizar_para_ordenar)
        
        safe_print("[EXITO] Nombres ordenados alfabéticamente:")
        safe_print("=" * 40)
        for i, nombre in enumerate(nombres_ordenados, 1):
            safe_print(f"{i:2d}. {nombre}")
        
        return nombres_ordenados
        
    except FileNotFoundError:
        print(f"[ERROR] No se pudo encontrar el archivo '{archivo_entrada}'.")
        print("   Verifica que la ruta del archivo sea correcta.")
        return []
    except PermissionError:
        print(f"[ERROR] No tienes permisos para leer el archivo '{archivo_entrada}'.")
        return []
    except UnicodeDecodeError as e:
        print(f"[ERROR] No se pudo decodificar el archivo '{archivo_entrada}'.")
        print(f"   Error de codificación: {e}")
        print("   El archivo puede estar en una codificación diferente a UTF-8.")
        return []
    except OSError as e:
        print(f"[ERROR] Error del sistema operativo al acceder al archivo '{archivo_entrada}': {e}")
        return []
    except Exception as e:
        try:
            print(f"[ERROR] Error inesperado al procesar el archivo '{archivo_entrada}': {e}")
            print(f"   Tipo de error: {type(e).__name__}")
        except UnicodeEncodeError:
            enc = (getattr(sys.stdout, 'encoding', None) or 'utf-8')
            msg = str(e).encode(enc, errors='replace').decode(enc, errors='replace')
            print(f"[ERROR] Error inesperado al procesar el archivo '{archivo_entrada}': {msg}")
            print(f"   Tipo de error: {type(e).__name__}")
        return []

if __name__ == "__main__":
    archivo = "nombres.txt"
    nombres_ordenados = ordenar_nombres_alfabeticamente(archivo)
    
    if nombres_ordenados:
        print(f"\nTotal de nombres procesados: {len(nombres_ordenados)}")
