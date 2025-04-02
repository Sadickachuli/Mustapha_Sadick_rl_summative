# play.py
import pygame
import time
import random
from environment.custom_env import WasteCollectionEnv
from environment.rendering import render_waste_env

def play():
    pygame.init()
    window_size = 600
    screen = pygame.display.set_mode((window_size, window_size), pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption("Random Movement Simulation")
    
    env = WasteCollectionEnv(grid_size=5, max_steps=100, render_mode='human')
    obs, _ = env.reset()
    clock = pygame.time.Clock()
    
    running = True
    while running:
        clock.tick(2)  # Adjust FPS as needed
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Randomly choose a movement action (0-3)
        action = random.choice([0, 1, 2, 3])
        obs, reward, terminated, truncated, _ = env.step(action)
        
        render_waste_env(env, screen)
        
        if terminated or truncated:
            print("Episode finished. Resetting environment...")
            time.sleep(1)
            obs, _ = env.reset()
        
    pygame.quit()

if __name__ == '__main__':
    play()
