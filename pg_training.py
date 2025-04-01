# training/pg_training.py
import os
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold
from environment.custom_env import WasteCollectionEnv

def train():
    # Create the environment.
    env = WasteCollectionEnv()
    
    # Create the directory to save models if it doesn't exist.
    models_dir = "models/pg/"
    os.makedirs(models_dir, exist_ok=True)
    
    # Setup an evaluation environment and callbacks to monitor progress.
    eval_env = WasteCollectionEnv()
    callback_on_best = StopTrainingOnRewardThreshold(reward_threshold=5, verbose=1)  # Adjust threshold as needed
    eval_callback = EvalCallback(eval_env, best_model_save_path=models_dir,
                                 log_path=models_dir, eval_freq=5000,
                                 deterministic=True, render=False, callback_after_eval=callback_on_best)
    
    # Initialize PPO with a MLP policy.
    # Increased learning rate and added entropy coefficient to boost exploration.
    model = PPO("MlpPolicy", env, verbose=1, learning_rate=0.0005, gamma=0.99, ent_coef=0.01)
    
    # Train the model for a given number of timesteps.
    model.learn(total_timesteps=100000, callback=eval_callback)
    
    # Save the trained model.
    model.save(models_dir + "ppo_waste(4)")
    
    print("Training completed and model saved.")
    
if __name__ == '__main__':
    train()
