# environment/rendering.py
import pygame

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)      # Agent
BROWN = (139, 69, 19)   # Waste
GRAY = (200, 200, 200)  # Grid lines

def draw_locate_waste_frame(env, screen, cell_size):
    """
    Draws a single frame of the LocateWasteEnv on the given screen.
    """
    width = cell_size * env.grid_size
    height = cell_size * env.grid_size
    screen.fill(WHITE)
    
    # Draw grid lines.
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, GRAY, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, GRAY, (0, y), (width, y))
    
    # Draw the waste as a brown square.
    wx, wy = env.waste_pos
    waste_rect = pygame.Rect(wx * cell_size + 20, wy * cell_size + 20, cell_size - 40, cell_size - 40)
    pygame.draw.rect(screen, BROWN, waste_rect)
    
    # Draw the agent as a blue circle.
    ax, ay = env.agent_pos
    agent_center = (ax * cell_size + cell_size // 2, ay * cell_size + cell_size // 2)
    pygame.draw.circle(screen, BLUE, agent_center, cell_size // 3)

def render_locate_waste_environment(env):
    """
    Runs a continuous loop that renders the current state of the LocateWasteEnv.
    Useful for quick debugging.
    """
    pygame.init()
    cell_size = 100
    grid_size = env.grid_size
    width = cell_size * grid_size
    height = cell_size * grid_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Locate Waste Environment")
    
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        draw_locate_waste_frame(env, screen, cell_size)
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
