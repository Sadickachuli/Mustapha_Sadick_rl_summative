# environment/rendering.py
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# New color definitions in normalized RGB (0-1)
COLORS = {
    'background': (1.0, 1.0, 1.0),              
    'cell': (0.4, 0.2, 0.7),                 
    'grid': (0.8, 0.7, 0.9), 
    'agent': (0.68, 0.85, 0.90),  
    'waste': (0.55, 0.27, 0.07),           
    'bin': (0.0, 1.0, 0.0)                    
}

def draw_filled_rect(x, y, w, h, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x+w, y)
    glVertex2f(x+w, y+h)
    glVertex2f(x, y+h)
    glEnd()

def draw_circle(cx, cy, radius, color, segments=32):
    glColor3f(*color)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(cx, cy)
    for i in range(segments+1):
        angle = 2 * math.pi * i / segments
        glVertex2f(cx + math.cos(angle) * radius, cy + math.sin(angle) * radius)
    glEnd()

def render_waste_env(env):
    # Set window size based on grid size. Here we use 600x600.
    window_size = 600
    cell_size = window_size / env.grid_size

    pygame.init()
    # Use double buffering with OpenGL
    screen = pygame.display.set_mode((window_size, window_size), pygame.OPENGL | pygame.DOUBLEBUF)
    
    glClearColor(*COLORS['background'], 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluOrtho2D(0, env.grid_size, 0, env.grid_size)

    # Draw cells: fill each cell with light purple.
    for i in range(env.grid_size):
        for j in range(env.grid_size):
            draw_filled_rect(i, j, 1, 1, COLORS['cell'])
    
    # Draw grid lines
    glColor3f(*COLORS['grid'])
    glLineWidth(2)
    glBegin(GL_LINES)
    for i in range(env.grid_size + 1):
        glVertex2f(i, 0)
        glVertex2f(i, env.grid_size)
    for j in range(env.grid_size + 1):
        glVertex2f(0, j)
        glVertex2f(env.grid_size, j)
    glEnd()

    # Draw bin as a square (green)
    bx, by = env.bin_pos
    draw_filled_rect(bx + 0.1, by + 0.1, 0.8, 0.8, COLORS['bin'])

    # Draw waste as a circle (brown) if not carried
    if not env.carrying_waste:
        wx, wy = env.waste_pos
        # Draw waste circle in center of cell with radius 0.35
        draw_circle(wx + 0.5, wy + 0.5, 0.35, COLORS['waste'])
    
    # Draw agent as a circle (light blue)
    ax, ay = env.agent_pos
    draw_circle(ax + 0.5, ay + 0.5, 0.35, COLORS['agent'])
    
    pygame.display.flip()
    # Wait a short time to let the frame show
    pygame.time.wait(100)
