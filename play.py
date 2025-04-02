# play.py
import pygame
import time
import random
from environment.custom_env import WasteCollectionEnv

def play():
    # Create the environment with render_mode enabled so it uses OpenGL rendering.
    env = WasteCollectionEnv(grid_size=5, max_steps=100, render_mode='human')
    obs, _ = env.reset()
    
    # Initialize Pygame (required for handling events)
    pygame.init()
    running = True
    clock = pygame.time.Clock()

    while running:
        # Process Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # For this test, only use movement actions (0: up, 1: down, 2: left, 3: right)
        action = random.choice([0, 1, 2, 3])
        obs, reward, terminated, truncated, _ = env.step(action)
        
        # Call the environment's render function (which uses OpenGL)
        env.render()

        # If the episode ends (due to termination or max steps), reset the environment
        if terminated or truncated:
            print("Episode finished. Resetting environment...")
            time.sleep(1)
            obs, _ = env.reset()
        
        # Control simulation speed (adjust FPS as needed)
        clock.tick(2)  # e.g., 2 FPS for clear visualization

    pygame.quit()

if __name__ == '__main__':
    play()