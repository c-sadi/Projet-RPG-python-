class Item:
    def __init__(self, json, quantity = None):
        self.name = json.get('name')
        self.description = json.get("description") or "Pas de description."
        self.quantity = quantity or json.get('quantity') or 1

    def use(self, player, quantity = 1):
        if self.quantity >= quantity:
            self.quantity -= quantity
            print(f"{player.Name} utilisez {str(quantity)} {self.name}.")
            if self.name == "Potion":
                for i in range(quantity):
                    self.potion(player)
            elif self.name == "Super potion":
                for i in range(quantity):
                    self.potion(player, 50)
            else:
                print("Vous ne savez pas utiliser cet item.")
                self.quantity += quantity
            print("----------------------------------------------------")
            return True
        else:
            return False

    def add(self, quantity = 1):
        self.quantity += quantity

    def potion(self, player, health = 20):
        baseHealth = player.Health
        player.Health += health
        if player.Health > player.MaxHealth:
            player.Health = player.MaxHealth
        print(f"{player.Name} récupère {player.Health - baseHealth} points de vie.")
        return True

    def copy(self):
        return Item({ 'name': self.name, 'description': self.description, 'quantity': self.quantity})

    def export(self):
        return { 'name': self.name, 'description': self.description, 'quantity': self.quantity}
