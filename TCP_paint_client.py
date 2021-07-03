#! /usr/bin/env python3
# *******************************************************
# Nom ......... : TCP_paint_client.py
# Rôle ........ : Client d'un logiciel de dessin avec redistribution réseau
# Auteur ...... : Nicolas Tercé
# Version ..... : V0.1 du 29/06/2020
# Licence ..... : réalisé dans le cadre du cours de IED Paris8
# 
# Compilation : pas de compilation nécessaire
# Usage : Pour exécuter : ./TCP_paint_client.py
#********************************************************/
#import os
#import socket
import tkinter as tk
import os
from tkinter import *
import random as rd
from PIL import Image,ImageDraw,ImageTk
import io
from tkinter.colorchooser import askcolor
#module facielement installable avec un pip install pyscreenshot
import pyscreenshot as ImageGrab

import datetime
from tkinter import scrolledtext

#! /usr/bin/env python3

#envoi fichier
#https://codes-sources.commentcamarche.net/source/53419-transfert-de-fichier-par-socket
#https://stackoverflow.com/questions/30128079/how-to-send-end-of-file-without-closing-tcp-socket

# Héritage multiple
# https://deusyss.developpez.com/tutoriels/Python/heritage_metaclasse/
import socket, sys, time,os,threading


def connection_game(port,chiffre_status, nom_joueur):
    # Creation de la socket:

    game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # reutilisable:
    game_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        game_socket.connect((HOST, int(port)))
    except socket.error:
        print("La connexion à la partie a échoué.")
        sys.exit()

    print("Connexion partie établie avec le serveur.")


    #envoi du pseudo au serveur de jeu
    print("envoi du nom à:",datetime.datetime.now())
    game_socket.sendall(nom_joueur.encode("latin-1"))
    #self.game_socket.sendall(result.encode("latin-1"))    #Lancement de l'appli graphique
    app = AppliCanevas(port,game_socket ,chiffre_status,nom_joueur)

    app.title("TCP paint")
    app.mainloop()

    print("Connexion interrompue.")
    game_socket.close()

