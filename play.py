# play.py
import time
import pygame
import random
from environment.custom_env import WasteCollectionEnv

# Define colors (same as used in rendering.py)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)      # Agent color
BROWN = (139, 69, 19)   # Waste color
GREEN = (0, 255, 0)     # Bin color
GRAY = (200, 200, 200)  # Grid lines

def live_simulation():
    # Initialize environment
    env = WasteCollectionEnv()
    obs = env.reset()

    # Pygame display parameters
    cell_size = 100
    grid_size = env.grid_size
    width = cell_size * grid_size
    height = cell_size * grid_size

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Live Waste Collection Simulation")
    clock = pygame.time.Clock()

    running = True
    done = False

    while running:
        # Process pygame events (close window, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # For demonstration, we randomly sample an action.
        # You can later change this to use a trained model's prediction.
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        print(f"Action: {action}, Reward: {reward}")

        # Clear screen
        screen.fill(WHITE)
        
        # Draw grid lines
        for x in range(0, width, cell_size):
            pygame.draw.line(screen, GRAY, (x, 0), (x, height))
        for y in range(0, height, cell_size):
            pygame.draw.line(screen, GRAY, (0, y), (width, y))
        
        # Draw the bin (assumed to be at bottom right)
        bx, by = env.bin_pos
        bin_rect = pygame.Rect(bx * cell_size, by * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, GREEN, bin_rect)
        
        # Draw waste items
        for waste in env.waste_items:
            if waste['exists'] == 1:
                wx, wy = waste['pos']
                waste_rect = pygame.Rect(wx * cell_size + 20, wy * cell_size + 20, cell_size - 40, cell_size - 40)
                pygame.draw.rect(screen, BROWN, waste_rect)
        
        # Draw the agent
        ax, ay = env.agent_pos
        agent_center = (ax * cell_size + cell_size // 2, ay * cell_size + cell_size // 2)
        pygame.draw.circle(screen, BLUE, agent_center, cell_size // 3)
        
        pygame.display.flip()
        clock.tick(5)  # Adjust FPS for simulation speed (here, 5 frames per second)

        if done:
            # Pause for a moment to indicate end of episode, then reset environment.
            print("Episode finished. Resetting environment...\n")
            time.sleep(1)
            obs = env.reset()
            done = False

    pygame.quit()

if __name__ == '__main__':
    live_simulation()
