from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import random

esferas = []

class Esfera:

    def __init__(self):
    #Cor aleatória
        self.color = [random.random(), random.random(), random.random()]

    #Posição aleatória
        self.x = random.randint(-3, 3)
        self.y = random.randint(-3, 3)
        self.z = 0

    #Velocidade aleatória
        self.speedx = random.random()
        self.speedy = 1 - self.speedx*self.speedx

    def action(self):
        if(self.x > 8):
            self.speedx = -self.speedx
            self.x = 8
        if(self.x < -8):
            self.speedx = -self.speedx
            self.x = -8
        if(self.y > 8):
            self.speedy = -self.speedy
            self.y = 8
        if(self.y < -8):
            self.speedy = -self.speedy
            self.y = -8
        self.x += self.speedx*0.3
        self.y += self.speedy*0.3

def main():

    #Inicializa glut e cria janela
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(400,400)
    glutCreateWindow('Computacao Grafica')

    #Configura background e modelos
    glClearColor(0.3,0.3,0.3,1.0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

    #Cria esferas
    numero_de_esferas = 5
    for i in range(numero_de_esferas):
        esferas.append(Esfera())


    #Iluminação
    glEnable(GL_LIGHTING)
    lightZeroPosition = [10.,4.,10.,1.]
    lightZeroColor = [0.8,1.0,0.8,1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)

    #Loop
    glutDisplayFunc(display)
    glutIdleFunc(display)

    #Camera
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40.,1.,1.,40.)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0,0,40,
              0,0,0,
              0,1,0)
    glPushMatrix()
    glutMainLoop()
    return

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    for esfera in esferas:
        glPushMatrix()

        esfera.action()
        glMaterialfv(GL_FRONT,GL_DIFFUSE,esfera.color)
        glTranslate(esfera.x, esfera.y, esfera.z)
        glutSolidSphere(1.3,60,60)
        #glTranslate(-esfera.x, -esfera.y, -esfera.z)

        glPopMatrix()
    glutSwapBuffers()
    return

if __name__ == '__main__': 
    main()