# -*- coding: utf-8 -*-

def capitalizar_titulo(texto, palabras_excepciones=None):
    """
    Capitaliza la primera letra de cada palabra en un texto, excepto para
    palabras específicas que se mantienen en minúsculas.
    
    Args:
        texto (str): El texto a capitalizar
        palabras_excepciones (list): Lista de palabras que no se capitalizarán
                                   (por defecto: ["y", "el", "la", "en", "de", "del", "con", "por", "para"])
    
    Returns:
        str: El texto capitalizado según las reglas especificadas
    """
    if palabras_excepciones is None:
        palabras_excepciones = ["y", "el", "la", "en", "de", "del", "con", "por", "para", "un", "una", "los", "las"]
    
    # Dividir el texto en palabras
    palabras = texto.split()
    palabras_capitalizadas = []
    
    for i, palabra in enumerate(palabras):
        # Limpiar la palabra de signos de puntuación para la comparación
        palabra_limpia = palabra.lower().strip(".,;:!?()[]{}'\"")
        
        # Solo capitalizar si no está en excepciones
        if palabra_limpia not in palabras_excepciones:
            # Capitalizar manteniendo signos de puntuación
            palabra_capitalizada = palabra.capitalize()
        else:
            # Mantener en minúsculas
            palabra_capitalizada = palabra.lower()
        
        palabras_capitalizadas.append(palabra_capitalizada)
    
    return " ".join(palabras_capitalizadas)

def probar_funcion():
    """
    Prueba la función con varios ejemplos de texto.
    """
    print("Pruebas de la función capitalizar_titulo:")
    print("=" * 50)
    
    # Ejemplo 1: Título de libro
    texto1 = "el señor de los anillos y la comunidad del anillo"
    resultado1 = capitalizar_titulo(texto1)
    print(f"Texto original: {texto1}")
    print(f"Resultado: {resultado1}")
    print()
    
    # Ejemplo 2: Título de artículo
    texto2 = "la historia de españa en el siglo xv y su influencia en el mundo"
    resultado2 = capitalizar_titulo(texto2)
    print(f"Texto original: {texto2}")
    print(f"Resultado: {resultado2}")
    print()
    
    # Ejemplo 3: Título con excepciones personalizadas
    texto3 = "mi viaje por el mundo y las aventuras en el mar"
    excepciones_personalizadas = ["y", "el", "en"]
    resultado3 = capitalizar_titulo(texto3, excepciones_personalizadas)
    print(f"Texto original: {texto3}")
    print(f"Excepciones: {excepciones_personalizadas}")
    print(f"Resultado: {resultado3}")
    print()
    
    # Ejemplo 4: Texto con signos de puntuación
    texto4 = "el arte de la guerra (y la paz) en el mundo moderno"
    resultado4 = capitalizar_titulo(texto4)
    print(f"Texto original: {texto4}")
    print(f"Resultado: {resultado4}")
    print()
    
    # Ejemplo 5: Párrafo completo
    parrafo = """
    el desarrollo de la inteligencia artificial y su impacto en la sociedad 
    moderna ha transformado la manera en que vivimos y trabajamos. 
    desde el surgimiento de los primeros algoritmos hasta las redes neuronales 
    actuales, la tecnología ha evolucionado de manera exponencial.
    """
    resultado_parrafo = capitalizar_titulo(parrafo.strip())
    print("Párrafo completo:")
    print(f"Texto original: {parrafo.strip()}")
    print(f"Resultado: {resultado_parrafo}")

def demostrar_excepciones():
    """
    Demuestra cómo funcionan las excepciones con diferentes listas.
    """
    print("\nDemostración de excepciones personalizadas:")
    print("=" * 50)
    
    texto = "el rey y la reina de inglaterra en el palacio de buckingham"
    
    # Sin excepciones (todas las palabras se capitalizan)
    resultado1 = capitalizar_titulo(texto, [])
    print(f"Sin excepciones: {resultado1}")
    
    # Con excepciones por defecto
    resultado2 = capitalizar_titulo(texto)
    print(f"Excepciones por defecto: {resultado2}")
    
    # Con excepciones personalizadas
    excepciones = ["y", "de"]
    resultado3 = capitalizar_titulo(texto, excepciones)
    print(f"Excepciones personalizadas {excepciones}: {resultado3}")

if __name__ == "__main__":
    # Ejecutar las pruebas
    probar_funcion()
    demostrar_excepciones()
    
    print("\n" + "=" * 50)
    print("Función lista para usar:")
    print("capitalizar_titulo(texto, palabras_excepciones)")
    print("=" * 50)
