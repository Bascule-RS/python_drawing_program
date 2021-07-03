#! /usr/bin/env python3
# *******************************************************
# Nom ......... : TCP_paint_server.py
# Rôle ........ : Serveur d'un logiciel de dessin avec redistribution réseau
# Auteur ...... : Nicolas Tercé
# Version ..... : V0.1 du 29/06/2020
# Licence ..... : réalisé dans le cadre du cours de IED Paris8
# 
# Compilation : pas de compilation nécessaire
# Usage : Pour exécuter : ./TCP_paint_server.py
#********************************************************/

import os
import socket
import sys, threading
import datetime



#threading du menu de départ:
class Thread_conn_start(threading.Thread):
    '''dérivation d un objet thread pour gérer les connections aux parties'''
    def __init__(self,conn):
        threading.Thread.__init__(self)
        self.connexion = conn


    def run(self):
        self.repClient=self.connexion.recv(1).decode("Utf8")
        if self.repClient == "1":
            #condition "1", lancement d'un échange normal:
            #recuperation du nom du thread:
            self.nom= self.getName()


            self.prompt()
        elif self.repClient == "2":
            print("**********************************************\n")
            print("Supression d'un joueur dans game_list:")
            #la condition "2" permet à un joueur d'indiquer qu'il a quitté la partie
            self.game_list_port=""
            self.buffer=""
            #reception du port de la partie:
            while len(self.game_list_port) < 5:
                self.buffer = self.connexion.recv(1).decode("utf-8")
                self.game_list_port += self.buffer
            print("Le port reçu est :",self.game_list_port)
            for key, value in game_list.items() :
                if value[0] == int(self.game_list_port):
                    value[1]-=1
                    print("Nombre de joueurs décrémenté pour la partie",key," sur le port ", value[0])





    def prompt(self):

        if not game_list:
            print ("Pas de Jeu enregistré.")

        else:
            print ('{} jeu(x) enregistré(s)'.format(len(game_list)))


        #envoi du prompt:
        prompt="**********************************************\n\
                    _____    ___  ___   \n\
                   |_   _| / ___||  _ \ \n\
                     | |  | |    | |_) |\n\
                     | |  | |___ |  __/ \n\
                     |_|   \____||_|    \n\
                                        \n\
                       _         _      \n\
         _ __    __ _ (_) _ __  | |_    \n\
        | '_ \  / _` || || '_ \ | __|   \n\
        | |_) || (_| || || | | || |_    \n\
        | .__/  \__,_||_||_| |_| \__|   \n\
        |_|                             \n\
**********************************************\n\
Bienvenue sur le serveur des Jeux             \n\
**********************************************\n\
Liste des Jeux en cours:                      \n"

        if not game_list:
            print("Pas de parties enregistrées.\n")
            prompt=prompt + "Pas encore de jeu en cours...     \n"
        else:
            prompt = prompt +"|Nom du Thread:|"+"Port:|"+"Initiateur:|"+"Nb joueurs:"+"\n"
            for key, value in game_list.items() :
                nomthread = key + ((14 -len(key))*" ") #on ajuste le nom du thread au cas ou son numero a 2 chiffres
                prompt = prompt +"|"+nomthread+  "|"+ str(value[0])+"|"+str(value[2])+" |"+str(value[1])\
                +"\n"


        prompt = prompt+ "**********************************************\n\
*************MENU:****************************\n\
**********************************************\n\
1.Commencer une partie                        \n\
2.Rejoindre une partie                        \n\
3.Demander le prompt à nouveau                \n\
4.Quitter                                     \n\
**********************************************\n"
        total = len(prompt)
        print ("La longueur du prompt est : ",total)
        #envoi de la longueur du prompt :
        self.connexion.send(bytes(str(total),"utf-8"))
        #envoi du prompt:
        self.connexion.send(bytes(prompt,"utf-8"))
        print("Prompt envoyé au client!")
        self.get_pseudo()

        self.get_choice()

    def get_pseudo(self):
        self.pseudo=""
        #reception du pseudo
        while len(self.pseudo) < 10:
            self.buffer = self.connexion.recv(1).decode("latin-1")
            self.pseudo += self.buffer




    def get_choice(self ):

        self.repClient=self.connexion.recv(1).decode("Utf8")
        if self.repClient == "1":
            print("**********************************************\n")
            print("Nouvelle partie: ajout à la base de données:")


            if not game_list:# si c'est la première partie

                game_list[self.nom]=[50000,1,self.pseudo] #la valeur du port le plus bas est 50000
            else :
                game_list[self.nom]=[0,1,self.pseudo]
                for i in game_list.values() : #sinon recupérer le numero de port
                #le plus elevé:
                    if game_list[self.nom][0]<=i[0] : #i[0] désigne le numero de port de chaque
                                            #partie
                        game_list[self.nom][0]= i[0] +1 # l'incrémenter


#==================
            print("Le dictionnaire game_list contient désormais: ")
            for key, value in game_list.items() :
                print (key, value)
