import numpy as np
import matplotlib.pyplot as plt

# Load entropy values
entropy_file = "dqn_logs/evaluations.npz"
entropy_values = np.load(entropy_file, allow_pickle=True)

if len(entropy_values) == 0:
    raise ValueError("No entropy values logged. Ensure training ran successfully.")

# Plot entropy values
plt.figure(figsize=(10, 5))
plt.plot(entropy_values, label="Policy Entropy", color="red")
plt.xlabel("Training Steps")
plt.ylabel("Entropy")
plt.title("Policy Entropy Over Training")
plt.legend()
plt.grid(True)

# Save plot
plt.savefig("dqn_logs/policy_entropy.png")
plt.show()
