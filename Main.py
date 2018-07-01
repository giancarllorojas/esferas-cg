# coding=utf-8

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys

from Esfera import Esfera

NUMERO_ESFERAS = 5
TAMANHO_CUBO   = 2

esferas = []

rotacionaCubo  = False
rotacionaLado  = 1
telaHorizontal = 0.0
velocidadeRotacao = 1.5


def main():
    #Inicializa glut e cria janela
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(600,600)
    glutCreateWindow('Computacao Grafica 2018.1')


    glutDisplayFunc(display)
    glutIdleFunc(atualiza)
    glutMouseFunc(mouse)
    glutKeyboardFunc(teclado)

    inicializa()
    glutMainLoop()
    return

'''
Instancializa os objetos das esferas, a iluminação e a matriz de perspectiva
'''
def inicializa():
    global NUMERO_ESFERAS, TAMANHO_CUBO
    for i in range(NUMERO_ESFERAS):
        esferas.append(Esfera(esferas, TAMANHO_CUBO))

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glClearColor(1.0,1.0,1.0,1.0)

    # Prepara matriz de perspectiva
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0,1.0,1.0,10.0)
    glTranslatef(0.0,0.0,-4)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def atualiza():
    global rotacionaCubo, telaHorizontal, velocidadeRotacao

    for esfera in esferas:
        esfera.action()
    
    if rotacionaCubo:
        telaHorizontal += rotacionaLado*velocidadeRotacao
        if telaHorizontal>360.0:
            telaHorizontal -= 360.0

    glutPostRedisplay()

def teclado(botao, x, y):
    global esferas, TAMANHO_CUBO
    botao = botao.decode("utf-8") 
    if str(botao) == "+":
        esferas.append(Esfera(esferas, TAMANHO_CUBO))
        print("Esfera adicionada")
    if str(botao) == "-":
        esferas.pop()
        print("Esfera removida")

    if str(botao) == "a":
        for e in esferas:
            e.speedx *= 1.2
            e.speedy *= 1.2
            e.speedz *= 1.2

    if str(botao) == "d":
        for e in esferas:
            e.speedx *= 0.8
            e.speedy *= 0.8
            e.speedz *= 0.8

def mouse(botao,estado,x,y):
    global rotacionaCubo, rotacionaLado
    if botao == GLUT_LEFT_BUTTON:
        rotacionaLado = -1
        rotacionaCubo = not estado
    if botao == GLUT_RIGHT_BUTTON:
        rotacionaLado = 1
        rotacionaCubo = not estado
    elif botao == GLUT_MIDDLE_BUTTON:
        sys.exit(0)

def display():
    global telaHorizontal
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    # Rotaciona horizontalmente dado o parametro telaHorizontal que é mudado com o mouse
    glPushMatrix()
    glRotatef(telaHorizontal,0.0,1.0,0.0)

    #glRotatef(90.0,-1.0,0.0,0.0)
    glutWireCube(TAMANHO_CUBO)

    for esfera in esferas:
        esfera.desenha()

    glPopMatrix()
    glutSwapBuffers()

if __name__ == '__main__': 
    main()