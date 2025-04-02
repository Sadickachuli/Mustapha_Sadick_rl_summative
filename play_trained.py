# play_trained.py
import pygame
from stable_baselines3 import PPO
from environment.custom_env import WasteCollectionEnv

def simulate_trained_model(model_path):
    env = WasteCollectionEnv(grid_size=5, max_steps=100, render_mode='human')
    model = PPO.load(model_path)
    
    obs, _ = env.reset()
    terminated = False
    clock = pygame.time.Clock()  # Add pygame clock
    
    while True:
        # Control rendering speed
        clock.tick(2)  # Set to 5 FPS (adjust this number as needed)
        
        action, _ = model.predict(obs, deterministic=True)
        obs, _, terminated, _, _ = env.step(action)
        
        env.render()
        
        if terminated:
            obs, _ = env.reset()
        
        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == '__main__':
    simulate_trained_model("models/pg/ppo_collection.zip")