class AppliCanevas(tk.Tk):
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
    def __init__(self,port,game_socket,chiffre_status,nom_joueur):
        #appel de la methode de l'ancêtre.
        tk.Tk.__init__(self)
        self.game_socket =game_socket
        self.nom_joueur=nom_joueur
        self.port_de_la_partie = port
        #paramètres PIL pour la copie d'image en parallèle
        #self.image1 = Image.new("RGB", (500, 500), "white")
        #self.draw = ImageDraw.Draw(self.image1)

        #status du joueur: initiateur, joueur ou spectateur
        self.chiffre_status=chiffre_status

        #paramètres classiques de tkinter
        self.size = 500
        self.creer_widgets()
        print("Lancement des widgets de AppliCanevas...")




    def creer_widgets(self):
        self.menu_left = tk.Frame(self)
        self.frame_right = tk.Frame(self)
        self.canv_frame=Label(self.frame_right)
        self.canv_frame.pack()
        self.menu_left.grid(row=0, padx=20 , pady=20,column=0, rowspan=2, sticky="nsew")
        self.frame_right.grid(row=0, column=1, sticky="ew")
        # création canevas

        self.canv= Canvas(self.canv_frame, bg="white", height=self.size,
                              width=self.size)
        ############################################################
        # lancement du thread de reception

        print("Lancement du thread de reception!\n")

        self.th=Threadreception(self ,self.game_socket)
        self.th.start()


        ############################################################

        # boutons qui n'apparaitront pas si spectateur:
        print("Le thread de reception a été lancé.\n Chargement de l'interface graphique:")
        if self.chiffre_status<=2:
            self.bouton_new = tk.Button(self.menu_left, text="New",font = "courier",
                                            command=self.New)
            self.bouton_new.pack()
            self.bouton_cercles = tk.Button(self.menu_left, text="Cercles",font = "courier",
                                            command=self.dessine_cercles)
            self.bouton_cercles.pack()
            self.bouton_lignes = tk.Button(self.menu_left, text="Lignes",font = "courier",
                                           command=self.dessine_lignes)
            self.bouton_lignes.pack()
            self.bouton_pinc_cercles = tk.Button(self.menu_left, text="Paintcercles",font = "courier",
                                            command=self.paint_cercles)
            self.bouton_pinc_cercles.pack()
            self.bouton_pinc_squares = tk.Button(self.menu_left, text="Paintsquares",font = "courier",
                                            command=self.paint_squares)
            self.bouton_pinc_squares.pack()
            self.rainbow_cercles = tk.Button(self.menu_left, text="Circle rainbow",font = "courier",
                                            command=self.rainbow_cercles)
            self.rainbow_cercles.pack()
            self.rainbow_squares = tk.Button(self.menu_left, text="Squares rainbow",font = "courier",
                                            command=self.rainbow_squares)
            self.rainbow_squares.pack()




            self.bouton_brush = tk.Button(self.menu_left, text="pinceau",font = "courier",
                                            command=self.pinceau)
            self.bouton_brush.pack()



            self.color_button = Button(self.menu_left, text='Couleur pinceau', command=self.choose_color,font = "courier")
            self.color_button.pack()

            self.color_button = Button(self.menu_left, text='Couleur fond', command=self.choose_colorbg,font = "courier")
            self.color_button.pack()

            self.etiquette2=Label(self.menu_left)
            self.etiquette2.configure(text='Taille pinceau:')
            self.etiquette2.pack()

            self.choose_size_button = Scale(self.menu_left, from_=1, to=50, orient=HORIZONTAL)
            self.choose_size_button.pack()

            self.etiquette3=Label(self.menu_left)
            self.etiquette3.configure(text='Taille diametre maximum')
            self.etiquette3.pack()
            self.choose_diam_button = Scale(self.menu_left, from_=1, to=100, orient=HORIZONTAL)
            self.choose_diam_button.pack()


            self.bouton_sauver = tk.Button(self.menu_left,pady=20, text="Envoyer",font = "courier",
                                           command=self.launch_copy_image)
            self.bouton_sauver.pack()

            self.etiquette4=Label(self.menu_left)
            self.etiquette4.configure(text=self.nom_joueur,font="courier")
            self.etiquette4.pack()



        print("Chargement des boutons qui apparaitront pour tous les utilisateurs")
        # Autres boutons:

        self.etiquette=Label(self.menu_left)
        if self.chiffre_status >2:
            self.etiquette.configure(text='Spectateur',fg = "Blue1",bg = "Blue4",font = "courier")
        else :
            self.etiquette.configure(text='TOUR: non determiné')

        self.etiquette.pack()

        self.bouton_quitter = tk.Button(self.frame_right, text="Quitter",font = "courier",
                                        command=self. exit_app)
        self.bouton_quitter.pack()

        self.canv.pack()
        self.textExample=tk.Text(self.frame_right, height=2,font = "courier")
        self.textExample.pack()
        self.btnRead=tk.Button(self.frame_right, height=1, width=10, text="Envoyer",
                            command=self.getTextInput,font = "courier")
        self.btnRead.pack()

        self.text = scrolledtext.ScrolledText(self.frame_right,height=10,font = "courier")
        self.text.insert(tk.END, "Reponses:\n")
        self.text.pack()
        if self.chiffre_status <=2:
            self.setup_pinceau()

    def config_etiquette(self):
        if self.chiffre_status == 2:
            self.etiquette.configure(text="C'est votre tour!"  , fg = "light green",bg = "dark green",font = "courier")
            self.bouton_sauver.config(state='normal')
        elif self.chiffre_status >2:
            pass
        else :
            self.etiquette.configure(text="Ce n'est pas votre tour!"  , fg = "red2",bg = "red4",font = "courier")
            self.bouton_sauver.config(state='disabled')

    def New(self):
        self.canv.delete("all")


    def launch_copy_image(self):
        ###################################
        #Code pour recentrer le widget:
        #ici j'ai volontairement conservé les noms de variables du code originel
        #pour la clarté

        # Gets the requested values of the height and widht.
        self.windowWidth = self.winfo_reqwidth()
        self.windowHeight = self.winfo_reqheight()
        print("Width",self.windowWidth,"Height",self.windowHeight)

        # Gets both half the screen width/height and window width/height
        self.positionRight = int(self.winfo_screenwidth()/2 - self.windowWidth/2)
        self.positionDown = int(self.winfo_screenheight()/2 - self.windowHeight/2)

        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(self.positionRight, self.positionDown))
        self.update()

        ###################################
        #Code qui fait la copie du Canvas:
        #ici j'ai volontairement conservé les noms de variables du code originel
        #pour la clarté
        self.chiffre_status=0
        self.config_etiquette()
        x=self.canv_frame.winfo_rootx()+self.canv.winfo_x()
        y=self.canv_frame.winfo_rooty()+self.canv.winfo_y()
        x1=x+self.canv.winfo_width()
        y1=y+self.canv.winfo_height()
        ImageGrab.grab().crop((x,y,x1,y1)).save("IMG_DATA.gif")

        self.envoi()

    def envoi(self):
        print("Envoi du fichier")
        self.msgServeur="8@^IMG_DATA"
        self.game_socket.send(bytes(self.msgServeur.encode("ascii")))
        self.fich = open("IMG_DATA.gif", "rb")

        self.Data_serveur=os.path.getsize("IMG_DATA.gif")
        self.msgServeur = str(len(str(self.Data_serveur))) + "@^" +str(self.Data_serveur)
        self.game_socket.send(bytes(self.msgServeur.encode("ascii")))
        self.num=0
        self.Data_serveur=self.Data_serveur/ 1024
        if self.Data_serveur > 1024:	# Si le fichier est plus lourd que 1024 on l'envoi par paquet
            for i in range(self.Data_serveur / 1024):

                self.fich.seek(self.num, 0) # on se deplace par rapport au numero de caractere (de 1024 a 1024 octets)
                self.message_total = self.fich.read(1024) # Lecture du fichier en 1024 octets
                self.game_socket.sendall(self.message_total) # Envoi du fichier par paquet de 1024 octets
                self.num = self.num + 1024
        else: # Sinon on envoi tous d'un coup
            self.message_total = self.fich.read()
            self.game_socket.sendall(self.message_total)
        print("Fermeture")

        self.fich.close()

    def textinsert(self,text):
        self.text.insert(INSERT, text)


    def getTextInput(self):
        self.result=self.textExample.get("1.0","end")
        #ajout de la taille du message avec un delimiteur:
        self.result = str(len(self.result)) + "@^"+self.result
        self.game_socket.sendall(self.result.encode("latin-1"))
        print ("Chaine envoyée:\n {}".format(self.result))

    #Les deux fonctions suivantes
    #fabriquent une couleur en hexa de facon aléatoire:
    def rd_col(self):
        return '#'+self.hexa_make()+self.hexa_make()+self.hexa_make()

    #reutilisation de "self.result"
    def hexa_make(self):
        self.result  =hex(rd.randint(0x0,0xff))[2:]
        if len(self.result )<2 :
            return "0" +self.result
        else :
            return self.result



    def dessine_cercles(self):
        for i in range(20):
            self.x, self.y = [rd.randint(1, self.size) for j in range(2)]
            colorfill=self.rd_col()
            coloroutline=self.rd_col()
            diameter=rd.randint(0,self.choose_diam_button.get())
            self.canv.create_oval(self.x, self.y, self.x+diameter, self.y+diameter,
                                  outline=coloroutline, fill=colorfill)


    def dessine_lignes(self):
        for i in range(20):
            self.x, self.y, self.x2, self.y2 = [rd.randint(1, self.size) for j in range(4)]
            colorfill=self.rd_col()
            self.canv.create_line(self.x, self.y, self.x2, self.y2, fill=colorfill)


    def load_image(self):
        if self.chiffre_status >2:
            pass
        else:
            self.chiffre_status =2
        self.config_etiquette()
        #chargement de l'image GIF echangée
        self.photo =PhotoImage(file="IMG_DATA.gif")
        #sur le Canvas
        self.canv.create_image(0, 0, anchor = NW, image = self.photo)

        self.canv.update()


    def setup_pinceau(self):
        self.config_etiquette()
        self.old_x = None
        self.old_y = None
        #boutton de taille du pinceau
        self.line_width = self.choose_size_button.get()
        self.diameter = self.choose_diam_button.get()


        self.pinceau=1
        self.color="black"
        self.colorbg="black"

        self.canv.bind('<B1-Motion>', self.paint)
        self.canv.bind('<ButtonRelease-1>', self.reset)


    def choose_color(self):

        self.color = askcolor(color=self.color)[1]

    def choose_colorbg(self):

        self.colorbg = askcolor(color=self.color)[1]

    def pinceau(self):
        self.pinceau=1

    def paint_cercles(self):
        self.pinceau=2
    def paint_squares(self):
        self.pinceau=3
    def rainbow_squares(self):
        self.pinceau = 4
    def rainbow_cercles(self):
        self.pinceau = 5
    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        if self.pinceau ==1 :
            if self.old_x and self.old_y:
                self.canv.create_line(self.old_x, self.old_y, event.x, event.y,
                                   width=self.line_width, fill=self.color,
                                   )
            self.old_x = event.x
            self.old_y = event.y

        if self.pinceau ==2:
            self.diameter = self.choose_diam_button.get()
            if self.old_x and self.old_y:
                self.x=event.x+self.diameter
                self.y=event.y+self.diameter
                self.canv.create_oval(self.old_x, self.old_y,self.x ,self.y ,
                                      outline=self.color, fill=self.colorbg)

            self.old_x = event.x
            self.old_y = event.y

        if self.pinceau ==3:
            self.diameter = self.choose_diam_button.get()
            if self.old_x and self.old_y:
                self.x=event.x+self.diameter
                self.y=event.y+self.diameter
                self.canv.create_rectangle(self.old_x, self.old_y,self.x ,self.y ,
                                      outline=self.color, fill=self.colorbg)

            self.old_x = event.x
            self.old_y = event.y

        if self.pinceau == 4:
            self.diameter = self.choose_diam_button.get()
            if self.old_x and self.old_y:
                self.x=event.x+self.diameter
                self.y=event.y+self.diameter
                self.canv.create_rectangle(self.old_x, self.old_y,self.x ,self.y ,
                                      outline=self.rd_col(), fill=self.rd_col())
            self.old_x = event.x
            self.old_y = event.y
        if self.pinceau == 5:
            self.diameter = self.choose_diam_button.get()
            if self.old_x and self.old_y:
                self.x=event.x+self.diameter
                self.y=event.y+self.diameter
                self.canv.create_oval(self.old_x, self.old_y,self.x ,self.y ,
                                      outline=self.rd_col(), fill=self.rd_col())
            self.old_x = event.x
            self.old_y = event.y




    def reset(self, event):
        self.old_x, self.old_y = None, None

    def exit_app(self):
        print("Envoi du signal de fermeture au serveur.")
        result = str(5) + "@^"+'^#^^^'
        self.game_socket.sendall(result.encode("latin-1"))
        print("Fermeture de Thread de reception:")

