from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.mouse import Mouse
import modos

class Menu(object):
    def __init__(self, janela):
        self.janela = janela
        self.play1 = Sprite("Buttons/PLAY1.png")
        self.play2 = Sprite("Buttons/PLAY2.png")
        self.options1 = Sprite("Buttons/OP1.png")
        self.options2 = Sprite("Buttons/OP2.png")
        self.lead1 = Sprite("Buttons/LEAD1.png")
        self.lead2 = Sprite("Buttons/LEAD2.png")
        self.quit1 = Sprite("Buttons/QUIT1.png")
        self.quit2 = Sprite("Buttons/QUIT2.png")
        self.mouse = Mouse()
        

    def set_pos(self):
        self.play1.set_position(5, self.janela.height/2)
        self.play2.set_position(5, self.janela.height/2)
        self.options1.set_position(5, self.janela.height/2 + self.play1.height)
        self.options2.set_position(5, self.janela.height/2 + self.play1.height)
        self.lead1.set_position(5, self.janela.height/2 + self.lead1.height + self.play1.height)
        self.lead2.set_position(5, self.janela.height/2 + self.lead1.height + self.play1.height)
        self.quit1.set_position(5, self.janela.height/2 + self.lead1.height + self.play1.height + self.lead1.height)
        self.quit2.set_position(5, self.janela.height/2 + self.lead1.height + self.play1.height + self.lead1.height)


    def _draw(self):
        self.play1.draw()
        self.options1.draw() 
        self.lead1.draw() 
        self.quit1.draw() 

    def run(self):
        self._draw()
        self.set_pos()
        if(self.mouse.is_over_object(self.play1)):
            self.play2.draw()
            if(self.mouse.is_button_pressed(1)):
                modos.modo = 1
            
        if(self.mouse.is_over_object(self.options1)):
            self.options2.draw()
            if(self.mouse.is_button_pressed(1)):
                modos.modo = 2
            
        if(self.mouse.is_over_object(self.lead1)):
            self.lead2.draw()
            if(self.mouse.is_button_pressed(1)):
                modos.modo = 3
            
        if(self.mouse.is_over_object(self.quit1)):
            self.quit2.draw()
            if(self.mouse.is_button_pressed(1)):
                modos.modo = 4
            
    
