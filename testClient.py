#!/usr/bin/python3
import tkinter
from tkinter import ttk
import tkinter.messagebox
import socket, time
import pdb

entryAdresseHote = None
entryPortHote = None
entryCommande = None

def envoyerDonnees(hote, port, donnees) :
        
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((hote,int(port)))
        client.send(str.encode(donnees.strip()))
        client.close()
    except Exception as e :
        tkinter.messagebox.showerror("Erreur", f"L'erreur suivante s'est produite : {e}")


    
def envoi():

    tampon = txtCommande.get()
    tamponSplit = tampon.split(' ')

    if tampon[0:4] == "exe " :
        with open(tamponSplit[1], 'r', newline='') as f_commandes:
            ligne = f_commandes.readline()
            while ligne:
                print(f"ligne == {ligne}")
                if ligne[0] == "#":
                    pass
                elif ligne[0:3] == "del" :
                    ligneSplit = ligne.split(" ")
                    time.sleep(float(ligneSplit[1].strip()))
                else:
                    envoyerDonnees(txtAdresse.get(), txtPort.get(), ligne)
                ligne = f_commandes.readline()
    else:
        
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = socket.gethostbyname(txtAdresse.get())
            port = txtPort.get()
            client.connect((host,int(port)))
            #data = server.recv(1024)
            #print(bytes.decode(data))

            client.send(str.encode(txtCommande.get()))
            #data = server.recv(1024)
            #print("Received from server: ", bytes.decode(data))
            client.close()
        except Exception as e :
            tkinter.messagebox.showerror("Erreur", f"L'erreur suivante s'est produite : {e}")


root = tkinter.Tk()
root.title("Client pour la machine à voter")

frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Commande :").grid(column=0, row=0)
txtCommande = tkinter.StringVar()
print(entryCommande)
entryCommande = ttk.Entry(frm, textvariable=txtCommande)
entryCommande.grid(column=1, row=0)
entryCommande.focus()
ttk.Label(frm, text="Adresse :").grid(column=0, row=1)
txtAdresse = tkinter.StringVar()
ttk.Entry(frm, textvariable=txtAdresse).grid(column=1, row=1)
ttk.Label(frm, text="Port :").grid(column=0, row=2)
txtPort = tkinter.StringVar()
ttk.Entry(frm, textvariable=txtPort).grid(column=1, row=2)
ttk.Button(frm, text="Envoyer", command=envoi).grid(column=1, row=5)
ttk.Button(frm, text="Terminer", command=root.destroy).grid(column=3, row=5)
root.mainloop()

