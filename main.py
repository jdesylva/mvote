#!/usr/bin/python3
#
import sys,time,socket,json,socket
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

class voteur(tk.Frame):

    valeurChoisie = 0

    def __init__(self, root, index):

        self.root = root

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

        self.lblTexte = tk.Label(self, anchor="center", bg="grey", fg="yellow")
        self.lblTexte.place(relx=0.5, rely=0.5)
        self.lblTexte.configure(text=str(index))
        self.lblTexte.configure(justify='center')
        self.lblTexte.configure(font=("Courrier New", 10, "bold"))
        #self.lbl.bind("<Button-1>", self.buttonPort)

    def setVote(self, valeur):
        self.valeurChoisie = valeur 
        
    def getVote(self, valeur):
        return self.valeurChoisie 
        

class dlgVoteur:
    
    def __init__(self, parent):
        self.parent = parent
        self.top = tk.Toplevel(parent)
        self.top.title("Configuration")
        self.top.geometry("800x400")
        self.top.resizable(True, True)

        self.myCheckEmail = tk.IntVar(self.top)
        self.myCheckEmail.set(False)
        self.mEmail_check = tk.Checkbutton(self.top, text = "Actif", variable = self.myCheckEmail, onvalue = 1, offvalue = 0, height=3, width = 5)
        self.mEmail_check.place(relx=0.80, rely=0.32, anchor=tk.W)

    def show(self):
        self.top.wm_deiconify()
        self.top.wait_window()
        return self.myCheckEmail.get()
    

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
        self.backlog = self.parametres['backlog']
        
        self.nbVoteurs = self.parametres['nb_voteurs']
        self.nbColonnes = self.parametres['nb_colonnes']
        self.nbRangees = self.parametres['nb_rangees']
        

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
        self.Header.bind("<Button-1>", self.buttonLogoClick)

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

        self.initialiseVoteurs(self.nbVoteurs, self.nbColonnes, self.nbRangees)

        self.initialiseOutils()


        

    def initialiseOutils(self):

        self.panneauLateral = tk.Frame(self.root, bg='grey', borderwidth=2)
        self.panneauLateral.place(relx=0.65, rely=0.30, relheight=0.58, relwidth=0.30)   
        
        self.lblTitre = tk.Label(self.panneauLateral, anchor="w")
        self.lblTitre.place(relx=0.43, rely=0.02, relheight=0.05, relwidth=0.15)
        self.lblTitre.configure(text="Outils", bg="grey", fg="white")
        self.lblTitre.configure(justify='center')
        self.lblTitre.configure(font=("Courrier New", 10, "bold"))
        
        self.lblNombreChoix = tk.Label(self.panneauLateral, anchor="w")
        self.lblNombreChoix.place(relx=0.05, rely=0.22, relheight=0.05, relwidth=0.45)
        self.lblNombreChoix.configure(text="Nombre de choix : ", bg="grey", fg="white")
        self.lblNombreChoix.configure(justify='center')
        self.lblNombreChoix.configure(font=("Courrier New", 10, "bold"))

        self.nbChoixVar = tk.StringVar()
        self.nbChoixVar.set("2")
        
        self.entryNbChoix = tk.Entry(self.panneauLateral, textvariable=self.nbChoixVar)
        self.entryNbChoix.place(relx=0.50, rely=0.22, width=50)

        self.lblDureeVote = tk.Label(self.panneauLateral, anchor="w")
        self.lblDureeVote.place(relx=0.05, rely=0.32, relheight=0.05, relwidth=0.45)
        self.lblDureeVote.configure(text="Durée du vote (s): ", bg="grey", fg="white")
        self.lblDureeVote.configure(justify='center')
        self.lblDureeVote.configure(font=("Courrier New", 10, "bold"))

        self.dureeVoteVar = tk.StringVar()
        self.dureeVoteVar.set("0")
        
        self.entryDureeVote = tk.Entry(self.panneauLateral, textvariable=self.dureeVoteVar)
        self.entryDureeVote.place(relx=0.50, rely=0.32, width=50)

        self.btnDemarrer = tk.Button(self.panneauLateral, text="Démarrer", command = self.controlerVote)
        self.btnDemarrer.place(relx=0.75, rely=0.22, relheight=0.05, relwidth=0.2)
        self.btnDemarrer.configure(bg="green", fg="yellow", activebackground="green")
        
        self.entete_voteurs = ["Choix", "Résultat"]

        style = ttk.Style(self.panneauLateral)
        style.theme_use("clam")
        style.configure("Treeview", background="grey", 
                fieldbackground="grey", foreground="white")

        self.tree = ttk.Treeview(self.panneauLateral, columns=self.entete_voteurs, show="tree headings", height=10)
        self.tree.column("# 0", anchor=tk.W, width=10)
        self.tree.heading("# 0", text="")
        self.tree.column("# 1", anchor=tk.W, width=30)
        self.tree.heading("# 1", text="Choix")
        self.tree.column("# 2", anchor=tk.W, width=30)
        self.tree.heading("# 2", text="Résultat")

        vsb = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.tree, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        self.tree.place(relx=0.05, rely=0.4, relheight=0.55, relwidth=0.9)
        self.tree['show'] = 'tree headings'

        self.myCheckAlias = tk.IntVar(self.panneauLateral)
        self.myCheckAlias.set(False)
        self.mAlias_check = tk.Checkbutton(self.panneauLateral, text = "Afficher Alias", variable = self.myCheckAlias, onvalue = "1", offvalue = "0", height=1, width = 12, bg="grey", fg = "white", command=self.aliasActive)
        self.mAlias_check.place(relx=0.05, rely=0.15, anchor=tk.W)
        
    def aliasActive(self):
        if self.myCheckAlias.get() == 1:
            print("Checkbox == 1")
        elif self.myCheckAlias.get() == 0:
            print("Checkbox == 0")

    def controlerVote(self):
        if self.btnDemarrer['text'] == 'Démarrer' :
            self.btnDemarrer.configure(text="Arrêter", bg="red", fg="yellow", activebackground="red")
            print("Le vote est en cours.")
            self.effacerResultatVote()
            self.demarrerServeur()
            self.demarrerHorloge()
        else :
            self.btnDemarrer.configure(text="Démarrer", bg="green", fg="yellow", activebackground="green")
            print("Le vote est terminé.")
            self.arreterServeur()
            self.arreterHorloge()

    def effacerResultatVote(self):

        print("Le résultat du vote précédent a été effacé.")


    def demarrerServeur(self):

        # Créer le socket serveur
        self.serveur =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.serveur.bind((self.adresseIP, self.port))
        self.serveur.listen(self.backlog)
        
        print("Le serveur est en opération.")

    def demarrerHorloge(self):

        print("Le compteur du temps de vote est en cours")

    def arreterServeur(self):

        self.serveur.close()
        print("Le serveur est arrêté.")

    def arreterHorloge(self):

        print("Le compteur du temps est arrêté.")

    def initialiseVoteurs(self, nombre, nb_colonnes, nb_lignes):
        
        rng = range(nombre)
        for i in rng:
            self.vot = voteur(self.root, i+1)
            self.vot.place(relx=0.05 + (i % nb_colonnes) * (0.6 / nb_colonnes),
                        rely=0.30 + (i // nb_colonnes) * (0.6 / nb_lignes),
                        relheight=0.5/nb_lignes,
                        relwidth=0.5/nb_colonnes)
            self.vot.bind("<Button-3>", self.confDlg)

            self.voteurs.append(self.vot)

    def confDlg(self, event):

        print(str(event))
        chck = dlgVoteur(self.root).show()
        print(f"chck[0] == {chck}")
        
    def buttonLogoClick(self, event):

        self.on_closing()
        
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
    
