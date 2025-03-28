import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *  # For drawing text

GRID_SIZE = 5
CELL_SIZE = 100  
WINDOW_SIZE = GRID_SIZE * CELL_SIZE  

WHITE = (1, 1, 1)
BLACK = (0, 0, 0)

# Texture placeholders
agent_texture = None  
recyclable_texture = None  
non_recyclable_texture = None  
recyclable_bin_texture = None
nonrecyclable_bin_texture = None

def load_texture(path, scale_factor=0.7):
    """Loads a texture from an image file, resizes it, and flips it for OpenGL."""
    image = pygame.image.load(path)
    new_size = (int(CELL_SIZE * scale_factor), int(CELL_SIZE * scale_factor))
    image = pygame.transform.scale(image, new_size)
    image = pygame.transform.flip(image, False, True)  # Flip vertically for OpenGL
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
    glColor3f(1, 1, 1)  # Reset color to white

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
        agent_texture = load_texture("agent.png")
    draw_texture(x, y, agent_texture)

def draw_waste(x, y, waste_type):
    """Draws the waste emoji based on its type."""
    global recyclable_texture, non_recyclable_texture
    if recyclable_texture is None:
        recyclable_texture = load_texture("recyclable.png")
    if non_recyclable_texture is None:
        non_recyclable_texture = load_texture("non-recyclable.png")
    texture = recyclable_texture if waste_type == "recyclable" else non_recyclable_texture
    draw_texture(x, y, texture)

def draw_bin(x, y, bin_type):
    """Draws a bin at (x, y) based on its type."""
    global recyclable_bin_texture, nonrecyclable_bin_texture
    if bin_type == "recyclable":
        if recyclable_bin_texture is None:
            recyclable_bin_texture = load_texture("recycle-bin.png", scale_factor=1.0)
        texture = recyclable_bin_texture
    else:
        if nonrecyclable_bin_texture is None:
            nonrecyclable_bin_texture = load_texture("nonrecycle-bin.png", scale_factor=1.0)
        texture = nonrecyclable_bin_texture
    draw_texture(x, y, texture)

def draw_text(x, y, text_string):
    """Draws text using GLUT bitmap fonts."""
    glColor3f(1, 1, 1)
    glWindowPos2f(x, y)
    for ch in text_string:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

def render_scene(agent_pos, waste_pos, waste_type, holding, bin_positions, total_reward, episode_end):
    """
    Renders the entire scene:
      - Draws the grid.
      - Draws the bins at their fixed positions.
      - If the agent is not holding waste, draws the waste.
      - Draws the agent.
      - Draws a scoreboard at the top showing the total reward and, if applicable, an "Episode Ended" message.
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    draw_grid()
    # Draw bins at fixed positions
    draw_bin(bin_positions["recyclable"][0], bin_positions["recyclable"][1], "recyclable")
    draw_bin(bin_positions["non-recyclable"][0], bin_positions["non-recyclable"][1], "non-recyclable")
    
    # Draw the waste only if the agent is not holding it
    if not holding:
        draw_waste(waste_pos[0], waste_pos[1], waste_type)
    
    draw_emoji(agent_pos[0], agent_pos[1])
    
    # Draw the scoreboard at the top of the window
    draw_text(10, 20, f"Total Reward: {total_reward}")
    if episode_end:
        draw_text(10, 40, "Episode Ended")

def init_opengl():
    """Initializes OpenGL settings."""
    glViewport(0, 0, WINDOW_SIZE, WINDOW_SIZE)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_SIZE, WINDOW_SIZE, 0, -1, 1)  
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # Initialize GLUT (needed for text rendering)
    glutInit()
