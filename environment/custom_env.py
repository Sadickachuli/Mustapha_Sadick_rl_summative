import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random
import pygame  # Needed for OpenGL window
from environment.rendering import render_scene, init_opengl  # Import rendering functions

class WasteSortingEnv(gym.Env):
    def __init__(self):
        super(WasteSortingEnv, self).__init__()

        self.grid_size = 5  
        self.state = None  
        # Now state is 4-dimensional: [agent_x, agent_y, waste_type_index, holding]
        self.action_space = spaces.Discrete(5)  
        self.observation_space = spaces.Box(low=0, high=self.grid_size - 1, shape=(4,), dtype=np.int32)

        # Fixed bin positions (grid coordinates)
        # Using glOrtho(0,500,500,0) with cell size 100 means (0,0) is top-left.
        self.bin_positions = {
            "recyclable": [0, 0],       # Top-left cell
            "non-recyclable": [4, 0]      # Top-right cell
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
        self.holding = 0  # 0 = not holding waste, 1 = holding waste

        self.state = np.array([self.agent_pos[0], self.agent_pos[1],
                                0 if self.waste_type == "recyclable" else 1,
                                self.holding], dtype=np.int32)
        return self.state, {}

    def step(self, action):
        reward = -1  
        done = False

        # Move actions: 0 = up, 1 = down, 2 = left, 3 = right
        if action == 0:
            self.agent_pos[1] = max(0, self.agent_pos[1] - 1)
        elif action == 1:
            self.agent_pos[1] = min(self.grid_size - 1, self.agent_pos[1] + 1)
        elif action == 2:
            self.agent_pos[0] = max(0, self.agent_pos[0] - 1)
        elif action == 3:
            self.agent_pos[0] = min(self.grid_size - 1, self.agent_pos[0] + 1)
        elif action == 4:
            # Action 4: Interact (pick up or drop off)
            if self.holding == 0:
                # If not holding, try to pick up waste
                if self.agent_pos == self.waste_pos:
                    self.holding = 1  # Pick up the waste
                    reward = 0  # No reward for picking up
                else:
                    reward = -1  # Penalty for attempting pickup at wrong location
            else:
                # If already holding, try to drop off at correct bin
                correct_bin = self.bin_positions[self.waste_type]
                if self.agent_pos == correct_bin:
                    reward = 10  # Correct drop-off reward
                    done = True
                    self.holding = 0  # Drop off completed
                else:
                    reward = -1  # Penalty for dropping off at wrong location

        # Update state with new positions and holding status
        self.state = np.array([self.agent_pos[0], self.agent_pos[1],
                                0 if self.waste_type == "recyclable" else 1,
                                self.holding], dtype=np.int32)
        return self.state, reward, done, {}

    def render(self):
        """Render the environment using OpenGL."""
        # Pass bin positions and holding flag to rendering so it knows whether to draw waste on floor
        render_scene(self.agent_pos, self.waste_pos, self.waste_type, self.holding, self.bin_positions)
        pygame.display.flip()

    def close(self):
        pygame.quit()