###################################################################################################
# passage un peu complexe rajouté le 28 juin 2021:
# Il s'agit de changer le dictionnaire des parties sur le serveur initial pour diminuer le nombre
# de joueurs dans la partie correspondante.
###################################################################################################
        self.HOST =sys.argv[1]

        self.PORT = int(sys.argv[2])
        #start_socket: variable globale:
        self.change_game_list_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # réutilisable:
        self.change_game_list_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.change_game_list_socket.connect((self.HOST, self.PORT))
            self.repClient = "2"
            self.change_game_list_socket.sendall(bytes(self.repClient,"utf-8"))
            print("On appelle le serveur pour le prévenir qu'un joueur s'est déconnecté.")
            #envoi du port de la partie de jeu pour que le serveur décrémente le nb de joueurs:
            self.change_game_list_socket.sendall(bytes(self.port_de_la_partie,"utf-8"))
            print("Le port ",self.port_de_la_partie," a été envoyé.")

        except socket.error:
            print("La connexion au serveur pour changer la valeur des joueurs de la partie a échoué.")

###################################################################################################
        self.th.quithread()
        print("Fermeture de l'AppliCanevas")
        self.destroy()
        os._exit(0)

class Threadreception(threading.Thread):
    '''dérivation d'un objet thread pour gérer la connexion avec un client'''
    def __init__(self, AppliCanevas,connexion):
        threading.Thread.__init__(self)
        self.AppliCanevas=AppliCanevas
        self.game_socket =connexion
        self.levier=1
        print("Thread de reception en chargement")

    def run(self):
        #recuperation du nom du thread
        self.nom = self.getName()
        print(self.nom,"lancé pour la reception")
        self.msgServeur  =""
        self.Data_Serveur=""
        self.message_total=""
        self.taille_message=""
        ###############petit message du serveur:
        while len(self.msgServeur) < 44:
            self.Data_Serveur = self.game_socket.recv(1).decode("Utf8")
            self.msgServeur += self.Data_Serveur

        print("**********************************************\nServeur:",self.msgServeur,"\n\
**********************************************\n")
        ##############

        while self.levier: # Boucle de reception
            self.message_total= self.recep_message()
            if not self.message_total :
                print("Message null du serveur. Fermeture de connection.")
                break
            print("message reçu:|",self.message_total,"|")
            if self.message_total == 'IMG_DATA':
                print("Code IMG_DATA reçu:")
                print("Lancement de la fonction de reception...")
                self.reception()
                self.AppliCanevas.load_image()
            else:
                self.AppliCanevas.textinsert(self.message_total)
