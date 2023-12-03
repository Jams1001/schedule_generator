import tkinter as tk
from tkinter import filedialog
import subprocess
import threading


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de horarios")

        try:
            self.root.state('zoomed')
        except tk.TclError:
            self.root.geometry("800x600")

        self.csv_path = tk.StringVar(value="Archivo no cargado")
        self.csv_path_label = tk.Label(root, textvariable=self.csv_path)
        self.csv_path_label.pack(pady=10)
        self.load_button = tk.Button(
            root,
            text="Cargar csv de disponibilidad",
            command=self.load_csv)
        self.load_button.pack(pady=10)

        self.service_csv_path = tk.StringVar(
            value="Archivo de cursos de servicio no cargado")
        self.service_csv_path_label = tk.Label(
            root,
            textvariable=self.service_csv_path)
        self.service_csv_path_label.pack(pady=10)
        self.load_service_button = tk.Button(
            root,
            text="Cargar csv de cursos de servicio",
            command=self.load_service_csv)
        self.load_service_button.pack(pady=10)

        self.copies_name_label = tk.Label(
            root,
            text="Nombre de las soluciones a generar:")
        self.copies_name_label.pack(pady=10)
        self.output_name = tk.StringVar(value="outputname")
        self.output_name_entry = tk.Entry(root, textvariable=self.output_name)
        self.output_name_entry.pack(pady=10)

        self.copies_number_label = tk.Label(
            root,
            text="Número de soluciones a generar:")
        self.copies_number_label.pack(pady=10)
        self.copies_number = tk.IntVar(value=3)
        self.copies_number_entry = tk.Spinbox(
            root,
            from_=1,
            to=100,
            textvariable=self.copies_number)
        self.copies_number_entry.pack(pady=10)

        self.execute_button = tk.Button(
            root, text="Ejecutar",
            command=self.execute,
            state=tk.DISABLED)
        self.execute_button.pack(pady=10)

        self.status = tk.StringVar(value="Esperando archivo...")
        self.status_label = tk.Label(root, textvariable=self.status)
        self.status_label.pack(pady=10)

        self.running = False
        self.file_loaded = False
        self.service_file_loaded = False

    def load_csv(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.csv_path.set(file_path)
            self.file_loaded = True
            self.check_files_loaded()

    def load_service_csv(self):
        service_file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")])
        if service_file_path:
            self.service_csv_path.set(service_file_path)
            self.service_file_loaded = True
            self.check_files_loaded()

    def check_files_loaded(self):
        if self.file_loaded and self.service_file_loaded:
            self.status.set("Listo para generar, archivos cargados!")
            self.execute_button.config(state=tk.NORMAL)
        elif self.file_loaded:
            self.status.set("Listo para generar, archivo de horarios cargado!")
        elif self.service_file_loaded:
            self.status.set(
                "Listo para generar, archivo de cursos de servicio cargado!")
        else:
            self.status.set("Esperando archivos...")

    def animate_status(self):
        if not self.running:
            return

        dots = self.status.get().count('.')
        if dots < 3:
            self.status.set("Trabajando" + "."*(dots+1))
        else:
            self.status.set("Trabajando.")
        self.root.after(500, self.animate_status)

    def execute(self):
        if not self.file_loaded or not self.service_file_loaded:
            self.status.set("Por favor, carga los archivos CSV primero.")
            return

        output_directory = filedialog.askdirectory()
        if output_directory:
            self.execute_button.config(state=tk.DISABLED)
            self.load_button.config(state=tk.DISABLED)
            self.load_service_button.config(state=tk.DISABLED)

            self.running = True
            self.animate_status()

            num_copies = self.copies_number.get()
            thread = threading.Thread(target=self.copy_files, args=(
                output_directory,
                num_copies))
            thread.start()
            self.root.after(100, self.check_thread, thread)

    def check_thread(self, thread):
        if thread.is_alive():
            self.root.after(100, self.check_thread, thread)
        else:
            self.running = False
            self.status.set("¡Listo!")
            self.load_button.config(state=tk.NORMAL)
            self.load_service_button.config(state=tk.NORMAL)
            if self.file_loaded and self.service_file_loaded:
                self.execute_button.config(state=tk.NORMAL)

    def copy_files(self, output_directory, num_copies):
        file_path = self.csv_path.get()
        service_file_path = self.service_csv_path.get()
        output_name = self.output_name.get()
        subprocess.run([
            "python3",
            "fun.py",
            file_path,
            service_file_path,
            str(num_copies),
            output_name])


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
