from PPlay.gameimage import*
from PPlay.window import Window
from menu import Menu
from game import Game
from options import Options1
from lead import Lead 
import modos


janela = Window(1920, 1080)
janela.set_title("Space Invaders")
fundo = GameImage("Background/MENU1.jpg")

menu = Menu(janela)
game = Game(janela)
options = Options1(janela)
lead = Lead(janela)


while(modos.modo != 4):
    fundo.draw()

    if modos.modo == 0:
        menu.run()
    elif modos.modo == 1:
        game.run()
    elif modos.modo == 2:
        options.run()
    elif modos.modo == 3: 
        lead.run()

    janela.update()