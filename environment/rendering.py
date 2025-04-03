# environment/rendering.py
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Color definitions 
COLORS = {
    'background': (1.0, 1.0, 1.0),              # White background
    'cell': (0.4, 0.2, 0.7),                    # Light purple cells
    'grid': (0.8, 0.7, 0.9), 
    'agent_body': (0.0, 0.0, 1.0),              # Blue agent body
    'agent_head': (1.0, 1.0, 0.90),          
    'waste': (0.55, 0.27, 0.07)                 
}

# Global variable for bin texture
BIN_TEXTURE = None

def load_texture(image_path):
    """Loads an image as an OpenGL texture without flipping it, and with transparency enabled."""
    img = pygame.image.load(image_path) 
    img = img.convert_alpha()       
    img_data = pygame.image.tostring(img, "RGBA", True)
    width, height = img.get_size()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Set texture parameters for wrapping and filtering
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return texture_id

def draw_textured_rect(x, y, w, h, texture):
    """Draws a rectangle with the given texture and enables alpha blending."""
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    
    # Enable alpha blending
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glColor3f(1, 1, 1) 
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y)
    glTexCoord2f(1, 0); glVertex2f(x + w, y)
    glTexCoord2f(1, 1); glVertex2f(x + w, y + h)
    glTexCoord2f(0, 1); glVertex2f(x, y + h)
    glEnd()
    
    glDisable(GL_BLEND)
    glDisable(GL_TEXTURE_2D)

def draw_filled_rect(x, y, w, h, color):
    """Draws a filled rectangle."""
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x+w, y)
    glVertex2f(x+w, y+h)
    glVertex2f(x, y+h)
    glEnd()

def draw_circle(cx, cy, radius, color, segments=32):
    """Draws a filled circle."""
    glColor3f(*color)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(cx, cy)
    for i in range(segments+1):
        angle = 2 * math.pi * i / segments
        glVertex2f(cx + math.cos(angle) * radius, cy + math.sin(angle) * radius)
    glEnd()

def render_waste_env(env, screen):
    """
    Renders the environment onto the provided 'screen'.
    Assumes that 'screen' has already been created (e.g., via pygame.display.set_mode).
    """
    global BIN_TEXTURE
    if BIN_TEXTURE is None:
        BIN_TEXTURE = load_texture("images/recycle-bin.png")  

    window_size = screen.get_width()  
    cell_size = window_size / env.grid_size

    # Clear the buffer with the background color.
    glClearColor(*COLORS['background'], 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluOrtho2D(0, env.grid_size, 0, env.grid_size)

    # Drawing cells
    for i in range(env.grid_size):
        for j in range(env.grid_size):
            draw_filled_rect(i, j, 1, 1, COLORS['cell'])
    
    # Drawing grid lines.
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

    # drawing bin 
    bx, by = env.bin_pos
    draw_textured_rect(bx + 0.1, by + 0.1, 0.8, 0.8, BIN_TEXTURE)

    # drawing waste 
    if not env.carrying_waste:
        wx, wy = env.waste_pos
        draw_circle(wx + 0.5, wy + 0.5, 0.35, COLORS['waste'])
    
    # Drawing agent
    ax, ay = env.agent_pos
    draw_filled_rect(ax + 0.2, ay + 0.1, 0.6, 0.6, COLORS['agent_body'])
    draw_circle(ax + 0.5, ay + 0.75, 0.2, COLORS['agent_head']) 
    
    pygame.display.flip()
    pygame.time.wait(100)
