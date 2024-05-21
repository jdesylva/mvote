#!/usr/bin/python
#
import sys,time,socket,json
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

class voteur(tk.Frame):

    def __init__(self, root, index):

        self.root = root

        # field options
        options = {'padx': 5, 'pady': 5}
        
        # get the screen dimension
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        window_width = screen_width / 4
        window_height = screen_height / 4

        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        # set the position of the window to the center of the screen
        self.width = window_width
        self.height = window_height
        
        super().__init__(root, bg='grey')
        #super().__init__(root, width = window_width, height = window_height, bg='blue')

        #self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


        self.lblTexte = tk.Label(self, anchor="center", bg="grey", fg="yellow")
        #self.lblTexte.place(relx=0.5, rely=0.5, relheight=0.2, relwidth=0.3)
        self.lblTexte.place(relx=0.5, rely=0.5)
        self.lblTexte.configure(text=str(index))
        self.lblTexte.configure(justify='center')
        self.lblTexte.configure(font=("Courrier New", 10, "bold"))
        #self.lbl.bind("<Button-1>", self.buttonPort)
        

class appVote:

    lafin = False
    photo = None
    almRouge = None
    almVert = None
    adresseIP = None
    port = None
    root = None
    voteurs = []

    def __init__(self, geo="1000x700+225+150", confFile="config.json"):

        with open(confFile, 'r') as file:
            self.parametres = json.load(file)

        self.adresseIP = self.parametres['adresse_serveur']
        self.port = self.parametres['port_tcp_serveur']

        self.email_sender = self.parametres['email_sender']

        self.root = tk.Tk()
        self.root.geometry(geo)
        #self.root.resizable(False, False)
        #self.root.attributes('-fullscreen',True)
        self.root.minsize(1000, 700)
        self.root.title("Cégep Joliette Télécom@" + str(socket.gethostname()))
        self.root.wm_attributes('-alpha', 0.75)

        try :

            self.almRouge = tk.PhotoImage(file="almRouge.png")
            self.almVerte = tk.PhotoImage(file="almVerte.png")
            self.photo = tk.PhotoImage(file="logodemo_t.png")

            # Load the custom icon image
            icon_image = tk.PhotoImage(file="iconeDemo.png")

            # Set the custom icon for the window titlebar
            self.root.iconphoto(False, icon_image)

        except Exception as excpt:
            
            print("Fichiers des images manquants!")
            print("Erreur : ", excpt)
            sys.exit()
            
        # Get the current screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # get the width and height of the image
        image_width = self.photo.width()
        image_height = self.photo.height()
        print(f"image_width == {image_width}")
        print(f"image_height == {image_height}")

        self.Header = tk.Label(self.root, image=self.photo, width=image_width, height=image_height)
        self.Header.place(relx=0.5, rely=0.03, anchor=tk.N)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            self.adresseIP = s.getsockname()[0]
        except:
            self.adresseIP='127.0.0.1'
        finally:
            s.close()
        self.lblAdresseIP = tk.Label(self.root, anchor="w")                     # Bas de page
        self.lblAdresseIP.place(relx=0.05, rely=0.95, height=23, width=225)
        self.lblAdresseIP.configure(text="Serveur " + self.adresseIP)
        self.lblAdresseIP.configure(justify='left')
        self.lblAdresseIP.configure(font=("Courrier New", 10, "bold"))
        #self.lblAdresseIP.bind("<Button-1>", self.buttonAdresse)

        self.lblPortTCP = tk.Label(self.root, anchor="w")                       # Bas de page
        self.lblPortTCP.place(relx=0.25, rely=0.95, height=23, width=100)
        self.lblPortTCP.configure(text="Port " + ":" + str(self.port))
        self.lblPortTCP.configure(justify='left')
        self.lblPortTCP.configure(font=("Courrier New", 10, "bold"))
        #self.lblPortTCP.bind("<Button-1>", self.buttonPort)

        self.initialiseVoteurs(35, 5, 7)
        #self.vott1 = voteur(self.root)
        #self.vott1.place(relx=0, rely=0.25, height=100, width=100)

    def initialiseVoteurs(self, nombre, nb_colonne, nb_ligne):
        
        rng = range(nombre)
        for i in rng:
            vot = voteur(self.root, i)
            vot.place(relx=0.05 + (i % nb_colonne) * (0.9 / nb_colonne),
                        rely=0.30 + (i // nb_colonne) * (0.6 / nb_ligne),
                        relheight=0.5/nb_ligne,
                        relwidth=0.6/nb_colonne)
            self.voteurs.append(vot)
            #print(f"relx =  {0.02 + (i % nb_colonne) * (0.96 / nb_colonne)}")
            #print(f"rely =  {0.30 + (i // nb_ligne) * (0.60 / nb_ligne)}")
    def run(self):

        while not self.lafin:
    
            self.root.update_idletasks()
            self.root.update()
            time.sleep(0.01)
            
        self.root.quit()

    def on_closing(self):

        if tk.messagebox.askokcancel("Terminé ?", "Est-ce que vous voulez fermer le programme ?"):

            self.lafin = True
            time.sleep(1)
            
application = appVote("1190x750+225+150")
application.run()
    
