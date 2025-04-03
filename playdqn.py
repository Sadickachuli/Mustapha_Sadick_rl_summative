# playdqn.py
import pygame
import time
from stable_baselines3 import DQN
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
    print(f"Episode {state.episode} finished:")
    print(f"   Total Reward: {state.total_reward:.2f}")
    print(f"   Steps: {state.steps}")
    print(f"   Average Reward per Step: {avg_reward:.2f}")
    print(f"   Episode Duration: {elapsed:.2f} seconds")
    print("-" * 60)

def simulate_trained_model(model_path):
    # Initialize Pygame and create the display
    pygame.init()
    window_size = 600
    screen = pygame.display.set_mode((window_size, window_size), pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption("Trained DQN Waste Collection Simulation")
    
    # Load environment and DQN model
    env = WasteCollectionEnv(grid_size=5, max_steps=100, render_mode='human')
    model = DQN.load(model_path)
    
    obs, _ = env.reset()
    clock = pygame.time.Clock()
    state = GameState()

    running = True
    while running:
        clock.tick(2)  # Control simulation speed

        # Process Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Get DQN model's action prediction
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, _ = env.step(action)

        # Update performance metrics
        state.total_reward += reward
        state.steps += 1

        # Render the environment state
        render_waste_env(env, screen)

        # Handle episode completion
        if terminated or truncated:
            log_episode(state)
            obs, _ = env.reset()
            state.episode += 1
            state.total_reward = 0.0
            state.steps = 0
            state.ep_start_time = time.time()
    
    pygame.quit()

if __name__ == '__main__':
    # Updated path to DQN model
    simulate_trained_model("models/dqn/dqn_final_model.zip")