import os
import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import BaseCallback, EvalCallback
from stable_baselines3.common.logger import configure
from environment.custom_env import WasteCollectionEnv

# Custom callback to log rewards
class TrainingLoggerCallback(BaseCallback):
    def __init__(self, log_dir, verbose=1):
        super(TrainingLoggerCallback, self).__init__(verbose)
        self.episode_rewards = []
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

    def _on_step(self) -> bool:
        if "infos" in self.locals and len(self.locals["infos"]) > 0:
            episode_reward = self.locals["infos"][0].get("episode", {}).get("r")
            if episode_reward is not None:
                self.episode_rewards.append(episode_reward)
                print(f"Episode Reward Logged: {episode_reward}")
        return True

    def on_training_end(self):
        np.save(os.path.join(self.log_dir, "dqn_reward_history.npy"), 
               np.array(self.episode_rewards, dtype=np.float32))

def train():
    env = WasteCollectionEnv(grid_size=5, max_steps=100)
    
    # paths
    models_dir = "models/dqn/"
    log_dir = "dqn_logs/"
    best_model_dir = os.path.join(models_dir, "best/")
    
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(best_model_dir, exist_ok=True)

    model = DQN(
        "MultiInputPolicy",
        env,
        verbose=1,
        learning_rate=3e-4,
        gamma=0.99,
        batch_size=64,
        buffer_size=100000,
        learning_starts=1000,
        target_update_interval=500,
        exploration_fraction=0.1,
        exploration_initial_eps=1.0,
        exploration_final_eps=0.01,
        tensorboard_log=log_dir
    )

    new_logger = configure(log_dir, ["stdout", "tensorboard"])
    model.set_logger(new_logger)

    training_logger = TrainingLoggerCallback(log_dir)
    eval_callback = EvalCallback(
        env, 
        best_model_save_path=best_model_dir,
        log_path=log_dir,
        eval_freq=5000,
        deterministic=True,
        render=False
    )

    model.learn(total_timesteps=100000, callback=[training_logger, eval_callback])
    
    # model save
    model.save(os.path.join(models_dir, "dqn_final_model"))
    print("DQN training completed and model saved to separate directory.")

if __name__ == '__main__':
    train()