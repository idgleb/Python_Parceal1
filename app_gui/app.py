import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import sys
from typing import Literal
import io
import contextlib

# Asegurar que podamos importar módulos del directorio padre
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Importar funciones reutilizables
from ordenar_nombres import ordenar_nombres_alfabeticamente
from contar_frecuencia_nombres import contar_frecuencia_nombres
from exportar_frecuencias import exportar_frecuencias_a_archivo
from ordenar_por_longitud import ordenar_por_longitud_descendente
from filtrar_nombres_largos import filtrar_nombres_largos

# Matplotlib para gráficos embebidos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Procesamiento de Nombres - GUI")
        self.geometry("1200x650")

        self.selected_file: str | None = None
        self.loaded_names: list[str] = []
        self.last_view_kind: Literal["alpha", "freq", "filter", "len", "msg"] = "msg"

        self.create_widgets()

    def create_widgets(self) -> None:
        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        btn_select = tk.Button(top_frame, text="Seleccionar archivo", command=self.select_file)
        btn_select.pack(side=tk.LEFT)

        self.lbl_file = tk.Label(top_frame, text="Ningún archivo seleccionado", anchor="w")
        self.lbl_file.pack(side=tk.LEFT, padx=10)

        actions = tk.Frame(self)
        actions.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(actions, text="Ordenar alfabéticamente", command=self.action_sort_alpha).pack(side=tk.LEFT, padx=5)
        tk.Button(actions, text="Frecuencia por nombre", command=self.action_frequency).pack(side=tk.LEFT, padx=5)
        tk.Button(actions, text="Exportar frecuencias", command=self.action_export_freq).pack(side=tk.LEFT, padx=5)
        tk.Button(actions, text="Filtrar primer nombre > 4", command=self.action_filter_long_first).pack(side=tk.LEFT, padx=5)
        tk.Button(actions, text="Ordenar por longitud 1er nombre", command=self.action_sort_by_first_len).pack(side=tk.LEFT, padx=5)

        # Contenedor dividido: texto a la izquierda, gráfico a la derecha
        split = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RIDGE)
        split.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_panel = tk.Frame(split)
        right_panel = tk.Frame(split)
        split.add(left_panel, stretch="always")
        split.add(right_panel)

        self.output = scrolledtext.ScrolledText(left_panel, wrap=tk.WORD, height=25, width=80)
        self.output.pack(fill=tk.BOTH, expand=True)

        # Figura de Matplotlib
        self.fig = Figure(figsize=(5.5, 4.5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_visible(False)
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def select_file(self) -> None:
        file_path = filedialog.askopenfilename(title="Selecciona archivo de nombres",
                                               filetypes=[("Texto", "*.txt"), ("Todos", "*.*")])
        if not file_path:
            return
        self.selected_file = file_path
        self.lbl_file.config(text=file_path)
        self.loaded_names = []  # Reset
        self.last_view_kind = "msg"
        self.output_message("Archivo seleccionado. Usa un botón para procesar.")
        self.clear_chart()

    def ensure_file(self) -> bool:
        if not self.selected_file:
            messagebox.showwarning("Atención", "Primero selecciona un archivo .txt con nombres.")
            return False
        return True

    def output_message(self, text: str) -> None:
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, text)

    def clear_chart(self) -> None:
        self.ax.clear()
        self.ax.set_visible(False)
        self.canvas.draw_idle()

    def plot_bar(self, labels: list[str], values: list[int], title: str, xlabel: str = "", ylabel: str = "") -> None:
        self.ax.clear()
        self.ax.set_visible(True)
        # Limitar etiquetas largas para no saturar
        display_labels = [lbl if len(lbl) <= 18 else lbl[:16] + "…" for lbl in labels]
        self.ax.bar(range(len(values)), values, color="#4C78A8")
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.set_xticks(range(len(values)))
        self.ax.set_xticklabels(display_labels, rotation=45, ha="right")
        self.fig.tight_layout()
        self.canvas.draw_idle()

    def read_names_sorted(self) -> tuple[list[str], str]:
        # Reutiliza la función existente; captura salida y guarda nombres en memoria
        if not self.selected_file:
            return [], ""
        
        # Capturar la salida de la función
        output_buffer = io.StringIO()
        with contextlib.redirect_stdout(output_buffer):
            names = ordenar_nombres_alfabeticamente(self.selected_file)
        
        output_text = output_buffer.getvalue()
        self.loaded_names = names
        return names, output_text

    # Acciones
    def action_sort_alpha(self) -> None:
        if not self.ensure_file():
            return
        names, log_output = self.read_names_sorted()
        
        # Mostrar siempre el log capturado (contiene información útil sobre errores)
        if log_output.strip():
            self.output_message(log_output)
        elif not names:
            # Si no hay nombres ni log, mostrar mensaje genérico pero más útil
            self.output_message("[ERROR] No se pudieron obtener nombres del archivo.\n\nPosibles causas:\n• El archivo está vacío\n• El archivo contiene solo espacios o líneas vacías\n• El archivo no tiene el formato correcto (debe ser 'Nombre Apellido')\n• Error de permisos o codificación del archivo")
            self.clear_chart()
            return
        # Gráfico: conteo por inicial del primer nombre
        initials = {}
        for n in names:
            first = (n.split()[0] if n.split() else "?")
            key = first[0].upper() if first else "?"
            initials[key] = initials.get(key, 0) + 1
        labels, values = zip(*sorted(initials.items(), key=lambda x: (-x[1], x[0]))) if initials else ([], [])
        if labels:
            self.plot_bar(list(labels), list(values), "Conteo por inicial (primer nombre)", "Inicial", "Cantidad")
        else:
            self.clear_chart()
        self.last_view_kind = "alpha"

    def action_frequency(self) -> None:
        if not self.ensure_file():
            return
        if not self.loaded_names:
            names, _ = self.read_names_sorted()
        else:
            names = self.loaded_names
        if not names:
            self.output_message("No se pudieron obtener nombres.")
            self.clear_chart()
            return
        freq = contar_frecuencia_nombres(names)
        sorted_items = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
        lines = [f"{name}: {count}" for name, count in sorted_items]
        self.output_message("Frecuencia de nombres:\n" + "\n".join(lines))
        # Gráfico de barras de frecuencias
        if sorted_items:
            labels = [k for k, _ in sorted_items]
            values = [v for _, v in sorted_items]
            self.plot_bar(labels, values, "Frecuencia de primer nombre", "Nombre", "Frecuencia")
        else:
            self.clear_chart()
        self.last_view_kind = "freq"

    def action_export_freq(self) -> None:
        if not self.ensure_file():
            return
        if not self.loaded_names:
            names, _ = self.read_names_sorted()
        else:
            names = self.loaded_names
        if not names:
            messagebox.showerror("Error", "No se pudieron obtener nombres para exportar.")
            return
        freq = contar_frecuencia_nombres(names)
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="frecuencia_nombres.txt",
                                                 filetypes=[("Texto", "*.txt")])
        if not save_path:
            return
        ok = exportar_frecuencias_a_archivo(freq, save_path)
        if ok:
            messagebox.showinfo("Exportación", f"Frecuencias exportadas en:\n{save_path}")
        else:
            messagebox.showerror("Exportación", "No se pudo exportar el archivo.")

    def action_filter_long_first(self) -> None:
        if not self.ensure_file():
            return
        if not self.loaded_names:
            names, _ = self.read_names_sorted()
        else:
            names = self.loaded_names
        filtered = filtrar_nombres_largos(names, longitud_minima=4)
        if not filtered:
            self.output_message("No hay nombres que cumplan la condición.")
            self.clear_chart()
            return
        lines = [f"{idx+1:2d}. {name} (primer nombre '{name.split()[0]}')" for idx, name in enumerate(filtered)]
        self.output_message("Filtrado (primer nombre > 4):\n" + "\n".join(lines))
        # Gráfico: usar el nombre completo en X y la longitud del primer nombre en Y
        labels = [n for n in filtered]
        values = [len(n.split()[0]) for n in filtered]
        self.plot_bar(labels, values, "Longitud del primer nombre (filtrados)", "Nombre completo", "Longitud 1er nombre")
        self.last_view_kind = "filter"

    def action_sort_by_first_len(self) -> None:
        if not self.ensure_file():
            return
        if not self.loaded_names:
            names, _ = self.read_names_sorted()
        else:
            names = self.loaded_names
        sorted_by_len = ordenar_por_longitud_descendente(names)
        lines = [
            f"{idx+1:2d}. {name} (len 1er nombre: {len(name.split()[0])})" for idx, name in enumerate(sorted_by_len)
        ]
        self.output_message("Ordenado por longitud del primer nombre (desc):\n" + "\n".join(lines))
        # Gráfico: top 15 por longitud del primer nombre usando nombre completo en X
        top = sorted_by_len[:15]
        labels = [n for n in top]
        values = [len(n.split()[0]) for n in top]
        self.plot_bar(labels, values, "Top 15 longitudes del primer nombre", "Nombre completo", "Longitud 1er nombre")
        self.last_view_kind = "len"


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
