import os
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from environment.custom_env import WasteCollectionEnv

def train():
    env = WasteCollectionEnv(grid_size=5, max_steps=100)
    
    models_dir = "models/pg/"
    os.makedirs(models_dir, exist_ok=True)

    # Using MultiInputPolicy for dictionary observations
    model = PPO(
        "MultiInputPolicy",
        env,
        verbose=1,
        learning_rate=3e-4,
        gamma=0.99,
        batch_size=64,
        n_steps=2048,
        n_epochs=10,
        ent_coef=0.01
    )

    # Evaluation callback
    eval_callback = EvalCallback(
        env,
        best_model_save_path=models_dir,
        log_path=models_dir,
        eval_freq=5000,
        deterministic=True,
        render=False
    )

    model.learn(total_timesteps=100000, callback=eval_callback)
    model.save(os.path.join(models_dir, "ppo_collection"))
    print("Training completed and model saved.")

if __name__ == '__main__':
    train()