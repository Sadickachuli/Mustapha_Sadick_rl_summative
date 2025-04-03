import numpy as np
import matplotlib.pyplot as plt

# Load rewards
reward_file = "logs/reward_history.npy"
rewards = np.load(reward_file, allow_pickle=True)

if len(rewards) == 0:
    raise ValueError("No rewards logged. Ensure training ran successfully.")

# Compute cumulative rewards
cumulative_rewards = np.cumsum(rewards)

# Plot
plt.figure(figsize=(10, 5))
plt.plot(cumulative_rewards, label="Cumulative Reward", color="blue")
plt.xlabel("Episodes")
plt.ylabel("Cumulative Reward")
plt.title("Cumulative Reward Over Training")
plt.legend()
plt.grid(True)

# Save plot
plt.savefig("logs/cumulative_rewards.png")
plt.show()
