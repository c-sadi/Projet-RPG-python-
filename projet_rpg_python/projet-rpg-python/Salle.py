import random
from Inventaire import Inventaire
from Character import Character

class Salle:
    def __init__(self, json):
        self.name = json.get('name')

        self.mobs = []
        mobsData = json.get('mobs') or []
        for mob in mobsData:
            name = mob.get('name')
            health = mob.get('health') or 100
            oxygen = mob.get('oxygen') or 0
            ammo = mob.get('ammo') or 0
            attack = mob.get('attack') or 20
            defense = mob.get('defense') or 10
            mobObject = Character(name, health, oxygen, ammo, attack, defense)
            mobObject.Inventory = Inventaire(mob.get('items') or [])
            self.mobs.append(mobObject)

        self.items = Inventaire(json.get('items') or [])
        self.description = json.get('description') or ""
        self.exits = json.get('exits') or {}
        self.item_chance = json.get('item_chance') or 0
        self.fight_chance = json.get('fight_chance') or 0

    def search_item(self):
        return self.items.search_item()

    def search_fight(self):
        return random.choice(self.mobs).copy()

    def roll(self, chance):
        res = False
        rolled = random.random()
        if rolled < chance:
            res = True
        return res

    def roll_fight(self):
        if len(self.mobs) == 0:
            return False
        return self.roll(self.fight_chance)

    def roll_items(self):
        if self.items.get_size() == 0:
            self.display_items()
            return False
        return self.roll(self.item_chance)

    def display_items(self):
        print("Liste des items présent dans la salle :")
        self.items.show_inv("Il n'y a pas d'items dans cette salle.\n")

    def display_exits(self):
        if len(self.exits) == 0:
            print("Il n'y a pas de sortie dans cette salle.")
        else:
            print("Liste des sorties de la salle :")
            for direction, salle in self.exits.items():
                print(f"- {salle} ({direction})")

    def remove_item(self, name, quantity=1):
        self.items.remove_item(name, quantity)

    def export(self):
        mobs = []
        for mob in self.mobs:
            mobs.append(mob.export())
        return {
            "name": self.name,
            "items": self.items.export(),
            "mobs": mobs,
            "description": self.description,
            "exits": self.exits,
            "item_chance": self.item_chance,
            "fight_chance": self.fight_chance
        }
