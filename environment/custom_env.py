import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random
import pygame  # Needed for OpenGL window
from environment.rendering import render_scene, init_opengl  # Import OpenGL rendering function

class WasteSortingEnv(gym.Env):
    def __init__(self):
        super(WasteSortingEnv, self).__init__()

        self.grid_size = 5  
        self.state = None  
        self.action_space = spaces.Discrete(5)  
        self.observation_space = spaces.Box(low=0, high=self.grid_size - 1, shape=(3,), dtype=np.int32)

        # Initialize pygame and OpenGL
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500), pygame.DOUBLEBUF | pygame.OPENGL)
        init_opengl()  # Initialize OpenGL

        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.agent_pos = [random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)]
        self.waste_pos = [random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)]
        self.waste_type = random.choice(["recyclable", "non-recyclable"])  

        self.state = np.array([self.agent_pos[0], self.agent_pos[1], 0 if self.waste_type == "recyclable" else 1])
        return self.state, {}

    def step(self, action):
        reward = -1  
        done = False

        if action == 0:
            self.agent_pos[1] = max(0, self.agent_pos[1] - 1)
        elif action == 1:
            self.agent_pos[1] = min(self.grid_size - 1, self.agent_pos[1] + 1)
        elif action == 2:
            self.agent_pos[0] = max(0, self.agent_pos[0] - 1)
        elif action == 3:
            self.agent_pos[0] = min(self.grid_size - 1, self.agent_pos[0] + 1)
        elif action == 4:
            if self.agent_pos == self.waste_pos:
                reward = 10 if self.waste_type == "recyclable" else -5
                done = True 

        self.state = np.array([self.agent_pos[0], self.agent_pos[1], 0 if self.waste_type == "recyclable" else 1])

        return self.state, reward, done, {}

    def render(self):
        """Ensure OpenGL renders properly without reinitializing the window each frame."""
        render_scene(self.agent_pos, self.waste_pos, self.waste_type)
        pygame.display.flip()

    def close(self):
        pygame.quit()
