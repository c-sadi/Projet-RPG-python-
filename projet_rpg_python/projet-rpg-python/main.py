import sys
import json
from time import sleep as slp
from Game import Game

game = None

def Main_Menu(NG,LG,Cr,Ex):
    Game.clear_terminal()
    Choice = input("\n1 - New Game \n2 - Load Game \n3 - Credits \n4 - Exit\n> ")
    while Choice not in ["1","2","3","4"] :
        Game.clear_terminal()
        print("Veuillez saisir une réponse valide !")
        Choice = input("\n1 - New Game \n2 - Load Game \n3 - Credits \n4 - Exit\n> ")

    if Choice == "1" :
        NG()
    elif Choice == "2" :
        LG(NG)
    elif Choice == "3" :
        Cr()
    elif Choice == "4" :
        Ex()

def New_Game() :
    Game.clear_terminal()
    User_Name = input("Entrez votre nom :\n> ")
    while len(User_Name.replace(" ","")) == 0 :
        Game.clear_terminal()
        print("Veuillez saisir un nom valide\n")
        User_Name = input("Entrez votre nom :\n> ")
    game = Game(User_Name)
    print("Le Jeux va commencer !")
    slp(1)
    Game.clear_terminal()
    game.start("Debut")

def Load_Game(NG) :
    with open('save.json',"r") as file :
        data = json.load(file)
        game = Game.create(data)
    restart = input(f"Voulez vous reprendre la partie avec le personnage \"{game.player.Name}\" ? (O/N) ")
    while restart.lower() not in ["o","n"] :
        print("Veuillez saisir une réponse valide (O/N) !")
        restart = input(f"Voulez vous reprendre la partie avec le personnage \"{game.player.Name}\" ? (O/N) ")
    Game.clear_terminal()
    if restart.lower() == "o" :
        game.start()
    elif restart.lower() == "n" :
        NG()


def Credits() :
    with open("Credits.JSON","r") as file :
        Credits_Txt = json.load(file)
    Game.clear_terminal()
    i = 1
    while i <= len(Credits_Txt["Credits"]) :
        print(Credits_Txt['Credits']["Part_" + str(i)])
        i +=1
        slp(1)
    slp(3)
    Main_Menu(New_Game,Load_Game,Credits,Exit)

def Exit():
    sys.exit()

Main_Menu(New_Game,Load_Game,Credits,Exit)

