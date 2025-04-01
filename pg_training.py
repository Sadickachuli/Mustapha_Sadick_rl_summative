# training/pg_training.py
import os
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold
from environment.custom_env import LocateWasteEnv

def train():
    # Create the environment.
    env = LocateWasteEnv(grid_size=5, max_steps=50)
    
    # Create directory for saving models.
    models_dir = "models/pg/"
    os.makedirs(models_dir, exist_ok=True)
    
    # Setup evaluation environment and callback.
    eval_env = LocateWasteEnv(grid_size=5, max_steps=50)
    callback_on_best = StopTrainingOnRewardThreshold(reward_threshold=15, verbose=1)
    eval_callback = EvalCallback(
        eval_env, 
        best_model_save_path=models_dir,
        log_path=models_dir, 
        eval_freq=2000, 
        deterministic=True, 
        render=False, 
        callback_after_eval=callback_on_best
    )
    
    # Initialize PPO with an MLP policy.
    model = PPO("MlpPolicy", env, verbose=1, learning_rate=0.0005, gamma=0.99)
    
    # Train the model.
    model.learn(total_timesteps=50000, callback=eval_callback)
    
    # Save the trained model.
    model.save(models_dir + "ppo_locate")
    
    print("Training completed and model saved.")
    
if __name__ == '__main__':
    train()
