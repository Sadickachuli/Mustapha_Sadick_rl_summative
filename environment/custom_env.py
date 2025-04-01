# environment/locate_waste_env.py
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random

class LocateWasteEnv(gym.Env):
    """
    Simplified Environment where an agent navigates a grid to locate a waste item.
    The grid is of size grid_size x grid_size. The agent starts at (0,0) and a single waste
    item is placed randomly (not at the agent’s start location). The agent has four movement actions.
    The episode terminates when the agent reaches the waste.
    """
    metadata = {'render.modes': ['human']}
    
    def __init__(self, grid_size=5, max_steps=50):
        super(LocateWasteEnv, self).__init__()
        self.grid_size = grid_size
        self.max_steps = max_steps
        
        # Action space: 0: up, 1: down, 2: left, 3: right.
        self.action_space = spaces.Discrete(4)
        
        # Observation space: [agent_x, agent_y, waste_x, waste_y]
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0]), 
            high=np.array([grid_size-1, grid_size-1, grid_size-1, grid_size-1]),
            dtype=np.int32
        )
        
        self.seed()
        self.reset()
    
    def seed(self, seed=None):
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]
    
    def reset(self, seed=None, options=None):
        if seed is not None:
            self.seed(seed)
        self.steps = 0
        # Start agent at (0,0)
        self.agent_pos = [0, 0]
        # Place waste randomly, ensuring it's not at the agent's start.
        while True:
            self.waste_pos = [random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)]
            if self.waste_pos != self.agent_pos:
                break
        return self._get_obs(), {}
    
    def _get_obs(self):
        # Observation is [agent_x, agent_y, waste_x, waste_y]
        return np.array(self.agent_pos + self.waste_pos, dtype=np.int32)
    
    def step(self, action):
        self.steps += 1
        reward = -0.1  # Small step penalty
        
        # Move the agent according to the action.
        if action == 0:  # Up
            if self.agent_pos[1] > 0:
                self.agent_pos[1] -= 1
            else:
                reward -= 1  # Penalize illegal move.
        elif action == 1:  # Down
            if self.agent_pos[1] < self.grid_size - 1:
                self.agent_pos[1] += 1
            else:
                reward -= 1
        elif action == 2:  # Left
            if self.agent_pos[0] > 0:
                self.agent_pos[0] -= 1
            else:
                reward -= 1
        elif action == 3:  # Right
            if self.agent_pos[0] < self.grid_size - 1:
                self.agent_pos[0] += 1
            else:
                reward -= 1
        else:
            reward -= 1
        
        # Compute Manhattan distance between agent and waste.
        distance = abs(self.agent_pos[0] - self.waste_pos[0]) + abs(self.agent_pos[1] - self.waste_pos[1])
        
        # If agent reaches the waste, add bonus and terminate.
        if distance == 0:
            reward += 20
            terminated = True
        else:
            terminated = False
        
        truncated = self.steps >= self.max_steps
        
        return self._get_obs(), reward, terminated, truncated, {}
    
    def render(self, mode='human'):
        # Create a simple text-based rendering.
        grid = [['.' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        ax, ay = self.agent_pos
        wx, wy = self.waste_pos
        grid[ay][ax] = 'A'
        grid[wy][wx] = 'W'
        for row in grid:
            print(" ".join(row))
        print()
