# play.py
import time
import pygame
from environment.custom_env import LocateWasteEnv
from environment.rendering import draw_locate_waste_frame

def play():
    # Create the simplified environment.
    env = LocateWasteEnv(grid_size=5, max_steps=50)
    obs, _ = env.reset()
    
    # Set up pygame display.
    pygame.init()
    cell_size = 100
    grid_size = env.grid_size
    width = cell_size * grid_size
    height = cell_size * grid_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Play: Locate Waste Environment (Random Policy)")
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # For demonstration, take a random action.
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        
        # Draw current frame.
        draw_locate_waste_frame(env, screen, cell_size)
        pygame.display.flip()
        clock.tick(5)  # Slow down the simulation for visualization.
        
        # If episode finished, reset the environment.
        if terminated or truncated:
            print("Episode finished. Resetting environment...")
            time.sleep(1)
            obs, _ = env.reset()
    
    pygame.quit()

if __name__ == '__main__':
    play()