# Fermeture de la connexion :
        self.game_socket.close()
# couper la connexion côté serveur
        del conn_client[nom]
   # supprimer son entrée dans le dictionnaire
        print("Client %s déconnecté." % nom)

    def quithread(self):
        self.levier=0




    def recep_message (self):

        self.Data_serveur=""
        self.taille_message=""
        self.message_total=""
        #self.game_socket= connexion

        while 1:

            self.Data_serveur = self.game_socket.recv(1).decode('latin-1')
            self.taille_message = self.taille_message +self.Data_serveur
            if "@^" in self.taille_message:
                break

        self.taille_message,ignored,self.message_total =self.taille_message.partition('@^')

        while len(self.message_total) < int(self.taille_message):
            self.Data_serveur = self.game_socket.recv(1).decode('latin-1')
            self.message_total = self.message_total +self.Data_serveur

        return self.message_total


    def reception(self):

        self.taille_message = self.recep_message()
        print("taille du fichier:",self.taille_message)

        self.message_total=0
        self.fich= open("IMG_DATA.gif", "wb")
        print("Reception du fichier")
        while self.message_total < int(self.taille_message) :
            print(".",end="")
            self.data_serveur = self.game_socket.recv(1024)
            self.message_total += len(self.data_serveur)

            self.fich.write(self.data_serveur)
        print("Fermeture du fichier")
        self.fich.close()

