# environment/rendering.py
import pygame

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)      # Agent
BROWN = (139, 69, 19)   # Waste
GREEN = (0, 255, 0)     # Bin
GRAY = (200, 200, 200)  # Grid lines

def render_environment(env):
    pygame.init()
    
    # Set up display parameters.
    cell_size = 100
    grid_size = env.grid_size
    width = cell_size * grid_size
    height = cell_size * grid_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Waste Collection Environment")
    
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(WHITE)
        
        # Draw grid lines.
        for x in range(0, width, cell_size):
            pygame.draw.line(screen, GRAY, (x, 0), (x, height))
        for y in range(0, height, cell_size):
            pygame.draw.line(screen, GRAY, (0, y), (width, y))
        
        # Draw the bin.
        bx, by = env.bin_pos
        bin_rect = pygame.Rect(bx * cell_size, by * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, GREEN, bin_rect)
        
        # Draw waste items.
        for waste in env.waste_items:
            if waste['exists'] == 1:
                wx, wy = waste['pos']
                waste_rect = pygame.Rect(wx * cell_size + 20, wy * cell_size + 20, cell_size - 40, cell_size - 40)
                pygame.draw.rect(screen, BROWN, waste_rect)
        
        # Draw the agent.
        ax, ay = env.agent_pos
        agent_center = (ax * cell_size + cell_size // 2, ay * cell_size + cell_size // 2)
        pygame.draw.circle(screen, BLUE, agent_center, cell_size // 3)
        
        pygame.display.flip()
        clock.tick(30)  # Limit to 30 FPS
    
    pygame.quit()