#===================

            print ("Nouvelle partie:\n"+self.nom,game_list[self.nom][0])
            print("Envoi du port au client...")
            self.connexion.send(bytes(str(game_list[self.nom][0]),"utf-8"))

            fork1(game_list[self.nom][0],self.nom)
        elif self.repClient == "2":#si le client veut joindre une partie et qu'il
        #n'y en a pas
            print("**********************************************\n")
            if not game_list:
                print("Erreur : Pas de partie disponible pour le choix 2")
                self.connexion.send(bytes("Erreur: pas de partie disponible ","utf-8"))
                self.get_choice()
            else:
                self.connexion.send(bytes("Chargement de demande de Thread  ","latin-1"))
                self.prompthread()
        elif self.repClient =="3":
            self.prompt()
        else :
            self.get_choice()

    def prompthread(self):
        self.repClient=""
        #prompt de la demande de thread
        #on va incrémenter la variable
        print("**********************************************\n")
        print("Envoi de la demande du Thread.")
        self.connexion.send(bytes("Veuillez choisir le nom du Thread","latin-1"))
        #Reception de la réponse:

        while len(self.repClient) < 9:
            buffer = self.connexion.recv(1).decode("latin-1")
            self.repClient += buffer
        if self.repClient[8]==" ":
            self.repClient = self.repClient[:8]
    #===================
        print("Le dictionnaire game_list contient: ")
        for clé, value in game_list.items() :
            print (clé, value)
    #===================
        print ("Le nom de Thread reçu est:",self.repClient)

        for clé in game_list:
            if clé == self.repClient:
                game_list[self.repClient][1]+=1
                game_list[self.repClient].append(self.nom)

                print("Envoi du status de joueur:",game_list[self.repClient][1])
                self.connexion.send(bytes(str(game_list[self.repClient][1]),"utf-8"))
                print("Envoi du port:")
                self.connexion.send(bytes(str(game_list[self.repClient][0]),"utf-8"))
                return



        print("Erreur, la partie demandée n'existe pas!")
        #on envoit un erreur qui relancera le code de demande
        #coté client.
        self.connexion.send(bytes("%","utf-8"))
        self.prompthread()
        return














#threading du jeu:
#ce thread se lance à chaque connection d'un joueur
#pour gerer plusieurs connections simultanées
class Thread_conn_game(threading.Thread):
    '''dérivation d un objet thread pour gérer une partie'''
    def __init__(self,clientsocket):
        threading.Thread.__init__(self)
        self.connexion = clientsocket

    def run(self):
        print("**********************************************\n")
        print("Thread de partie lancé")
        print("Reception du pseudo à ",datetime.datetime.now())
        self.pseudo =""
        #Cette reception du pseudo correspond cette fois au serveur de jeu distant
        while len(self.pseudo) < 10:
            self.buffer = self.connexion.recv(1).decode("latin-1")
            self.pseudo += self.buffer
        print("Le pseudo connecté au thread est: ",self.pseudo)
        ##################################

        # Mémoriser la connexion dans le dictionnaire :
        self.nom= self.pseudo+ "("+self.getName()+")" # identifiant du thread
        connection_game[self.nom] = self.connexion


        # Message adréssé au client:
        self.msg ="Vous etes connecte sur un fork a une partie."
        self.connexion.sendall(self.msg.encode("Utf8"))
        #################################
        print("L'ensemble des threads et des connection est: ")
        for key , value in connection_game.items():
            print(key,value)
        #################################
        self.Data_Client=""
        self.message_total=""
        ####
        while 1:
            print("Le thread:",self.nom)
            print("Envoie ses message à:")
            for cle in connection_game:
                if cle != self.nom:
         # ne pas le renvoyer à l'émetteur
                    print(cle)

            self.message_total =self.recep_message()

            if not self.message_total or self.message_total=='^#^^^':
                break

            elif self.message_total == 'IMG_DATA':
                self.reception(connection_game[self.nom])
            else:
                self.taille_message = len(self.message_total) + len(self.nom) +2

                message = str (self.taille_message)+"@^"+"%s> %s" % (self.nom, self.message_total)

                print(message)
                 # Faire suivre le message à tous les autres clients :
                for cle in connection_game:
                    if cle != self.nom:
             # ne pas le renvoyer à l'émetteur
                        print("Diffusion du message: {} Au recepteur: {}".format(message,cle))
                        connection_game[cle].send(message.encode("latin-1"))
# Fermeture de la connexion :
        self.connexion.close()
