#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import markdown
import os
import subprocess
import sys

def markdown_to_html(markdown_file, html_file):
    """
    Convierte un archivo Markdown a HTML con formato profesional.
    """
    try:
        # Leer el archivo Markdown
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convertir Markdown a HTML
        md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])
        html_content = md.convert(markdown_content)
        
        # CSS para formato profesional
        css_content = """
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            font-size: 11pt;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
        }
        
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 30px;
            margin-bottom: 20px;
            font-size: 24pt;
        }
        
        h2 {
            color: #34495e;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
            margin-top: 25px;
            margin-bottom: 15px;
            font-size: 18pt;
        }
        
        h3 {
            color: #7f8c8d;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 14pt;
        }
        
        h4 {
            color: #95a5a6;
            margin-top: 15px;
            margin-bottom: 8px;
            font-size: 12pt;
        }
        
        code {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 3px;
            padding: 2px 4px;
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            color: #e83e8c;
        }
        
        pre {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            line-height: 1.4;
        }
        
        pre code {
            background: none;
            border: none;
            padding: 0;
            color: #333;
        }
        
        blockquote {
            border-left: 4px solid #3498db;
            margin: 15px 0;
            padding-left: 15px;
            color: #7f8c8d;
            font-style: italic;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
            font-size: 10pt;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        
        ul, ol {
            margin: 10px 0;
            padding-left: 25px;
        }
        
        li {
            margin: 5px 0;
        }
        
        hr {
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }
        
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 15px auto;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            text-align: center;
            font-size: 10pt;
            color: #7f8c8d;
            font-style: italic;
        }
        
        @media print {
            body {
                margin: 0;
                padding: 15mm;
            }
            
            h1 {
                page-break-before: auto;
            }
            
            h2, h3, h4 {
                page-break-after: avoid;
            }
            
            pre, blockquote {
                page-break-inside: avoid;
            }
        }
        """
        
        # Crear HTML completo
        full_html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Informe Final - Proyecto de Procesamiento de Nombres</title>
            <style>{css_content}</style>
        </head>
        <body>
            {html_content}
            <div class="footer">
                Informe - Proyecto de Procesamiento de Nombres<br>
                Desarrollado por: Ursol Gleb
            </div>
        </body>
        </html>
        """
        
        # Escribir archivo HTML
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        print(f"[EXITO] HTML generado exitosamente: {html_file}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error al generar HTML: {e}")
        return False

def html_to_pdf_with_chrome(html_file, pdf_file):
    """
    Convierte HTML a PDF usando Chrome/Chromium en modo headless.
    """
    try:
        # Comando para convertir HTML a PDF usando Chrome
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            "chrome",
            "chromium",
            "google-chrome"
        ]
        
        chrome_path = None
        for path in chrome_paths:
            try:
                if os.path.exists(path) or path in ["chrome", "chromium", "google-chrome"]:
                    chrome_path = path
                    break
            except:
                continue
        
        if not chrome_path:
            print("[ERROR] Chrome no encontrado. Instalando alternativa...")
            return False
        
        # Comando para generar PDF
        cmd = [
            chrome_path,
            "--headless",
            "--disable-gpu",
            "--print-to-pdf=" + os.path.abspath(pdf_file),
            "--print-to-pdf-no-header",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=5000",
            "file://" + os.path.abspath(html_file)
        ]
        
        print("[INFO] Convirtiendo HTML a PDF con Chrome...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and os.path.exists(pdf_file):
            print(f"[EXITO] PDF generado exitosamente: {pdf_file}")
            return True
        else:
            print(f"[ERROR] Error al convertir a PDF: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("[ERROR] Timeout al convertir a PDF")
        return False
    except Exception as e:
        print(f"[ERROR] Error al convertir HTML a PDF: {e}")
        return False

def markdown_to_pdf(markdown_file, output_file):
    """
    Convierte un archivo Markdown a PDF usando HTML como intermediario.
    """
    html_file = output_file.replace('.pdf', '.html')
    
    # Paso 1: Markdown a HTML
    if not markdown_to_html(markdown_file, html_file):
        return False
    
    # Paso 2: HTML a PDF
    if not html_to_pdf_with_chrome(html_file, output_file):
        print(f"[INFO] Se generó el archivo HTML: {html_file}")
        print("[INFO] Puedes abrirlo en un navegador y usar Ctrl+P para guardar como PDF")
        return False
    
    # Limpiar archivo HTML temporal
    try:
        os.remove(html_file)
        print("[INFO] Archivo HTML temporal eliminado")
    except:
        pass
    
    return True

if __name__ == "__main__":
    # Archivos de entrada y salida
    markdown_file = "INFORME_FINAL.md"
    output_file = "INFORME_FINAL.pdf"
    
    # Verificar que existe el archivo Markdown
    if not os.path.exists(markdown_file):
        print(f"[ERROR] No se encontró el archivo '{markdown_file}'")
        exit(1)
    
    print(f"[INFO] Convirtiendo '{markdown_file}' a PDF...")
    print("=" * 50)
    
    # Generar PDF
    success = markdown_to_pdf(markdown_file, output_file)
    
    if success:
        print("=" * 50)
        print(f"[EXITO] El informe PDF está listo: {output_file}")
        print(f"[INFO] Ubicación: {os.path.abspath(output_file)}")
    else:
        print("=" * 50)
        print("[ERROR] No se pudo generar el PDF")
        exit(1)
