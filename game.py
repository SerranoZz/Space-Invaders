from PPlay.sprite import *
from PPlay.animation import *
from PPlay.window import *
from player_and_enemy import Jogador, Invasores
from PPlay.collision import *
from PPlay.sound import *
import random
import modos



class Game(object):
    def __init__(self, janela):
        self.janela = janela
        self.nivel = 1
        self.teclado = janela.get_keyboard()
        self.jogador = Jogador(self.janela)
        self.invasores = Invasores(self.janela)
        self.tempo = 0
        self.pontuacao = 0
        self.FPS = 0
        self.fpsAtual = 0
        self.cronometroFPS = 0
        self.fundo1 = Sprite("Background/fundo.jpg")
        self.fundo2 = Sprite("Background/fundo.jpg")
        self.som_morte_invasor = Sound("Sound/morteinimigo.ogg")
        self.gameoverimg = Sprite("Background/go.png")
        self.gameoverimg.set_position(self.janela.width/2 , self.janela.height/2)
        self.vivo = True
        self.cronometroMorte = 2
        
      

    def colisaoTiroInimigo(self): 
        for i in range(len(self.jogador.listatiros)):
            for j in range(len(self.invasores.matrizInvasores)):
                for k in range(len(self.invasores.matrizInvasores[j])):
                    if(Collision.collided(self.jogador.listatiros[i], self.invasores.matrizInvasores[j][k])):
                        self.som_morte_invasor.play()
                        self.pontuacao += 50 + 50 / self.tempo
                        self.invasores.matrizInvasores[j].pop(k)
                        self.jogador.listatiros.pop(i)
                        if(len(self.invasores.matrizInvasores[j])) == 0:
                            self.invasores.matrizInvasores.pop(j)
                        self.invasores.Invasores -= 1
                        return

    def respawn(self):
        self.jogador.player.set_position(self.janela.width/2, self.janela.height - self.jogador.player.height)


    def colisaoTiroPlayer(self):
        if(self.cronometroMorte >= 2):
            for i in range(len(self.invasores.listatiros)):
                if Collision.collided(self.invasores.listatiros[i], self.jogador.player):
                    self.jogador.vidas -= 1
                    self.invasores.listatiros.pop(i)
                    self.cronometroMorte = 0
                    if self.jogador.vidas != 0:
                        self.respawn()
                    break
        else: self.cronometroMorte += self.janela.delta_time()
    
    def passarNivel(self):
        self.pontuacao += self.nivel * 1000
        self.nivel += 1
        modos.velInvasores += 20
        modos.veltiroinimigo -= 0.1
        modos.veltiro += 0.1
        modos.velplayer -= 10
        self.invasores.Coluna += 1
        self.invasores.Linha += 1
        self.invasores.direcaoInimigos = 1
        if self.invasores.Coluna > self.janela.width/60 - 1:
            self.invasores.Coluna = int(self.janela.width/60 - 1)
        if self.invasores.Linha > self.janela.height/60 - 2:
            self.invasores.Linha = int(self.janela.height/60-2)
        self.jogador.listatiros.clear()
        self.invasores.listatiros.clear()
        self.tempo = 0
        self.invasores.spawn()
        self.invasores.Invasores = self.invasores.Coluna * self.invasores.Linha

    def reset(self):
        self.nivel = 1
        self.pontuacao = 0
        self.vivo = True
        self.invasores = Invasores(self.janela)
        self.jogador = Jogador(self.janela)
        self.cronometroMorte = 2

    def checarGameOverY(self):
        for i in range(len(self.invasores.matrizInvasores)):
            for j in range(len(self.invasores.matrizInvasores[i])):
                if(self.invasores.matrizInvasores[i][j].y + self.invasores.matrizInvasores[i][j].height >= self.jogador.player.y):
                    return True
        return False
    
    def gameOver(self):    
        self.janela.draw_text("GAME OVER", self.janela.width/2 , self.janela.height/2, size=500, color=(255,255,255), font_name="Minecraft")    
        arq = open('ranking.txt','r')
        conteudo = arq.readlines()
        nome = input('Digite seu nome: ')
        linha = nome + '/' + str(modos.texto) + '/' + str(int(self.pontuacao)) + '\n'
        conteudo.append(linha)
        arq.close()
        arq = open('ranking.txt', 'w')
        arq.writelines(conteudo)
        arq.close()
        print('Ranking atualizado com sucesso')
        self.reset()
        modos.modo = 3
        
    def scrolling(self): 
        self.fundo1.y += 100 * self.janela.delta_time()
        self.fundo2.y += 100 * self.janela.delta_time()
    
        if self.fundo2.y >= 0:
            self.fundo1.y = 0
            self.fundo2.y = -self.fundo2.height
    
        self.fundo1.draw()
        self.fundo2.draw()
        
    def run(self):
        #Controle de FPS
        self.cronometroFPS += self.janela.delta_time()
        self.FPS += 1
        if self.cronometroFPS > 1: 
            self.fpsAtual = self.FPS   
            self.FPS = 0
            self.cronometroFPS = 0
    
        if self.vivo:
            if self.invasores.Invasores == 0:
                self.passarNivel() 
            self.scrolling()
            self.invasores.run()
            self.jogador.run()
            self.colisaoTiroInimigo()
            self.colisaoTiroPlayer()

            self.tempo += self.janela.delta_time()
            
            if(self.teclado.key_pressed("ESC")):
                modos.modo = 0
                self.reset()

            if self.checarGameOverY() or self.jogador.vidas == 0:
                self.nivel = 1
                self.vivo = False
                self.gameOver()
    


        #Draw na tela
        self.janela.draw_text("FPS: "+str(self.fpsAtual), 0, 0, size=28, color=(255,255,255), font_name="Minecraft")
        self.janela.draw_text("Difficulty: " + str(modos.texto), self.janela.width - 172, 5, size=28, color=(255,255,255), font_name="Minecraft")
        self.janela.draw_text("Nivel: " + str(self.nivel), self.janela.width - 172, 30, size=28, color=(255,255,255), font_name="Minecraft")
        self.janela.draw_text("Score: " + str(int(self.pontuacao)), self.janela.width - 172, 55, size=28, color=(255,255,255), font_name="Minecraft")
        self.janela.draw_text("Life: " + str(int(self.jogador.vidas)), self.janela.width - 172, 80, size=28, color=(255,255,255), font_name="Minecraft")
      
        if self.cronometroMorte < 2:
                self.jogador.player.draw()
                self.jogador.player.update()
        else: 
            self.jogador.player.set_curr_frame(0)


            
    