# couper la connexion côté serveur
        del connection_game[self.nom]
        print("**********************************************\n")
   # supprimer son entrée dans le dictionnaire
        print("Client %s déconnecté." % self.nom)
        print("Fermeture du Thread_conn_game {}".format(self.nom))
        if not connection_game:
            print("Le dictionnaire connection_game est vide. Lancement de sys.exit(0)")
            os._exit(os.EX_OK)


    def recep_message (self):
        self.Data_Client=""
        self.taille_message=""
        self.message_total=""

        while 1:

            self.Data_Client = self.connexion.recv(1).decode('latin-1')
            self.taille_message = self.taille_message +self.Data_Client
            if "@^" in self.taille_message:
                break

        self.taille_message,ignored,self.message_total =self.taille_message.partition('@^')

        while len(self.message_total) < int(self.taille_message):
            self.Data_Client = self.connexion.recv(1).decode('latin-1')
            self.message_total = self.message_total +self.Data_Client

        return self.message_total


    def reception(self,conn):

        self.taille_message= self.recep_message()
        self.message_total=""
        self.Data_Client=""
        print("**********************************************\n")
        print("Boucle de reception du fichier")
        self.message_total=0
        f = open("IMG_DATA", "wb")
        while self.message_total < int(self.taille_message) :
            self.Data_Client = conn.recv(1024)
            self.message_total += len(self.Data_Client)
            print(".")
            f.write(self.Data_Client)
        print("Fermeture du fichier")
        f.close()
        self.envoi(self.nom)


    def envoi(self,socket):

        print("**********************************************\n")
        print("Boucle d'envoi du fichier")
        self.message_total='8@^IMG_DATA'
        self.nom



        self.Data_Client=0
        for cle in connection_game:
            if cle != self.nom:                # ne pas le renvoyer à l'émetteur
                print("envoi du signal 'IMG_DATA' fichier à:",cle)

                while self.Data_Client < 11:
                    self.Data_Client=connection_game[cle].send(bytes(self.message_total.encode("ascii")))
                self.Data_Client=0
        fich = open("IMG_DATA", "rb")
        self.Data_Client=0
        octets=os.path.getsize("IMG_DATA")
        print("taille du fichier:",octets)
        self.message_total = str(len(str(octets))) + "@^" +str(octets)
        for cle in connection_game:
            if cle != self.nom:
                print("envoi de la longueur de fichier à:",cle)
                while self.Data_Client < len(self.message_total):
     # ne pas le renvoyer à l'émetteur
                    self.Data_Client=connection_game[cle].send(self.message_total.encode("ascii"))
                self.Data_Client=0



        for cle in connection_game:
            if cle != self.nom:
                print("envoi du fichier à ",cle)
                while self.Data_Client < octets:
                    octet= fich.read(1)
                    self.Data_Client +=1
                    connection_game[cle].sendall(octet)
                print("Envoi du signal de fermeture à",cle)
                self.Data_Client =0
                fich.seek(0, 0)


        fich.close()




def fork1(port,Nom_thread):

    fork_pid=os.fork()
    if fork_pid < 0:
        print("fork failed!")
    if fork_pid ==0:
        print("fork réussi!")
        ##################################
        #ici lancement d'un nouveau serveur qui va gérer une partie:
        s2= socket.socket(socket.AF_INET,socket.SOCK_STREAM) # construction de la socket

        s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind de la socket
        s2.bind((sys.argv[1],port))
        #ecoute
        s2.listen(5)
        global connection_game
        connection_game = {}
        while True:
            #Accept a connection. The socket must be bound to an address
            #and listening for connections. The return value is a pair
            #(conn, address) where conn is a new socket object usable
            #to send and receive data on the connection, and address is
            # the address bound to the socket on the other end of the connection.
            clientsocket,adresse=s2.accept()

            th = Thread_conn_game(clientsocket)
            # Mémoriser la connexion dans le dictionnaire :
            #reception du pseudo (pour le serveur fork cette fois)
            it= Nom_thread
            th.start()
            ##################################

            print("Client %s connecté, adresse IP %s, port %s." %\
                (it, adresse[0], adresse[1]))


        pass
    if fork_pid >0:
        #ajout du pid à la valeur liste de la clé:
        print("Ajout du pid du fork au nom de la connection:")
        game_list[Nom_thread].append(fork_pid)
        print(Nom_thread,game_list[Nom_thread])
        print("Wait du parent")


        ret =os.waitpid(fork_pid, 0)
        if ret[0] == fork_pid:
            print("Supression de l'entrée du dictionnaire de",fork_pid)
            #petite subtilité: on ne peut pas effacer une clé d'un dictionnaire
            # sur lequel on itère.
            for cle in list(game_list):
                if game_list[cle][3]== fork_pid:
                    print("Clé trouvée:",cle,"suppression..")
                    del game_list[cle]



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Serveur paint:\nVeuillez indiquer l'ip de l'interface et le port, merci.")
        sys.exit(0)
     #première connection :
    else:

        s= socket.socket(socket.AF_INET,socket.SOCK_STREAM) # construction de la socket

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #réutilisable
        s.bind((sys.argv[1],int(sys.argv[2])))
        s.listen(5)

        # dicionnaire des connexions client
        conn_client = {}
        #dinctionnaire des listes de jeux:
        game_list={}
        print("               ___ ____ ___     ___  ____ _ _  _ ___\n\
                |  |    |__]    |__] |__| | |\ |  | \n\
                |  |___ |       |    |  | | | \|  | \n\
                                                    \n\
                ____ ____ ____ _  _ ____ ____       \n\
                [__  |___ |__/ |  | |___ |__/       \n\
                ___] |___ |  \  \/  |___ |  \       \n")
        print ("Attente de Clients..")

        while True:
            clientsocket,adresse=s.accept()
            ##################################
            th = Thread_conn_start(clientsocket)
            th.start()

            ##################################
