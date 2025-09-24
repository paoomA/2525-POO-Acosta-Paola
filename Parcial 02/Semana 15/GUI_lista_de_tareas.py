import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import json
import os


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📋 Mi Lista de Tareas - Paola Acosta")
        self.task_states = {}

        self.root.geometry("900x600")
        self.root.config(bg="#FFF9F2")

        # Fuentes
        self.font_title = ("Comic Sans MS", 26, "bold")
        self.font_subtitle = ("Comic Sans MS", 14, "italic")
        self.font_buttons = ("Comic Sans MS", 14, "bold")
        self.font_list = ("Comic Sans MS", 13)

        # Colores
        self.color_button_add = "#FF8C94"
        self.color_button_complete = "#A8DCD1"
        self.color_button_delete = "#FFAAA6"
        self.color_button_exit = "#FF6F91"
        self.task_bg_color = "#FFFFFF"
        self.task_completed_color = "#D6EADF"

        # Título
        tk.Label(root, text="📋 Mi Lista de Tareas", font=self.font_title, bg="#FFF9F2", fg="#FF6F91").pack(pady=(20, 0))
        tk.Label(root, text="Paola Acosta", font=self.font_subtitle, bg="#FFF9F2", fg="#FF6F91").pack(pady=(0, 20))

        # Entrada de tareas
        entry_frame = tk.Frame(root, bg="#FAE3D9", bd=2, relief="ridge")
        entry_frame.pack(pady=10, padx=20, fill="x")

        self.task_entry = tk.Entry(entry_frame, font=self.font_buttons, bg="#FFFFFF", fg="#333333")
        self.task_entry.pack(side=tk.LEFT, padx=5, pady=10, fill="x", expand=True)

        self.date_entry = DateEntry(entry_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.pack(side=tk.LEFT, padx=5)

        self.time_entry = tk.Entry(entry_frame, width=8, font=self.font_buttons)
        self.time_entry.insert(0, "HH:MM")
        self.time_entry.pack(side=tk.LEFT, padx=5)

        add_button = tk.Button(entry_frame, text="Añadir Tarea ➕", font=self.font_buttons,
                               bg=self.color_button_add, fg="white", bd=0, command=self.add_task)
        add_button.pack(side=tk.LEFT, padx=5)

        # Lista
        list_frame = tk.Frame(root, bg="#FFF9F2")
        list_frame.pack(padx=20, pady=15, fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox = tk.Listbox(list_frame, font=self.font_list, bg=self.task_bg_color,
                                       fg="#333333", selectbackground=self.color_button_add,
                                       selectforeground="white", yscrollcommand=self.scrollbar.set)
        self.task_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        self.scrollbar.config(command=self.task_listbox.yview)

        # Botones
        button_frame = tk.Frame(root, bg="#FFF9F2")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="✅ Marcar completada", font=self.font_buttons, bg=self.color_button_complete,
                  fg="white", bd=0, command=self.mark_completed).grid(row=0, column=0, padx=10)

        tk.Button(button_frame, text="🗑️ Eliminar tarea", font=self.font_buttons, bg=self.color_button_delete,
                  fg="white", bd=0, command=self.delete_task).grid(row=0, column=1, padx=10)

        tk.Button(button_frame, text="🚪 Salir", font=self.font_buttons, bg=self.color_button_exit,
                  fg="white", bd=0, command=self.root.destroy).grid(row=0, column=2, padx=10)

        self.load_tasks()

    def add_task(self):
        task_text = self.task_entry.get().strip()
        date = self.date_entry.get()
        time = self.time_entry.get().strip()

        if not task_text:
            messagebox.showwarning("Atención", "Por favor, ingresa una tarea.")
            return

        full_task = f"{task_text} - {date} {time}"

        if full_task in self.task_states:
            messagebox.showinfo("Ya existe", "Esa tarea ya está en la lista.")
            return

        self.task_listbox.insert(tk.END, full_task)
        self.task_states[full_task] = False
        self.save_tasks()
        self.task_entry.delete(0, tk.END)

    def mark_completed(self):
        try:
            index = self.task_listbox.curselection()[0]
            task = self.task_listbox.get(index)
            self.task_states[task] = True
            self.task_listbox.itemconfig(index, fg="#B6B7BA", bg=self.task_completed_color)
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Atención", "Selecciona una tarea para marcarla como completada.")

    def delete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            task = self.task_listbox.get(index)
            confirm = messagebox.askyesno("Eliminar", f"¿Eliminar la tarea?\n\n{task}")
            if confirm:
                self.task_listbox.delete(index)
                if task in self.task_states:
                    del self.task_states[task]
                self.save_tasks()
        except IndexError:
            messagebox.showwarning("Atención", "Selecciona una tarea para eliminarla.")

    def save_tasks(self):
        with open("tareas.json", "w", encoding="utf-8") as f:
            json.dump(self.task_states, f, ensure_ascii=False, indent=4)

    def load_tasks(self):
        if os.path.exists("tareas.json"):
            with open("tareas.json", "r", encoding="utf-8") as f:
                self.task_states = json.load(f)
            for task, completed in self.task_states.items():
                self.task_listbox.insert(tk.END, task)
                index = self.task_listbox.size() - 1
                if completed:
                    self.task_listbox.itemconfig(index, fg="#B6B7BA", bg=self.task_completed_color)


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()


