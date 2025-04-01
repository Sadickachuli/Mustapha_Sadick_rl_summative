# environment/custom_env.py
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random

class WasteCollectionEnv(gym.Env):
    """
    Custom Environment where an agent picks up waste and drops them in a bin.
    The grid is of size grid_size x grid_size. Waste items are placed randomly
    (avoiding the agent start and the bin location). Actions include moving in 4 directions,
    picking up waste, and dropping waste.
    """
    metadata = {'render.modes': ['human']}
    
    def __init__(self, grid_size=5, num_waste=3, max_steps=100):
        super(WasteCollectionEnv, self).__init__()
        self.grid_size = grid_size
        self.num_waste = num_waste
        self.max_steps = max_steps
        
        # Define action space:
        # 0: move up, 1: move down, 2: move left, 3: move right, 4: pick up, 5: drop
        self.action_space = spaces.Discrete(6)
        
        # Observation space: [agent_x, agent_y, has_waste,
        # waste1_x, waste1_y, waste1_exists, ...]
        obs_low = np.array([0, 0, 0] + [0, 0, 0] * self.num_waste, dtype=np.int32)
        obs_high = np.array(
            [grid_size - 1, grid_size - 1, 1] + [grid_size - 1, grid_size - 1, 1] * self.num_waste,
            dtype=np.int32
        )
        self.observation_space = spaces.Box(low=obs_low, high=obs_high, dtype=np.int32)
        
        # Fixed bin location at bottom right corner.
        self.bin_pos = (grid_size - 1, grid_size - 1)
        
        self.seed()  # initialize RNG
        self.reset()
    
    def seed(self, seed=None):
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]
    
    def reset(self, seed=None, options=None):
        if seed is not None:
            self.seed(seed)
        
        self.steps = 0
        self.last_action = None  # For repeated-action penalty
        
        # Initialize agent at (0,0) and not carrying waste.
        self.agent_pos = [0, 0]
        self.has_waste = 0
        
        # Place waste items randomly (avoid agent start and bin position).
        self.waste_items = []
        positions = []
        while len(positions) < self.num_waste:
            pos = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            if pos == tuple(self.agent_pos) or pos == self.bin_pos or pos in positions:
                continue
            positions.append(pos)
        for pos in positions:
            self.waste_items.append({'pos': pos, 'exists': 1})
        
        # Initialize distance for shaping rewards.
        self._update_prev_distance()
        return self._get_obs(), {}
    
    def _get_obs(self):
        obs = [self.agent_pos[0], self.agent_pos[1], self.has_waste]
        for waste in self.waste_items:
            obs.extend([waste['pos'][0], waste['pos'][1], waste['exists']])
        return np.array(obs, dtype=np.int32)
    
    def _get_target(self):
        # When not carrying waste, target the nearest available waste.
        # If carrying waste, target the bin.
        if self.has_waste == 0:
            candidates = [waste['pos'] for waste in self.waste_items if waste['exists'] == 1]
            if candidates:
                distances = [abs(self.agent_pos[0]-p[0]) + abs(self.agent_pos[1]-p[1]) for p in candidates]
                min_index = distances.index(min(distances))
                return candidates[min_index]
            else:
                return self.bin_pos
        else:
            return self.bin_pos

    def _update_prev_distance(self):
        target = self._get_target()
        self.prev_distance = abs(self.agent_pos[0] - target[0]) + abs(self.agent_pos[1] - target[1])
    
    def step(self, action):
        base_reward = -0.1  # Small step penalty
        terminated = False
        truncated = False
        info = {}
        self.steps += 1

        # Penalty for repeating the same movement action.
        if self.last_action is not None and action == self.last_action and action in [0, 1, 2, 3]:
            base_reward -= 0.05

        # Save previous distance for shaping reward.
        prev_distance = self.prev_distance
        
        # Execute action.
        if action == 0:  # Move Up
            if self.agent_pos[1] > 0:
                self.agent_pos[1] -= 1
            else:
                base_reward -= 1
        elif action == 1:  # Move Down
            if self.agent_pos[1] < self.grid_size - 1:
                self.agent_pos[1] += 1
            else:
                base_reward -= 1
        elif action == 2:  # Move Left
            if self.agent_pos[0] > 0:
                self.agent_pos[0] -= 1
            else:
                base_reward -= 1
        elif action == 3:  # Move Right
            if self.agent_pos[0] < self.grid_size - 1:
                self.agent_pos[0] += 1
            else:
                base_reward -= 1
        elif action == 4:  # Pick up waste
            if self.has_waste == 0:
                picked = False
                for waste in self.waste_items:
                    if waste['exists'] == 1 and tuple(self.agent_pos) == waste['pos']:
                        waste['exists'] = 0
                        self.has_waste = 1
                        base_reward += 10  # Stronger reward for pickup.
                        picked = True
                        break
                if not picked:
                    base_reward -= 1
            else:
                base_reward -= 1
        elif action == 5:  # Drop waste
            if self.has_waste == 1:
                if tuple(self.agent_pos) == self.bin_pos:
                    self.has_waste = 0
                    base_reward += 30  # Stronger reward for correct drop-off.
                else:
                    base_reward -= 1
            else:
                base_reward -= 1
        else:
            base_reward -= 1
        
        self.last_action = action
        
        # Update distance for shaping rewards.
        self._update_prev_distance()
        new_distance = self.prev_distance
        # Increase shaping coefficient (now 1.0) to provide a stronger signal.
        shaping_reward = 1.0 * (prev_distance - new_distance)
        
        total_reward = base_reward + shaping_reward

        # Mission complete: all waste delivered.
        all_delivered = all(waste['exists'] == 0 for waste in self.waste_items) and self.has_waste == 0
        if all_delivered:
            terminated = True
            total_reward += 20  # Bonus for mission completion.
        
        if self.steps >= self.max_steps:
            truncated = True
        
        return self._get_obs(), total_reward, terminated, truncated, info
    
    def render(self, mode='human'):
        grid = [['.' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        bx, by = self.bin_pos
        grid[by][bx] = 'B'
        for waste in self.waste_items:
            if waste['exists'] == 1:
                x, y = waste['pos']
                grid[y][x] = 'W'
        ax, ay = self.agent_pos
        grid[ay][ax] = 'A'
        for row in grid:
            print(" ".join(row))
        print()
