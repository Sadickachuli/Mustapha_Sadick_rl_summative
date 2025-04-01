# play_trained.py
import time
import pygame
from stable_baselines3 import PPO
from environment.custom_env import LocateWasteEnv

def simulate_trained_model(model_path):
    # Create the environment and load the trained model.
    env = LocateWasteEnv(grid_size=5, max_steps=50)
    model = PPO.load(model_path)
    
    obs, _ = env.reset()

    # Set up pygame.
    cell_size = 100
    grid_size = env.grid_size
    width = cell_size * grid_size
    height = cell_size * grid_size

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Trained Model Simulation: Locate Waste")
    clock = pygame.time.Clock()

    running = True
    done = False

    while running:
        # Process events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Use the model to predict the next action.
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated

        # Clear screen.
        screen.fill((255, 255, 255))
        
        # Draw grid lines.
        for x in range(0, width, cell_size):
            pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, height))
        for y in range(0, height, cell_size):
            pygame.draw.line(screen, (200, 200, 200), (0, y), (width, y))
        
        # Draw waste as a brown square.
        wx, wy = env.waste_pos
        waste_rect = pygame.Rect(wx * cell_size + 20, wy * cell_size + 20, cell_size - 40, cell_size - 40)
        pygame.draw.rect(screen, (139, 69, 19), waste_rect)
        
        # Draw the agent as a blue circle.
        ax, ay = env.agent_pos
        agent_center = (ax * cell_size + cell_size // 2, ay * cell_size + cell_size // 2)
        pygame.draw.circle(screen, (0, 0, 255), agent_center, cell_size // 3)
        
        pygame.display.flip()
        clock.tick(5)  # Adjust FPS as needed

        if done:
            print("Episode finished. Resetting environment...")
            time.sleep(1)
            obs, _ = env.reset()

    pygame.quit()

if __name__ == '__main__':
    # Make sure the model file exists at this path.
    simulate_trained_model("models/pg/ppo_locate.zip")
