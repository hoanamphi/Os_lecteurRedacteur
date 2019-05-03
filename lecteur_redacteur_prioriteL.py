from threading import *
from random import *
from time import *

# Donnees : Ensemble de messages quelconques
# Les lecteurs peuvent les afficher et les redacteurs les modifier, en ajouter de nouveaux ou en supprimer
messages = ["message1", "message2", "message3"]
# Semaphore pour controler l'acces aux donnees
acces_messages = Semaphore(1)

# Nombre de lecteurs accédant aux données en même temps
nombre_lecteurs = 0
# Semaphore pour controler l'accès à la variable nombre_lecteurs
verrou_nombre_lecteurs = Semaphore(1)


# Classe définissant un lecteur
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
            global nombre_lecteurs

            # Le lecteur accède à la variable nombre_lecteurs pour signaler qu'il veut accèder à la donnée
            verrou_nombre_lecteurs.acquire()
            nombre_lecteurs += 1

            # Le premier lecteur verrouille l'acces aux donnees
            # Tous les autres lecteurs peuvent y accéder mais pas les redacteurs
            if nombre_lecteurs == 1:
                acces_messages.acquire()

            # Le lecteur libère l'accès à la variable nombre_lecteurs
            verrou_nombre_lecteurs.release()

            # Le lecteur accès aux donnees
            self.lire()

            # Le lecteur accède à la variable nombre_lecteurs pour signaler qu'il a cessé ces actions sur les donnees
            verrou_nombre_lecteurs.acquire()
            nombre_lecteurs -= 1

            # L'acces aux donnees n'est libere que lorsque le dernier lecteur a fini son activite
            # CONCLUSION : Les lecteurs ont la priorite sur les redacteurs :
            # Ces derniers ne peuvent accéder aux donnees que en l'absence de lecteur
            # Tandis que les lecteurs peuvent y acceder librement
            if nombre_lecteurs == 0:
                acces_messages.release()

            # Le lecteur libère l'accès à la variable nombre_lecteurs
            verrou_nombre_lecteurs.release()

            # Les lecteurs ont tendance à s'allier et à ne jamais laisser la place aux redacteurs
            # Il faut juste les endormir un peu pour les faire partager
            sleep(0.2)


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
            # Accede aux donnees
            acces_messages.acquire()

            self.choisir()

            acces_messages.release()


if __name__ == "__main__":
    lecteur = Lecteur(1)
    lecteur2 = Lecteur(2)
    redacteur = Redacteur(1)
    redacteur2 = Redacteur(2)

    lecteur.start()
    lecteur2.start()
    redacteur.start()
    redacteur2.start()
