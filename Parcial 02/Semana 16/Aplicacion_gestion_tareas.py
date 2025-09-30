import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
from datetime import datetime
import json
import os

from tkcalendar import Calendar  # Necesitas instalar tkcalendar

ARCHIVO_JSON = "tareas.json"

# Colores pastel y fuentes
COLOR_FONDO = "#f7f5f2"
COLOR_BOTON = "#c2dedc"
COLOR_BOTON_COMPLETAR = "#a0c3d2"
COLOR_BOTON_ELIMINAR = "#f8c8dc"
COLOR_BOTON_SALIR = "#f7a1a1"
COLOR_BOTON_SALIR_HOVER = "#f46b6b"

COLOR_TEXTO_COMPLETADO = "#9e9e9e"
COLOR_SELECCIONADO = "#c3f0ca"
COLOR_SELECCIONADO_COMPLETADO = "#a1d99b"

FUENTE_TITULO = ("Comic Sans MS", 16, "bold")
FUENTE_BOTONES = ("Comic Sans MS", 12, "bold")
FUENTE_LISTA = ("Helvetica", 13)
FUENTE_AUTOR = ("Comic Sans MS", 10, "italic")

# Selector de fecha y hora
class SelectorFechaHora(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Seleccionar Fecha y Hora")
        self.grab_set()
        self.config(bg=COLOR_FONDO)

        self.calendario = Calendar(self, selectmode='day', locale='es',
                                   date_pattern='yyyy-mm-dd', background=COLOR_BOTON,
                                   foreground='black', font=("Arial", 12))
        self.calendario.pack(padx=10, pady=10)

        frame_hora = tk.Frame(self, bg=COLOR_FONDO)
        frame_hora.pack(pady=5)

        tk.Label(frame_hora, text="Hora:", bg=COLOR_FONDO, font=FUENTE_BOTONES).pack(side=tk.LEFT)

        self.combo_hora = ttk.Combobox(frame_hora, width=3, values=[f"{h:02d}" for h in range(24)])
        self.combo_hora.current(0)
        self.combo_hora.pack(side=tk.LEFT, padx=2)

        tk.Label(frame_hora, text=":", bg=COLOR_FONDO, font=FUENTE_BOTONES).pack(side=tk.LEFT)

        self.combo_minuto = ttk.Combobox(frame_hora, width=3, values=[f"{m:02d}" for m in range(0, 60, 5)])
        self.combo_minuto.current(0)
        self.combo_minuto.pack(side=tk.LEFT, padx=2)

        frame_botones = tk.Frame(self, bg=COLOR_FONDO)
        frame_botones.pack(pady=10)

        btn_ok = tk.Button(frame_botones, text="OK", bg=COLOR_BOTON_COMPLETAR,
                           command=self.confirmar, width=10, font=FUENTE_BOTONES)
        btn_ok.pack(side=tk.LEFT, padx=10)

        btn_cancelar = tk.Button(frame_botones, text="Cancelar", bg=COLOR_BOTON_ELIMINAR,
                                 command=self.cancelar, width=10, font=FUENTE_BOTONES)
        btn_cancelar.pack(side=tk.LEFT, padx=10)

        self.resultado = None

    def confirmar(self):
        fecha = self.calendario.get_date()
        hora = self.combo_hora.get()
        minuto = self.combo_minuto.get()
        self.resultado = f"{fecha} {hora}:{minuto}"
        self.destroy()

    def cancelar(self):
        self.resultado = None
        self.destroy()

# Aplicación de tareas
class AppTareas:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación GUI para Gestión de Tareas - por Acosta Paoo")
        self.root.geometry("600x500")
        self.root.config(bg=COLOR_FONDO)

        self.tareas = []
        self.cargar_tareas()

        self.crear_widgets()
        self.asignar_atajos()

    def crear_widgets(self):
        self.label_titulo = tk.Label(self.root, text="Gestor de Tareas", font=FUENTE_TITULO, bg=COLOR_FONDO, fg="#4a6fa5")
        self.label_titulo.pack(pady=10)

        self.entry_tarea = tk.Entry(self.root, font=FUENTE_BOTONES)
        self.entry_tarea.pack(pady=10, padx=10, fill=tk.X)

        frame_botones = tk.Frame(self.root, bg=COLOR_FONDO)
        frame_botones.pack(pady=5)

        btn_agregar = tk.Button(frame_botones, text="Añadir Tarea", bg=COLOR_BOTON,
                                command=self.agregar_tarea, width=15, font=FUENTE_BOTONES)
        btn_agregar.pack(side=tk.LEFT, padx=5)

        btn_completar = tk.Button(frame_botones, text="Marcar Completada", bg=COLOR_BOTON_COMPLETAR,
                                  command=self.marcar_completada, width=15, font=FUENTE_BOTONES)
        btn_completar.pack(side=tk.LEFT, padx=5)

        btn_eliminar = tk.Button(frame_botones, text="Eliminar Tarea", bg=COLOR_BOTON_ELIMINAR,
                                 command=self.eliminar_tarea, width=15, font=FUENTE_BOTONES)
        btn_eliminar.pack(side=tk.LEFT, padx=5)

        btn_salir = tk.Button(frame_botones, text="Salir", bg=COLOR_BOTON_SALIR,
                              command=self.salir_app, width=10, font=FUENTE_BOTONES)
        btn_salir.pack(side=tk.LEFT, padx=5)
        btn_salir.bind("<Enter>", lambda e: btn_salir.config(bg=COLOR_BOTON_SALIR_HOVER))
        btn_salir.bind("<Leave>", lambda e: btn_salir.config(bg=COLOR_BOTON_SALIR))

        frame_lista = tk.Frame(self.root, bg=COLOR_FONDO)
        frame_lista.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(frame_lista)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lista_tareas = tk.Listbox(frame_lista, font=FUENTE_LISTA, selectmode=tk.SINGLE,
                                       yscrollcommand=self.scrollbar.set, activestyle='none')
        self.lista_tareas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.lista_tareas.yview)

        self.lista_tareas.bind("<<ListboxSelect>>", self.cambiar_color_seleccion)

        self.label_autor = tk.Label(self.root, text="Creado por Acosta Paoo", bg=COLOR_FONDO, font=FUENTE_AUTOR)
        self.label_autor.pack(pady=5)

        self.actualizar_lista()

    def asignar_atajos(self):
        # Atajos generales
        self.root.bind('<Return>', lambda event: self.agregar_tarea() if self.root.focus_get() == self.entry_tarea else None)
        self.root.bind('<Escape>', lambda event: self.salir_app())

        # Atajos que solo funcionan si el foco NO está en el Entry
        self.root.bind('<c>', self.atajo_marcar_completada)
        self.root.bind('<C>', self.atajo_marcar_completada)  # Mayúscula c
        self.root.bind('<e>', self.atajo_eliminar_tarea)
        self.root.bind('<E>', self.atajo_eliminar_tarea)     # Mayúscula e

    def atajo_marcar_completada(self, event):
        if self.root.focus_get() != self.entry_tarea:
            self.marcar_completada()

    def atajo_eliminar_tarea(self, event):
        if self.root.focus_get() != self.entry_tarea:
            self.eliminar_tarea()

    def agregar_tarea(self):
        descripcion = self.entry_tarea.get().strip()
        if descripcion == "":
            messagebox.showwarning("Campo vacío", "Por favor, escribe una tarea.")
            return

        if messagebox.askyesno("Agregar fecha y hora", "¿Deseas agregar una fecha y hora a esta tarea?"):
            selector = SelectorFechaHora(self.root)
            self.root.wait_window(selector)
            fecha_hora_str = selector.resultado
            if fecha_hora_str:
                try:
                    datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M")
                except:
                    messagebox.showerror("Error", "Fecha y hora inválidas.")
                    return
            else:
                fecha_hora_str = ""
        else:
            fecha_hora_str = ""

        tarea = {
            "descripcion": descripcion,
            "completada": False,
            "fecha_hora": fecha_hora_str
        }
        self.tareas.append(tarea)
        self.entry_tarea.delete(0, tk.END)
        self.actualizar_lista()
        self.guardar_tareas()

    def marcar_completada(self):
        seleccion = self.lista_tareas.curselection()
        if not seleccion:
            messagebox.showinfo("Selecciona una tarea", "Selecciona una tarea para marcar como completada.")
            return
        index = seleccion[0]
        self.tareas[index]["completada"] = not self.tareas[index]["completada"]
        self.actualizar_lista()
        self.guardar_tareas()

    def eliminar_tarea(self):
        seleccion = self.lista_tareas.curselection()
        if not seleccion:
            messagebox.showinfo("Selecciona una tarea", "Selecciona una tarea para eliminar.")
            return
        index = seleccion[0]
        if messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de eliminar esta tarea?"):
            self.tareas.pop(index)
            self.actualizar_lista()
            self.guardar_tareas()

    def actualizar_lista(self):
        self.lista_tareas.delete(0, tk.END)
        for tarea in self.tareas:
            texto = tarea["descripcion"]
            if tarea["fecha_hora"]:
                texto += f" ({tarea['fecha_hora']})"
            if tarea["completada"]:
                texto += " ✔"
            self.lista_tareas.insert(tk.END, texto)
        self.cambiar_color_seleccion()

    def cambiar_color_seleccion(self, event=None):
        for i in range(len(self.tareas)):
            if self.tareas[i]["completada"]:
                self.lista_tareas.itemconfig(i, fg=COLOR_TEXTO_COMPLETADO, bg=COLOR_FONDO)
            else:
                self.lista_tareas.itemconfig(i, fg="black", bg=COLOR_FONDO)

        seleccion = self.lista_tareas.curselection()
        if seleccion:
            i = seleccion[0]
            tarea = self.tareas[i]
            if tarea["completada"]:
                self.lista_tareas.itemconfig(i, bg=COLOR_SELECCIONADO_COMPLETADO, fg="black")
            else:
                self.lista_tareas.itemconfig(i, bg=COLOR_SELECCIONADO, fg="black")

    def guardar_tareas(self):
        with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
            json.dump(self.tareas, f, ensure_ascii=False, indent=4)

    def cargar_tareas(self):
        if os.path.exists(ARCHIVO_JSON):
            with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
                self.tareas = json.load(f)
        else:
            self.tareas = []

    def salir_app(self):
        messagebox.showinfo("¡Hasta luego!", "Gracias por utilizar la app 😊\n¡Vuelve pronto!")
        self.root.quit()

# Ejecutar la app
if __name__ == "__main__":
    root = tk.Tk()
    app = AppTareas(root)
    root.mainloop()





