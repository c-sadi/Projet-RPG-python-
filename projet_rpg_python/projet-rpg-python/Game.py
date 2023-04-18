import json
from Salle import Salle
import os
from Character import Character

class Game:
    def __init__(self, name = "Player"):
        self.current_room = None
        self.player = Character(name, Oxygen=100, Ammo=10, Attack=35, Defense=15)
        with open('dico_salle.json', "r") as f:
            data = json.load(f)
        self.rooms = Game.load_rooms(data)

    def get_room_by_name(self, name):
        for room in self.rooms:
            if room.name == name:
                return room

    def check_room(self, room):
        if room.roll_fight():
            ennemy = room.search_fight()
            print(f"Vous rencontrez un {ennemy.Name} !")
            print ("Défendez vous !")
            if not self.player.fight(ennemy):
                return False
        else:
            print(room.description)
        # TODO : Compteur enemie a 0, donne clé pour combat boss pour gagner

        search = input("Voulez vous fouiller la salle?: (y/n)\n> ")
        print(' ')
        if search == "y":
            if room.roll_items():
                found_item = room.search_item()
                print(f"Vous avez trouvé {found_item.name} x{found_item.quantity} !")
                if self.player.Inventory.pickup_item(found_item):
                    room.remove_item(found_item.name, found_item.quantity)
            else:
                print("Vous n'avez rien trouvé. Dommage !")

        else:
            print("Vous decidez de ne rien faire.")
        print(' ')
        
        room.display_exits()
        return True

    def move(self, direction):
        result = True
        if direction in self.current_room.exits:
            self.current_room = self.get_room_by_name(self.current_room.exits[direction])
            print(f'Vous êtes entré dans la salle {self.current_room.name}')
            result = self.check_room(self.current_room)
        else:
            print("Vous ne pouvez pas aller par la.")
        return result

    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')

    def save(self):
        result = {}
        result['player'] = self.player.export()
        result['current_room'] = self.current_room.name
        result['rooms'] = []
        for room in self.rooms:
            result['rooms'].append(room.export())
        with open("save.json", "w") as f:
            json.dump(result, f, indent=4)

    def load_rooms(data):
        rooms = []
        for room in data['rooms']:
            rooms.append(Salle(room))
        return rooms

    def main_loop(self):
        print('\nQue voulez vous faire ?')
        command = input("> ")
        Game.clear_terminal()
        if command.lower() == "quit":
            return False
        elif command.lower() in ["nord", "sud", "est", "ouest"]:
            if not self.move(command.lower()):
                print("Vous avez perdu !")
                return False
        elif command.lower() == "inventaire":
            self.player.Inventory.show_inv()
        elif command.lower() == "stats":
            self.player.show_stats()
        elif command.lower() == "save":
            self.save()
            print("Partie sauvegardée !")
        elif command.lower() == "help":
            print("Voici les commandes disponibles :")
            print('')
            print("- nord, sud, est, ouest : pour se déplacer")
            print("- inventaire : pour afficher votre inventaire")
            print("- stats : pour afficher vos statistiques")
            print("- save : pour sauvegarder votre partie")
            print("- help : pour afficher les commandes")
            print("- quit : pour quitter le jeu")
        else:
            print("Pas compris chef.")
        return True

    def start(self, starting_room = None):
        if starting_room is not None:
            self.current_room = self.get_room_by_name(starting_room)
        self.check_room(self.current_room)

        while self.main_loop():
            pass

    def create(data):
        player = Character.createFromJson(data.get('player'))
        game = Game()
        game.player = player
        game.rooms = Game.load_rooms(data)
        game.current_room = game.get_room_by_name(data.get('current_room'))
        return game
