from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
import modos

class Lead(object):
    def __init__(self, janela):
        self.janela = janela
        self.teclado = janela.get_keyboard()
        self.fundo = GameImage("Background/LEAD.jpg")

    
    def run(self):
        self.fundo.draw()
        arq = open('ranking.txt','r')
        conteudo = arq.readlines()
        nomes=[]
        pontos=[]
        difficulty = []
        for i in range(len(conteudo)):
            linha=conteudo[i].split('/')
            nomes.append(linha[0])
            difficulty.append(linha[1])
            pontos.append(int(linha[2].rstrip('\n')))
        arq.close()
        
        for j in range(10):
            for i in range(len(pontos)-1):
                if pontos[i] < pontos[i+1]:
                    pontos[i+1],pontos[i]=pontos[i],pontos[i+1]
                    nomes[i+1],nomes[i]=nomes[i],nomes[i+1]
                    difficulty[i+1],difficulty[i]=difficulty[i],difficulty[i+1]

        for i in range(len(nomes)):
            if i == 10:
                break
            self.janela.draw_text('{} - Name: {} / Difficulty: {} / Score: {}'.format(i+1, nomes[i], difficulty[i], pontos[i]), self.janela.width/2 - 270, (self.janela.height/2 - 150) + i*50, size=32, color=(0, 0, 0), font_name="")
        
        if(self.teclado.key_pressed("ESC")):
            modos.modo = 0 
