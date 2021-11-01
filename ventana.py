import tkinter as tk
from tkinter import Frame, Button, Label, StringVar, Canvas, CENTER, filedialog
from PIL import ImageTk, Image
import zipfile
import rarfile
from tqdm import tqdm
import threading
from tkinter.messagebox import showinfo
from tkinter import ttk

class Ventana():

    def __init__(self):

        self.root = tk.Tk()

        # Colocamos la imagen del zip que aparece al inicio
        canvas = Canvas(self.root, width = 400, height = 225)
        canvas.pack()
        img = ImageTk.PhotoImage(Image.open("./images/zip_icon.png"))
        canvas.create_image(200, 112, anchor=CENTER, image=img)

        self.configurar_root()

        self.configurar_panel_principal()

        self.configurar_panel_notificacion()

        self.root.mainloop()


    def configurar_root(self):
        self.root.geometry('400x450')
        self.root.title('Descompresor')

        # Colocamos el icono de la aplicacion
        ico = Image.open('./images/icon.png')
        photo = ImageTk.PhotoImage(ico)
        self.root.wm_iconphoto(False, photo)

        lbl_nombre = Label(self.root, text="Descompresor RAR y ZIP", font=('Arial', 25))
        lbl_nombre.pack()


    def configurar_panel_principal(self):
        self.panel_principal = Frame(self.root)
        self.panel_principal.pack()

        self.btn_analizar_archivo = Button(self.panel_principal, text="Analizar Archivo", command=self.scan_file)
        self.btn_analizar_archivo.grid(column=0, row=0, padx=10, pady=20)

    def configurar_panel_notificacion(self):
        self.panel_notificacion = Frame(self.root)
        self.panel_notificacion.pack()

        self.progressbar = ttk.Progressbar(self.panel_notificacion, length=350)
        self.progressbar.pack(fill='x', expand=True)


    def scan_file(self):
        # La funcion se ejecuta desde otro hilo para no colgar la interfaz grafica
        hilo = threading.Thread(target=self.scan_file_compress)
        hilo.start()

    # Funcion que llamara el boton de escanear archivos
    def scan_file_compress(self):
        # the password list path you want to use, must be available in the current directory
        wordlist = "password.txt"
        # the zip file you want to crack its password
        filename = filedialog.askopenfilename()

        showinfo(title='Información', message='El desbloqueo comenzara en breve. Revise la consola para ver el progreso')

        if filename.endswith('.zip'):
            fp = zipfile.ZipFile(filename)
        elif filename.endswith('.rar'):
            fp = rarfile.RarFile(filename)
        else:
            showinfo(title='Información', message='El archivo debe ser .rar o .zip')

        # count the number of words in this wordlist
        n_words = len(list(open(wordlist, "rb")))

        with open(wordlist, "rb") as wordlist:
            for word in tqdm(wordlist, total=n_words, unit="word"):
                try:
                    fp.extractall(pwd=word.strip())
                except:
                    continue
                else:
                    showinfo(title='Información', message=f'[+] Password found: {word.decode().strip()}')
                    exit(0)
        showinfo(title='Información', message='Contraseña no encontrada')
