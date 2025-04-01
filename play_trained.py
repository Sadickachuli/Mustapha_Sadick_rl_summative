# play_trained.py
import time
import pygame
from stable_baselines3 import PPO
from environment.custom_env import WasteCollectionEnv

def simulate_trained_model(model_path):
    # Create the environment and load the trained model.
    env = WasteCollectionEnv()
    model = PPO.load(model_path)
    
    # Reset the environment and unpack the observation and info.
    obs, _ = env.reset()

    # Define display parameters.
    cell_size = 100
    grid_size = env.grid_size
    width = cell_size * grid_size
    height = cell_size * grid_size

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Trained Model Simulation")
    clock = pygame.time.Clock()

    running = True
    done = False

    while running:
        # Check for window events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Predict action using the trained model (deterministic).
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        print(f"Action: {action}, Reward: {reward}")

        # Clear the screen.
        screen.fill((255, 255, 255))
        
        # Draw grid lines.
        for x in range(0, width, cell_size):
            pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, height))
        for y in range(0, height, cell_size):
            pygame.draw.line(screen, (200, 200, 200), (0, y), (width, y))
        
        # Draw the bin (green square).
        bx, by = env.bin_pos
        bin_rect = pygame.Rect(bx * cell_size, by * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (0, 255, 0), bin_rect)
        
        # Draw waste items (brown squares).
        for waste in env.waste_items:
            if waste['exists'] == 1:
                wx, wy = waste['pos']
                waste_rect = pygame.Rect(wx * cell_size + 20, wy * cell_size + 20, cell_size - 40, cell_size - 40)
                pygame.draw.rect(screen, (139, 69, 19), waste_rect)
        
        # Draw the agent (blue circle).
        ax, ay = env.agent_pos
        agent_center = (ax * cell_size + cell_size // 2, ay * cell_size + cell_size // 2)
        pygame.draw.circle(screen, (0, 0, 255), agent_center, cell_size // 3)
        
        pygame.display.flip()
        clock.tick(5)  

        if done:
            print("Episode finished. Resetting environment...")
            time.sleep(1)
            obs, _ = env.reset()

    pygame.quit()

if __name__ == '__main__':
    simulate_trained_model("models/pg/ppo_waste(3).zip")
