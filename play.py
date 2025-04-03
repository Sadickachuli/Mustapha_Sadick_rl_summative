# play.py
import pygame
import time
import random
from environment.custom_env import WasteCollectionEnv
from environment.rendering import render_waste_env

class GameState:
    def __init__(self):
        self.total_reward = 0.0
        self.steps = 0
        self.episode = 1
        self.ep_start_time = time.time()

def log_episode(state):
    elapsed = time.time() - state.ep_start_time
    avg_reward = state.total_reward / state.steps if state.steps > 0 else 0
    summary = (
        f"Episode {state.episode} finished: Total Reward: {state.total_reward:.2f} | "
        f"Steps: {state.steps} | Average Reward per Step: {avg_reward:.2f} | "
        f"Episode Duration: {elapsed:.2f} seconds"
    )
    print(summary)
    print("-" * 60)
    return summary

def play():
    pygame.init()
    window_size = 600
    # Use OPENGL and DOUBLEBUF for rendering
    screen = pygame.display.set_mode((window_size, window_size), pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption("Random Movement Simulation")
    
    # Create environment with render_mode 'human'
    env = WasteCollectionEnv(grid_size=5, max_steps=100, render_mode='human')
    obs, _ = env.reset()
    clock = pygame.time.Clock()
    
    state = GameState()

    running = True
    while running:
        clock.tick(2) 
        
        # Process Pygame events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Randomly choose an action (0-3 for movement, 4 for pickup/drop)
        action = random.choice([0, 1, 2, 3, 4])
        obs, reward, terminated, truncated, _ = env.step(action)
        state.total_reward += reward
        state.steps += 1

        # Render the environment with the log bar overlay.
        render_waste_env(env, screen)

        # Check for episode end.
        if terminated or truncated:
            summary = log_episode(state)
            obs, _ = env.reset()
            state.episode += 1
            state.total_reward = 0.0
            state.steps = 0
            state.ep_start_time = time.time()
        
    pygame.quit()

if __name__ == '__main__':
    play()
