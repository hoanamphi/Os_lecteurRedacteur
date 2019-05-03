from threading import *
from random import *

# Donnees : Ensemble de messages quelconques
# Les lecteurs peuvent les afficher et les redacteurs les modifier, en ajouter de nouveaux ou en supprimer
messages = ["message1", "message2", "message3"]

# Semaphore pour controler l'exclusion mutuelle entre lecteur et redacteur
mutual_exclusion = Semaphore(1)

# Semaphore pour controler l'acces des redacteurs
verrou_redacteur = Semaphore(0)
# Semaphore pour controler l'acces des lecteurs
verrou_lecteur = Semaphore(0)

# Nombre de redacteurs accedant ou voulant acceder aux donnees
nombre_redacteur = 0
demande_redacteur = 0

# Nombre de lecteurs accedant ou voulant acceder aux donnees
nombre_lecteurs = 0
demande_lecteur = 0


# Classe definissant un lecteur
class Lecteur(Thread):

    # Juste histoire de savoir de quel lecteur on parle, on les numerote
    def __init__(self, num):
        Thread.__init__(self)
        self.number = num

    # Methode affichant un des messages au hasard dans les donnees
    def lire(self):
        print("Redacteur " + str(self.number))
        index = randrange(len(messages))

        print(messages[index])

    def run(self):
        while True:
            global nombre_redacteur, demande_redacteur, nombre_lecteurs, demande_lecteur

            # Le lecteur verrouille les actions
            mutual_exclusion.acquire()

            # Si il y a deja des redacteurs ou que des redacteurs on demande à acceder aux donnees
            if nombre_redacteur > 0 or demande_redacteur > 0:

                # Le lecteur signale qu'il veut acceder aux donnes
                demande_lecteur += 1

                # Le lecteur libere les actions
                mutual_exclusion.release()

                # Le lecteur attend que les redacteurs liberent l'acces
                verrou_lecteur.acquire()

                # Le lecteur verrouille les actions
                mutual_exclusion.acquire()
                # Il n'est plus demandeur
                demande_lecteur -= 1

            # Le lecteur s'ajoute aux lecteurs accedant aux donnees
            nombre_lecteurs += 1
            # Le lecteur libere les actions
            mutual_exclusion.release()

            self.lire()

            # Le lecteur verrouille les actions
            mutual_exclusion.acquire()
            # Le lecteur n'accede plus aux donnees
            nombre_lecteurs -= 1

            # S'il il n'y a plus de lecteur ou qu'un redacteur a fait une demande d'acces
            # CONCLUSION : Les redacteurs ont la priorite :
            # Meme si il y a encore des lecteurs en cours un redacteur peut demander à acceder aux donnees
            # Tandis que les lecteurs ne peuvent que si aucun redacteur n'accede ou demande les donnees
            if nombre_lecteurs == 0 or demande_redacteur > 0:
                # On libere l'acces aux redacteurs
                verrou_redacteur.release()

            # On libere les actions
            mutual_exclusion.release()


# Classe definissant un redacteur
class Redacteur(Thread):

    # Juste histoire de savoir de quel redacteur on parle, on les numerote
    def __init__(self, num):
        Thread.__init__(self)
        self.number = num

    # Methode permettant au redacteur de choisir une action à effectuer
    def choisir(self):
        print("Redacteur " + str(self.number))
        print("Faire un choix")
        print("1) lire")
        print("2) modifier")
        print("3) ajouter")
        print("4) supprimer")

        choix = int(input())
        if choix == 1:
            self.lire()
        else:
            if choix == 2:
                self.modifier()
            else:
                if choix == 3:
                    self.ajouter()
                    if choix == 4:
                        self.supprimer()

    # Methode affichant le message selectionné par le redacteur
    @staticmethod
    def lire():
        index = int(input("Index du message à lire : "))

        print(messages[index])

    # Methode modifiant le message selectionné par le redacteur
    @staticmethod
    def modifier():
        index = int(input("Index du message à modifier : "))
        m = input("Nouveau message : ")

        messages[index] = m

    # Methode ajoutant un nouveau message
    @staticmethod
    def ajouter():
        m = input("Nouveau message : ")

        messages.append(m)

    # Methode supprimant un message
    @staticmethod
    def supprimer():
        index = int(input("Index du message à supprimer : "))

        messages.pop(index)

    def run(self):
        while True:
            global nombre_lecteurs, nombre_redacteur, demande_lecteur, demande_redacteur

            # Le redacteur verrouille les actions
            mutual_exclusion.acquire()

            # Si il y a des redacteurs, des lecteurs ou des demandes de redacteurs
            if nombre_redacteur > 0 or nombre_lecteurs > 0 or demande_redacteur > 0:
                # Le redacteur s'ajoute dans les demandeurs
                demande_redacteur += 1

                # Le redacteur libere les actions
                mutual_exclusion.release()

                # Le redacteur attend que les lecteurs liberent l'acces
                verrou_redacteur.acquire()

                # Le redacteur verrouille les actions
                mutual_exclusion.acquire()
                # Il n'est plus demandeur
                demande_redacteur -= 1

            # Le redacteur s'ajoute aux redacteurs accedant à la donnees
            nombre_redacteur += 1
            # Le redacteur libere les actions
            mutual_exclusion.release()

            self.choisir()

            # Le redacteur verrouille les actions
            mutual_exclusion.acquire()
            # Le redacteur n'accede plus aux donnees
            nombre_redacteur -= 1

            # Si des redacteurs demandent à acceder aux donnees
            if demande_redacteur > 0:
                # On libere l'acces aux redacteurs
                verrou_redacteur.release()
            else:
                # Si des lecteurs demandent à acceder aux donnees
                if demande_lecteur > 0:
                    # On libere l'acces aux lecteurs
                    for i in range(demande_lecteur):
                        verrou_lecteur.release()
            # Le redacteur libere les actions
            mutual_exclusion.release()


if __name__ == "__main__":
    lecteur = Lecteur(1)
    lecteur2 = Lecteur(2)
    redacteur = Redacteur(1)
    redacteur2 = Redacteur(2)

    lecteur.start()
    lecteur2.start()
    redacteur.start()
    redacteur2.start()
