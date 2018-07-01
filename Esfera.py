from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import random
import math
import numpy as np

        
# Objeto para a esfera
class Esfera:
    def __init__(self, esferas, tamanho_cubo):
        # lista com todas as esferas
        self.esferas = esferas

        #Cor aleatória
        self.color = [random.random(), random.random(), random.random()]
    
        #Raio aleatório
        self.raio  = random.uniform(0.1, 0.2)

        #Fronteiras do cubo
        self.max   = (tamanho_cubo/2) - (self.raio)
        self.min   = -self.max

        #Posição aleatória
        self.x      = random.uniform(self.min, self.max)
        self.y      = random.uniform(self.min, self.max)
        self.z      = random.uniform(self.min, self.max)

        #Colisões recentes
        self.colididos = []
            
        self.massa  = self.raio*2
        

        #Velocidade aleatória
        self.speedx = random.uniform(0,0.05)
        self.speedy = random.uniform(0,0.05)
        self.speedz = random.uniform(0,0.05)

    '''
    Checa para testar se a esfera está nos limites do cubo
    '''
    def checa_limites(self):
        if(self.x > self.max):
            self.speedx *= -1
            self.x = self.max
        if(self.x < self.min):
            self.speedx *= -1
            self.x = self.min

        if(self.y > self.max):
            self.speedy *= -1
            self.y = self.max
        if(self.y < self.min):
            self.speedy *= -1
            self.y = self.min

        if(self.z > self.max):
            self.speedz *= -1
            self.z = self.max
        if(self.z < self.min):
            self.speedz *= -1
            self.z = self.min
    
    def action(self):
        self.checa_limites()
        self.checa_colisoes()

        self.x += self.speedx
        self.y += self.speedy
        self.z += self.speedz

    # Implementação da ideia descrita aqui:
    # https://www.gamasutra.com/view/feature/131424/pool_hall_lessons_fast_accurate_.php?page=3
    def responde_colisao(self, e2):
        r1 = np.array([self.x, self.y, self.z])
        r2 = np.array([e2.x, e2.y, e2.z])

        v1 = np.array([self.speedx, self.speedy, self.speedz])
        v2 = np.array([e2.speedx, e2.speedy, e2.speedz])

        normal = (r1 - r2)/np.linalg.norm((r1 - r2))

        a1 = np.dot(v1, normal)
        a2 = np.dot(v2, normal)

        optP = 2*(a1 - a2)/(self.massa + e2.massa)

        nv1 = v1 - optP*e2.massa*normal
        nv2 = v2 + optP*self.massa*normal

        self.altera_velocidade(nv1)
        e2.altera_velocidade(nv2)

    def altera_velocidade(self, vetor_velocidade):
        self.speedx = vetor_velocidade[0]
        self.speedy = vetor_velocidade[1]
        self.speedz = vetor_velocidade[2]


    def checa_colisoes(self):
        for e in self.esferas:
            if(e != self): # Compara apenas com as outras esferas
                distance = abs(math.sqrt(((e.x - self.x)**2) + ((e.y - self.y)**2) + ((e.z - self.z)**2))) # Calcula a distância entre os centros das esferas

                if((e not in self.colididos) and (distance < (e.raio + self.raio) - 0.1)): # Se a distancia entre os centros é menor que a soma dos raios, então houve uma colisão
                    self.colididos.append(e)
                    e.colididos.append(self)
                    self.responde_colisao(e)
                
                if((e in self.colididos) and (distance > (e.raio + self.raio) - 0.1)):
                    self.colididos.remove(e)
                    e.colididos.remove(self)

    '''
    Desenha a esfera na posicao atual
    '''
    def desenha(self):
        glPushMatrix()
        glMaterialfv(GL_FRONT,GL_DIFFUSE,self.color)
        glTranslate(self.x, self.y, self.z)
        glutSolidSphere(self.raio, 30, 30)
        glPopMatrix()


'''
@deprecated
Função para calcular o angulo entre duas esferas
método: 
1. Achar o plano tangente as esferas usando o ponto central da esfera e a velocidade como vetor normal
2. Calcular o ângulo diedro(angulo entre os planos)


Acabamos não usando essa função porque fomos por outro método para calcular a nova velocidade após colisão
'''
def calcula_angulo_entre_esferas(e1, e2):
    #print("e1: " + str(e1.x) + " " + str(e1.y) + " " + str(e1.z) + " e2: " + str(e2.x) + " " + str(e2.y) + " " + str(e2.z))

    coef = abs((e1.x*e2.x) + (e1.y*e2.y) + (e1.z*e2.z))
    num  = math.sqrt((e1.x**2) + (e1.y**2) + (e1.z**2)) * math.sqrt((e2.x**2) + (e2.y**2) + (e2.z**2))
    cos  = coef/num

    print(str(coef) + " - " + str(num) + " - " + str(cos))

    return math.acos(cos)

'''
Funçao antiga que usamos numa tentativa de otimizar o custo, mas deixamos pra lá
'''
def check_colissions(esferas):
    remaining_spheres = esferas.copy()
    for e1 in esferas:
        for e2 in remaining_spheres:
            if(e1 != e2): # Compara apenas com as outras esferas
                distance = math.sqrt(((e2.x - e1.x)**2) + ((e2.y - e1.y)**2) + ((e2.z - e1.z)**2)) # Calcula a distância entre os centros das esferas

                if(distance < (e2.raio + e1.raio)): # Se a distancia entre os centros é menor que a soma dos raios, então houve uma colisão
                    e1.invert_speed(e2)
                    e2.invert_speed(e1)

        remaining_spheres.pop()