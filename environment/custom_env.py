import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random
import pygame  # Needed for OpenGL window
from environment.rendering import render_scene, init_opengl  # Import rendering functions

class WasteSortingEnv(gym.Env):
    """
    Custom Gym environment for waste collection and sorting.
    The agent navigates a 5x5 grid, picks up a waste item, and carries it to the correct bin.
    
    State: [agent_x, agent_y, waste_type_index, holding]
      - waste_type_index: 0 for recyclable, 1 for non-recyclable.
      - holding: 0 if not carrying waste, 1 if carrying waste.
    
    Action Space (Discrete, 5 actions):
      0: Move Up
      1: Move Down
      2: Move Left
      3: Move Right
      4: Interact (pick up if not holding; drop off if holding)
    """
    def __init__(self):
        super(WasteSortingEnv, self).__init__()

        self.grid_size = 5  
        self.state = None  
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(low=0, high=self.grid_size - 1, shape=(4,), dtype=np.int32)

        # Fixed bin positions (grid coordinates; (0,0) is top-left with our projection)
        self.bin_positions = {
            "recyclable": [0, 0],       # Recycling bin at top-left
            "non-recyclable": [4, 0]      # Non-recycling bin at top-right
        }

        # Initialize pygame and OpenGL once
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500), pygame.DOUBLEBUF | pygame.OPENGL)
        init_opengl()  # Set up OpenGL projection
        
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.agent_pos = [random.randint(0, self.grid_size - 1),
                          random.randint(0, self.grid_size - 1)]
        self.waste_pos = [random.randint(0, self.grid_size - 1),
                          random.randint(0, self.grid_size - 1)]
        self.waste_type = random.choice(["recyclable", "non-recyclable"])
        self.holding = 0  # Not holding any waste initially
        self.total_reward = 0  # Reset total reward for the episode

        self.state = np.array([self.agent_pos[0], self.agent_pos[1],
                                0 if self.waste_type == "recyclable" else 1,
                                self.holding], dtype=np.int32)
        return self.state, {}

    def step(self, action):
        reward = -1  # Step penalty
        done = False

        # Move actions (0: up, 1: down, 2: left, 3: right)
        if action == 0:
            self.agent_pos[1] = max(0, self.agent_pos[1] - 1)
        elif action == 1:
            self.agent_pos[1] = min(self.grid_size - 1, self.agent_pos[1] + 1)
        elif action == 2:
            self.agent_pos[0] = max(0, self.agent_pos[0] - 1)
        elif action == 3:
            self.agent_pos[0] = min(self.grid_size - 1, self.agent_pos[0] + 1)
        elif action == 4:
            # Interact action: pick up or drop off
            if self.holding == 0:
                # Pick up waste if on the same cell
                if self.agent_pos == self.waste_pos:
                    self.holding = 1
                    reward = 0  # No reward for pickup
                else:
                    reward = -1  # Penalty for interacting in the wrong cell
            else:
                # Drop off waste if holding it
                correct_bin = self.bin_positions[self.waste_type]
                if self.agent_pos == correct_bin:
                    reward = 10  # Correct drop-off reward
                    done = True
                    self.holding = 0
                else:
                    reward = -1  # Penalty for dropping off at wrong bin

        self.total_reward += reward

        self.state = np.array([self.agent_pos[0], self.agent_pos[1],
                                0 if self.waste_type == "recyclable" else 1,
                                self.holding], dtype=np.int32)
        return self.state, reward, done, {}

    def render(self, episode_end=False):
        """
        Renders the environment using OpenGL.
        Displays the grid, bins, waste (if not held), agent, and a scoreboard.
        """
        render_scene(self.agent_pos, self.waste_pos, self.waste_type,
                     self.holding, self.bin_positions, self.total_reward, episode_end)
        pygame.display.flip()

    def close(self):
        pygame.quit()
