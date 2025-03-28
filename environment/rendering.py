import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

GRID_SIZE = 5
CELL_SIZE = 100  
WINDOW_SIZE = GRID_SIZE * CELL_SIZE  

WHITE = (1, 1, 1)
BLACK = (0, 0, 0)

# Texture placeholders
agent_texture = None  
recyclable_texture = None  
non_recyclable_texture = None  

def load_texture(path, scale_factor=0.7):
    """Loads a texture from an image file, resizes it, and flips it for OpenGL."""
    image = pygame.image.load(path)
    
    # Compute new dimensions
    new_size = (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor))
    image = pygame.transform.scale(image, new_size)  # Resize the image
    image = pygame.transform.flip(image, False, True)  # Flip for OpenGL format
    image_data = pygame.image.tostring(image, "RGBA", True)
    
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(),
                 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    
    return texture_id

def draw_grid():
    """Draws the grid lines in OpenGL."""
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    for i in range(GRID_SIZE + 1):
        glVertex2f(i * CELL_SIZE, 0)
        glVertex2f(i * CELL_SIZE, WINDOW_SIZE)
        glVertex2f(0, i * CELL_SIZE)
        glVertex2f(WINDOW_SIZE, i * CELL_SIZE)
    glEnd()

def draw_texture(x, y, texture):
    """Draws a textured square at (x, y) using OpenGL."""
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    glColor3f(1, 1, 1)  # Reset color to white to avoid tinting

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x * CELL_SIZE, y * CELL_SIZE)
    glTexCoord2f(1, 0); glVertex2f((x + 1) * CELL_SIZE, y * CELL_SIZE)
    glTexCoord2f(1, 1); glVertex2f((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE)
    glTexCoord2f(0, 1); glVertex2f(x * CELL_SIZE, (y + 1) * CELL_SIZE)
    glEnd()
    
    glDisable(GL_TEXTURE_2D)

def draw_emoji(x, y):
    """Draws the agent emoji."""
    global agent_texture
    if agent_texture is None:
        agent_texture = load_texture("emoji.png")  

    draw_texture(x, y, agent_texture)

def draw_waste(x, y, waste_type):
    """Draws the waste as an emoji based on its type."""
    global recyclable_texture, non_recyclable_texture

    if recyclable_texture is None:
        recyclable_texture = load_texture("recyclable.png")
    if non_recyclable_texture is None:
        non_recyclable_texture = load_texture("non-recyclable.png")

    waste_texture = recyclable_texture if waste_type == "recyclable" else non_recyclable_texture
    draw_texture(x, y, waste_texture)

def render_scene(agent_pos, waste_pos, waste_type):
    """Renders the grid, waste, and agent."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    draw_grid()
    draw_waste(waste_pos[0], waste_pos[1], waste_type)  # Render waste as an emoji
    draw_emoji(agent_pos[0], agent_pos[1])  # Render agent as an emoji

def init_opengl():
    """Initializes OpenGL settings."""
    glViewport(0, 0, WINDOW_SIZE, WINDOW_SIZE)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_SIZE, WINDOW_SIZE, 0, -1, 1)  
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
