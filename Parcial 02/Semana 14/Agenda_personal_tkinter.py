import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Personal")
        self.root.geometry("750x450")
        self.root.configure(bg="#f0f4f8")  # Color de fondo general

        # ----------- Estilo Personalizado -----------
        style = ttk.Style()
        style.theme_use("clam")  # Se puede cambiar por: 'alt', 'default', 'classic', etc.

        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#333333",
                        rowheight=25,
                        fieldbackground="#f9f9f9",
                        font=('Segoe UI', 10))

        style.configure("Treeview.Heading",
                        background="#007acc",
                        foreground="white",
                        font=('Segoe UI', 11, 'bold'))

        style.configure("TButton",
                        font=("Segoe UI", 10),
                        padding=6)

        style.configure("TLabel",
                        font=("Segoe UI", 10),
                        background="#f0f4f8")

        # ----------- Frame: Lista de eventos -----------
        self.frame_tree = ttk.Frame(self.root)
        self.frame_tree.pack(pady=10)

        self.tree = ttk.Treeview(self.frame_tree, columns=("Fecha", "Hora", "Descripción"), show="headings")
        self.tree.heading("Fecha", text="📅 Fecha")
        self.tree.heading("Hora", text="⏰ Hora")
        self.tree.heading("Descripción", text="📝 Descripción")
        self.tree.column("Fecha", width=100, anchor="center")
        self.tree.column("Hora", width=100, anchor="center")
        self.tree.column("Descripción", width=460, anchor="w")
        self.tree.pack()

        # ----------- Frame: Entradas -----------
        self.frame_inputs = ttk.Frame(self.root)
        self.frame_inputs.pack(pady=10)

        # Fecha
        ttk.Label(self.frame_inputs, text="Fecha (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_fecha = ttk.Entry(self.frame_inputs, width=15)
        self.entry_fecha.grid(row=0, column=1, padx=5, pady=5)

        # Hora
        ttk.Label(self.frame_inputs, text="Hora (HH:MM):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_hora = ttk.Entry(self.frame_inputs, width=15)
        self.entry_hora.grid(row=0, column=3, padx=5, pady=5)

        # Descripción
        ttk.Label(self.frame_inputs, text="Descripción:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_descripcion = ttk.Entry(self.frame_inputs, width=60)
        self.entry_descripcion.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        # ----------- Frame: Botones -----------
        self.frame_buttons = ttk.Frame(self.root)
        self.frame_buttons.pack(pady=10)

        self.btn_agregar = ttk.Button(self.frame_buttons, text="✅ Agregar Evento", command=self.agregar_evento)
        self.btn_agregar.grid(row=0, column=0, padx=10)

        self.btn_eliminar = ttk.Button(self.frame_buttons, text="🗑️ Eliminar Seleccionado", command=self.eliminar_evento)
        self.btn_eliminar.grid(row=0, column=1, padx=10)

        self.btn_salir = ttk.Button(self.frame_buttons, text="🚪 Salir", command=self.root.quit)
        self.btn_salir.grid(row=0, column=2, padx=10)

    def agregar_evento(self):
        fecha = self.entry_fecha.get().strip()
        hora = self.entry_hora.get().strip()
        descripcion = self.entry_descripcion.get().strip()

        if not fecha or not hora or not descripcion:
            messagebox.showwarning("Campos Vacíos", "Por favor, completa todos los campos.")
            return

        # Validar formato de fecha
        try:
            datetime.datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Formato Incorrecto", "La fecha debe estar en formato YYYY-MM-DD.")
            return

        # Validar formato de hora
        try:
            datetime.datetime.strptime(hora, "%H:%M")
        except ValueError:
            messagebox.showerror("Formato Incorrecto", "La hora debe estar en formato HH:MM (24h).")
            return

        self.tree.insert("", "end", values=(fecha, hora, descripcion))

        # Limpiar campos
        self.entry_fecha.delete(0, tk.END)
        self.entry_hora.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)

    def eliminar_evento(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Sin selección", "Selecciona un evento para eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Eliminar el evento seleccionado?")
        if confirmar:
            self.tree.delete(seleccion)

# ----------- Ejecutar la app -----------
if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()

