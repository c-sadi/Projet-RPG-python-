from Item import Item
import random

class Inventaire:
    def __init__(self, content = []):
        self.content = []
        for item in content:
            self.content.append(Item(item))

    def show_inv(self, emptyMessage = "Votre inventaire est vide"):
        if self.get_size() == 0:
            print(emptyMessage)
        else:
            for item in self.get_available_items():
                print(f"- {item.name} x{item.quantity}")
                print(f"  \"{item.description}\"")

    def pickup_item(self, item):
        pickup=input("Voulez vous prendre l'objet ?(y/n)\n> ")
        if pickup == "y":
            self.add_item(item.copy())
            return True
        else:
            print("Vous decidez de ne rien faire.")
            return False

    def search_item(self):
        return random.choice(self.get_available_items())

    def includes(self, name):
        for item in self.content:
            if item.name == name:
                return True
        return False

    def have_item(self, name):
        for item in self.get_available_items():
            if item.name == name:
                return True
        return False

    def get_item(self, name):
        if self.includes(name):
            for item in self.content:
                if item.name == name:
                    return item
        else:
            return None

    def add_item(self, item):
        if self.includes(item.name):
            current_item = self.get_item(item.name)
            current_item.quantity += item.quantity
        else:
            self.content.append(item)

    def remove_item(self, name, quantity = 1):
        if self.includes(name):
            current_item = self.get_item(name)
            current_item.quantity -= quantity
            if current_item.quantity <= 0:
                self.content.remove(current_item)
        else:
            print("Vous n'avez pas cet objet")

    def get_size(self):
        return len(self.get_available_items())

    def get_available_items(self):
        available_items = []
        for item in self.content:
            if item.quantity > 0:
                available_items.append(item)
        return available_items

    def export(self):
        export = []
        for item in self.content:
            export.append(item.export())
        return export

    def copy(self):
        return Inventaire(self.export())

