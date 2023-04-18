from Inventaire import Inventaire
import os
import random
import time

#fonction pour gérer les combats
class Character() :
    def __init__(self, Name, Health=100, Oxygen=0, Ammo=0, Attack=20, Defense=10):
        self.Name      = Name
        self.Health    = Health
        self.MaxHealth = Health
        self.Armor     = None
        self.Oxygen    = Oxygen
        self.Ammo      = Ammo
        self.Inventory = Inventaire()
        self.Attack    = Attack
        self.Defense   = Defense

    def fight(self, Koopas):
        while self.Health > 0 and Koopas.Health > 0 :
            self.clear_terminal()
            self.display_fight_stats()
            Koopas.display_fight_stats()
            print(' ')
            # Afficher les options du combat
            print("Que voulez-vous faire?")
            print("1. Attaquer")
            print("2. Utiliser un objet")
            print("3. Fuir")
            choix = input("Choisissez une option : ")
            Choice= ["1","2","3"]
            while choix not in Choice : 
                print("Veuillez choisir une option valide :")
                choix = input("Choisissez une option : ")
            print("----------------------------------------------------")
            if choix == "1":
                # Le joueur fait l'Attack
                damage = int((((self.Attack/Koopas.Defense)*10)+1)*(random.randrange(85, 100)/100))
                Koopas.Health = Koopas.Health - damage  
                print(f"{self.Name} inflige {damage} points de dégats à {Koopas.Name}")
                print("----------------------------------------------------")
                time.sleep(1)
            elif choix == "2": # Création d'une liste d'objets
                self.Inventory.show_inv()
                print("----------------------------------------------------")
                item = input("Quel objet voulez-vous utiliser ? (quit pour annuler)\n> ")
                while item.lower() != "quit" and not self.Inventory.have_item(item.lower().capitalize()):
                    print("Vous n'avez pas cet objet")
                    print("----------------------------------------------------")
                    self.Inventory.show_inv()
                    print("----------------------------------------------------")
                    item = input("Quel objet voulez-vous utiliser ? (quit pour annuler)\n> ")
                if item.lower() == "quit":
                    continue
                self.Inventory.get_item(item.lower().capitalize()).use(self)
                time.sleep(1)
            else:
                print("Vous fuyez")
                print("----------------------------------------------------")
                return True
            # L'ennemi fait l'Attack
            damage = int((((Koopas.Attack/self.Defense)*10)+1)*(random.randrange(85, 100)/100))
            self.Health = self.Health - damage
            print(f"{Koopas.Name} vous inflige {damage}")
            print("----------------------------------------------------")
            time.sleep(1)
        if self.Health <=0:
            print("Vous avez été vaincu")
            print("----------------------------------------------------")
            return False
        if Koopas.Health <= 0 :
            print(f"Vous avez vaincu {Koopas.Name}")
            print("----------------------------------------------------")
            time.sleep(1)
            self.clear_terminal()
            return True

    def show_stats(self):
        print(f"Statistique de {self.Name} :")
        print(f"PV : {self.Health}")
        print(f"Oxygène : {self.Oxygen}")
        print(f"Munitions : {self.Ammo}")
        print(f"Attaque : {self.Attack}")
        print(f"Défense : {self.Defense}")
        print("----------------------------------------------------")

    def display_fight_stats(self):
        print(f"{self.Name} :")
        percent = int((self.Health / self.MaxHealth) * 100)
        print(f"{'█' * (percent // 10)}{'░' * (10 - (percent // 10))} {self.Health}/{self.MaxHealth} ({percent}%)")

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def copy(self):
        copy =  Character(self.Name, self.MaxHealth, self.Oxygen, self.Ammo, self.Attack, self.Defense)
        copy.Inventory = self.Inventory.copy()
        return copy

    def export(self):
        return {
            "name": self.Name,
            "health": self.Health,
            "MaxHealth": self.MaxHealth,
            "oxygen": self.Oxygen,
            "ammo": self.Ammo,
            "attack": self.Attack,
            "defense": self.Defense,
            "items": self.Inventory.export()
        }

    def createFromJson(data):
        player = Character(data["name"], data["health"], data["oxygen"], data["ammo"], data["attack"], data["defense"])
        player.MaxHealth = data["MaxHealth"]
        player.Inventory = Inventaire(data["items"])
        return player