def pseudo():
    print("Veuillez taper votre pseudo (MAX 10 caraceres):")
    repClient=input("Pseudo:")
    #si Pseudo trop grand il est tronqué:
    if len(repClient) >10:
        repClient=repClient[:10]
    # si pseudo trop petit il est rallongé:
    elif len(repClient) <10:
        repClient = repClient + (10-(len(repClient))) * (" ")
    start_socket.sendall(bytes(repClient.encode("latin-1")))
    return repClient

def connection_start():


    #ici, un prompt est envoyé par le Serveur
    msgServeur = ""
    total=""
    #Reception de la longeur du prompt
    while len(total) < 4:
        buffer = start_socket.recv(1).decode("utf-8")
        total += buffer
    print("Le prompt fera",total)
    #Boucle de reception:
    while len(msgServeur) < int(total):
        buffer = start_socket.recv(100).decode("utf-8")
        msgServeur += buffer
    print(msgServeur)

    pseudo1 =pseudo()

    # reponse au menu du serveur start:
    choice(pseudo1)






def choice(pseudo1):

    #ici on reste sur start_socket:

    msgServeur =""


    repClient =input ("**********************************************\nVeuillez choisir votre option: ")

    if repClient == "1":
        start_socket.sendall(bytes(repClient,"utf-8"))
        Game_port=""
        #Reception du port pour la partie:
        while len(Game_port) < 5:
            Data_Serveur = start_socket.recv(8).decode("utf-8")
            Game_port += Data_Serveur

        start_socket.close()

        #attente que le serveur fasse le fork de son coté
        time.sleep(1)

        chiffre_status=1
        print("Status du joueur: initiateur de jeu.")

        connection_game(Game_port, chiffre_status ,pseudo1)
    if repClient == "2":
        start_socket.sendall(bytes(repClient,"utf-8"))
        while len(msgServeur) < 33:
            buffer = start_socket.recv(1).decode("latin-1")
            msgServeur += buffer
        print("**********************************************\nServeur:",msgServeur,"\n\
**********************************************\n")
        if msgServeur[:3]=="Err":
            choice(pseudo1)
        else:

            Nom_thread(repClient,msgServeur,pseudo1)
    elif repClient == "3":
        print("Nouvelle demande du prompt:")
        start_socket.sendall(bytes(repClient,"utf-8"))
        connection_start()

    elif repClient =="4":
        sys.exit()
    else:
        print("Votre demande ne correspond pas aux options.")
        #le choix continue indéfiniment tant qu'un bon chiffre n'est pas donné
        choice(pseudo1)

