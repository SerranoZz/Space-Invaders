from PPlay import collision
from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.collision import *
from PPlay.animation import *
from PPlay.sound import *
import modos
import random

class Jogador(object):
    def __init__(self, janela):
        self.janela = janela
        self.player = Sprite("Naves_and_enemy/player.png", 20)
        self.player.set_total_duration(2000)
        self.vidas = modos.vidas
        self.teclado = self.janela.get_keyboard()
        self.listatiros = []
        self.cronometroTiros = 0
        self.somtiro = Sound('Sound/tiro.ogg')
        self.set_pos()

    def set_pos(self):
        self.player.set_position(self.janela.width/2, self.janela.height - self.player.height)
    
    def _draw(self):
        self.player.draw()
        for i in range(len(self.listatiros)):
            self.listatiros[i].draw()
    
    def atira(self):
        tiro = Sprite("Naves_and_enemy/tiro.png")
        tiro.set_position(self.player.x + self.player.width/2 - tiro.width/2, self.player.y)
        self.listatiros.append(tiro)

    def atualizaTiros(self):
        for i in range(len(self.listatiros)):
            self.listatiros[i].move_y(self.janela.delta_time() * modos.frame *-10)
            if(self.listatiros[i].y <= 0):
                self.listatiros.pop(i)
                break

    def run(self):        
        self._draw()     
        #Andar
        if(self.teclado.key_pressed("LEFT")):
            if(self.player.x >= 0):
                self.player.x = self.player.x - modos.velplayer * self.janela.delta_time()
        if(self.teclado.key_pressed("RIGHT")):
            if((self.player.x + self.player.width) <= self.janela.width):
                self.player.x = self.player.x + modos.velplayer * self.janela.delta_time()
        
        #Atirar
        if(self.cronometroTiros >= modos.veltiro):
            if(self.teclado.key_pressed("UP")):
                self.atira()
                self.somtiro.play()
                self.cronometroTiros = 0
        self.cronometroTiros += self.janela.delta_time()

        #Mover os tiros e remover da lista
        self.atualizaTiros()
        self._draw()

class Invasores(object):
    def __init__(self, janela):
        self.janela = janela
        self.matrizInvasores = []
        self.listatiros = []
        self.jogador = Jogador(self.janela)
        self.aux = []
        self.Coluna = 6
        self.Linha = 3
        self.Invasores = self.Coluna * self.Linha
        self.direcaoInimigos = 1
        self.cronometroAvancar = 0
        self.cronometrotiros = 0
        self.spawn()

    def spawn(self):
        for i in range(self.Linha):
            k = random.randint(0, 2)
            l = random.randint(0, 5)
            self.matrizInvasores.append([])
            for j in range(self.Coluna):
                self.matrizInvasores[i].append(Sprite("Naves_and_enemy/enemy3.png"))
                self.matrizInvasores[i][j].set_position((j+1)* (self.janela.width/(self.janela.width/80)) + 760, (i+1)*65 - 55)
                if k == i and l == j:
                    self.matrizInvasores[i].pop(j)
                    self.matrizInvasores[k].append(Sprite("Naves_and_enemy/enemy2.png"))
                    self.matrizInvasores[k][l].set_position((j+1)* (self.janela.width/(self.janela.width/80)) + 760, (i+1)*65 - 55)
        

                        
    def moverInimigos(self): 
        if self.Invasores > 0:
            self.velocidade =  (self.janela.delta_time() * modos.velInvasores ) * self.direcaoInimigos + self.direcaoInimigos * modos.dificuldade/5 + self.direcaoInimigos * 3 / self.Invasores
        for i in range(len(self.matrizInvasores)):
            for j in range(len(self.matrizInvasores[i])):
                self.matrizInvasores[i][j].move_x(self.velocidade)
    
    def atirar(self):
        if self.cronometrotiros >= modos.veltiroinimigo:
            k = random.randint(0, self.Linha)
            l = random.randint(0, self.Coluna)
            for i in range(len(self.matrizInvasores)):
                for j in range(len(self.matrizInvasores[i])):
                    if k == i and l == j:
                        tiro = Sprite("Naves_and_enemy/tiro2.png")
                        tiro.set_position(self.matrizInvasores[i][j].x + self.matrizInvasores[i][j].width/2 - tiro.width/2, self.matrizInvasores[i][j].y)
                        self.listatiros.append(tiro)
                        self.cronometrotiros = 0
                        return
        else: self.cronometrotiros += self.janela.delta_time()
    
    def atualizaTiros(self):
        for i in range(len(self.listatiros)):
            self.listatiros[i].move_y(self.janela.delta_time() * modos.frame *10)
            if(self.listatiros[i].y <= 0):
                self.listatiros.pop(i)
                break
    
    def checarLimitesLaterais(self):
        for i in range(len(self.matrizInvasores)):
            for j in range(len(self.matrizInvasores[i])):
                if (self.matrizInvasores[i][j].x <= 0) or (self.matrizInvasores[i][j].x >= (self.janela.width - self.matrizInvasores[i][j].width)):
                    return True
        return False

    def avancarInimigos(self):
        if self.cronometroAvancar > 0.15:
            if self.checarLimitesLaterais():
                self.direcaoInimigos = -self.direcaoInimigos
                for i in range(len(self.matrizInvasores)):
                    for j in range(len(self.matrizInvasores[i])):
                        self.matrizInvasores[i][j].y += 60
                self.cronometroAvancar = 0
        else: self.cronometroAvancar += self.janela.delta_time()
    
    def _draw(self):
        for i in range(len(self.matrizInvasores)):
            for j in range(len(self.matrizInvasores[i])):
                self.matrizInvasores[i][j].draw()
        for i in range(len(self.listatiros)):
            self.listatiros[i].draw()
    
    def run(self):
        self.moverInimigos()
        self.avancarInimigos()
        self.atirar()
        self.atualizaTiros()
        self._draw()