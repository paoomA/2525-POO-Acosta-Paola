import tkinter as tk
from tkinter import messagebox

# ------------------- Funciones -------------------
def agregar_dato():
    dato = entrada_texto.get().strip()
    if not dato:
        messagebox.showwarning("Campo vacío", "Por favor ingresa un número.")
        return

    try:
        # Convertimos a float para validar, pero mostramos como texto limpio
        valor = float(dato)
        # Si es entero, muestra sin punto decimal
        if valor.is_integer():
            lista_datos.insert(tk.END, str(int(valor)))
        else:
            lista_datos.insert(tk.END, str(valor))
        entrada_texto.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error de entrada", "Por favor ingresa un número válido.")

def limpiar_seleccion_o_todo():
    entrada_texto.delete(0, tk.END)

    seleccion = lista_datos.curselection()
    if seleccion:
        for i in reversed(seleccion):
            lista_datos.delete(i)
    else:
        lista_datos.delete(0, tk.END)

# ------------------- Ventana Principal -------------------
ventana = tk.Tk()
ventana.title("Gestor Numérico")
ventana.geometry("420x400")
ventana.configure(bg="#f0f4f8")
ventana.resizable(False, False)

# ------------------- Estilos -------------------
fuente_titulo = ("Arial", 16, "bold")
fuente_normal = ("Arial", 12)

# ------------------- Widgets -------------------
titulo = tk.Label(ventana, text="Gestor de Datos Numéricos", font=fuente_titulo, bg="#f0f4f8", fg="#333")
titulo.pack(pady=15)

frame_input = tk.Frame(ventana, bg="#f0f4f8")
frame_input.pack(pady=10)

etiqueta = tk.Label(frame_input, text="Dato numérico:", font=fuente_normal, bg="#f0f4f8")
etiqueta.grid(row=0, column=0, padx=5, pady=5)

entrada_texto = tk.Entry(frame_input, width=20, font=fuente_normal)
entrada_texto.grid(row=0, column=1, padx=5)

frame_botones = tk.Frame(ventana, bg="#f0f4f8")
frame_botones.pack(pady=10)

boton_agregar = tk.Button(frame_botones, text="Agregar", font=fuente_normal, bg="#4caf50", fg="white", width=10, command=agregar_dato)
boton_agregar.grid(row=0, column=0, padx=10)

boton_limpiar = tk.Button(frame_botones, text="Limpiar", font=fuente_normal, bg="#f44336", fg="white", width=10, command=limpiar_seleccion_o_todo)
boton_limpiar.grid(row=0, column=1, padx=10)

etiqueta_lista = tk.Label(ventana, text="Datos ingresados:", font=fuente_normal, bg="#f0f4f8", fg="#555")
etiqueta_lista.pack(pady=10)

lista_datos = tk.Listbox(ventana, width=30, height=10, font=fuente_normal, bg="white", fg="#333", selectmode=tk.MULTIPLE)
lista_datos.pack(pady=5)

# ------------------- Ejecutar App -------------------
ventana.mainloop()


