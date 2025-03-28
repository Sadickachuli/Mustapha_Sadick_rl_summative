import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

GRID_SIZE = 5
CELL_SIZE = 100  
WINDOW_SIZE = GRID_SIZE * CELL_SIZE  

WHITE = (1, 1, 1)
BLACK = (0, 0, 0)
GREEN = (0, 1, 0)  
RED = (1, 0, 0)  
BLUE = (0, 0, 1)  

def draw_grid():
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    for i in range(GRID_SIZE + 1):
        glVertex2f(i * CELL_SIZE, 0)
        glVertex2f(i * CELL_SIZE, WINDOW_SIZE)
        glVertex2f(0, i * CELL_SIZE)
        glVertex2f(WINDOW_SIZE, i * CELL_SIZE)
    glEnd()

def draw_square(x, y, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x * CELL_SIZE, y * CELL_SIZE)
    glVertex2f((x + 1) * CELL_SIZE, y * CELL_SIZE)
    glVertex2f((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE)
    glVertex2f(x * CELL_SIZE, (y + 1) * CELL_SIZE)
    glEnd()

def render_scene(agent_pos, waste_pos, waste_type):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    draw_grid()
    waste_color = GREEN if waste_type == "recyclable" else RED
    draw_square(waste_pos[0], waste_pos[1], waste_color)
    draw_square(agent_pos[0], agent_pos[1], BLUE)

def init_opengl():
    glViewport(0, 0, WINDOW_SIZE, WINDOW_SIZE)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_SIZE, WINDOW_SIZE, 0, -1, 1)  
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