def Nom_thread(repClient,msgServeur,pseudo1):
    msgServeur=""

    while len(msgServeur) < 33:
        buffer = start_socket.recv(1).decode("latin-1")
        msgServeur += buffer
    print("**********************************************\nServeur:",msgServeur,"\n\
**********************************************\n")


    # demande du choix du Thread par le serveur

    msgServeur =""
    repClient =input ("Nom du thread: ")
    #reduction du nom du Thread à la taille du prochain envoi:

    if len(repClient) <9:
        repClient =repClient +( (9 - len(repClient))*" ")
    repClient = repClient[:9]
    start_socket.sendall(bytes(repClient,"latin-1"))

    #à ce moment le serveur calcul le status du joueur
    #(qui fait 1 octet)
    chiffre_status= start_socket.recv(1).decode("Utf8")
    if chiffre_status == "2":
        print("Status du joueur: Deuxième joueur.")
    elif chiffre_status == "%":
        print("Désolé, le serveur n'a pas reconnu votre choix de thread.")
        Nom_thread(repClient,msgServeur,pseudo1)
        return

    elif chiffre_status > "2":
        print("Status du joueur: Spectateur.")

    print("Reception du port de la partie...")
    while len(msgServeur) < 5:
        buffer = start_socket.recv(50).decode("utf-8")
        msgServeur += buffer
    print("Port reçu!! Connexion:")
    start_socket.close()
    connection_game(msgServeur,int(chiffre_status),pseudo1)
    sys.exit()



if __name__ == "__main__":
     #première connection :
    if len(sys.argv)<3:
        print("Veuillez préciser l'IP du serveur et son port")
        sys.exit()

    HOST =sys.argv[1]

    PORT = int(sys.argv[2])
    #start_socket: variable globale:
    start_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # réutilisable:
    start_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    if len (sys.argv)>1 :
        try:
            start_socket.connect((HOST, PORT))
            #Envoi de l'octet qui indique le lancement d'un echange normal.
            repClient = "1"
            start_socket.sendall(bytes(repClient,"utf-8"))

        except socket.error:
            print("La connexion au serveur de départ a échoué.")
            sys.exit()
        connection_start()

    else :
        try:
            start_socket.connect((HOST, PORT))
        except socket.error:
            print("La connexion au serveur de départ sur le port 35555 en localhost a échoué.")
            sys.exit()
        connection_start()
