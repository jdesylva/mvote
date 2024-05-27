#!/usr/bin/python3
import tkinter
from tkinter import ttk
import socket

entryAdresseHote = None
entryPortHote = None
entryCommande = None

def envoi():

    global entryAdresseHote
    
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

