# **Reinforcement Learning for Waste Management 🚀**  

This project uses **Reinforcement Learning (RL)** to train an **agent** that efficiently collects and disposes of waste in a grid-based environment. The agent learns to **navigate**, **pick up waste**, and **drop it in a bin** using **Proximal Policy Optimization (PPO)**.

![wastepic](https://github.com/user-attachments/assets/6cbc13fa-8e5c-4627-856d-4a9e72a61761)

## **📌 Features**
- ✅ **Custom Gym Environment** for waste collection  
- ✅ **Deep Reinforcement Learning** with PPO (Stable-Baselines3)  
- ✅ **PyOpenGL + Pygame Rendering** for real-time visualization  
- ✅ **Multi-Step Decision Making** (Navigation, Waste Pickup, Drop-off)  

---

## **📂 Project Structure**
📦 waste-management-rl ├── environment │ ├── init.py # Initializes the environment package │ ├── custom_env.py # Custom Gym environment definition │ ├── rendering.py # 3D visualization with PyOpenGL + Pygame │ ├── config.py # Environment configuration settings │ ├── training │ ├── pg_training.py # PPO training script (Stable-Baselines3) │ ├── dqn_training.py # DQN training script (Stable-Baselines3) │ ├── evaluate.py # Evaluate trained models │ ├── models │ ├── pg/ # PPO trained models │ ├── dqn/ # DQN trained models │ ├── results │ ├── plots/ │ │ ├── dqncumulative.png # Cumulative reward for DQN │ │ ├── ppocumulative.png # Cumulative reward for PPO │ │ ├── policy_entropy.png # PPO Policy entropy over training │ ├── logs/ # Tensorboard logs for monitoring training │ ├── main.py # Run trained RL agents in the environment ├── requirements.txt # Dependencies for the project ├── README.md # This file ├── LICENSE # License file (MIT, GPL, etc.) └── .gitignore # Ignore unnecessary files

yaml
Copy
Edit

---

## **💻 Setup Instructions**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/waste-management-rl.git
cd waste-management-rl
2️⃣ Create and Activate a Virtual Environment
bash
Copy
Edit
# Create a virtual environment
python -m venv venv  

# Activate it
# On Windows:
venv\Scripts\activate  

# On macOS/Linux:
source venv/bin/activate
3️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
🚀 How to Train the RL Agent
1️⃣ Train with PPO (Proximal Policy Optimization)
bash
Copy
Edit
python training/pg_training.py
This will train the agent using PPO and save the model in the models/pg/ directory.

2️⃣ Train with DQN (Deep Q-Network)
bash
Copy
Edit
python training/dqn_training.py
This will train the agent using DQN and save the model in models/dqn/.

3️⃣ Monitor Training in TensorBoard
To visualize training metrics:

bash
Copy
Edit
tensorboard --logdir=results/logs/
Then, open http://localhost:6006/ in your browser.

🎮 Running the Trained Agent
After training, you can test the agent:

bash
Copy
Edit
python main.py --model_path models/pg/latest_model.zip
Modify --model_path to test different models.

📊 Results and Analysis
📈 PPO Training Performance

The cumulative reward increased over time, indicating successful learning.

PPO balanced exploration and exploitation well.

📉 DQN Training Performance

The cumulative reward decreased, suggesting that DQN struggled in this environment.

🔍 Policy Entropy Over Training

The policy entropy dropped to zero, meaning no exploration was happening after a while.

Possible Fix: Increase entropy coefficient (ent_coef).

🛠 Future Improvements
🔹 Fine-tuning hyperparameters for better performance

🔹 Experimenting with alternative RL algorithms (SAC, TRPO)

🔹 Implementing curriculum learning to gradually increase difficulty

📜 License
This project is licensed under the MIT License. See LICENSE for details.

📞 Contact
👤 Achuli Mustapha Sadick
✉️ Email: [your-email@example.com]
🔗 GitHub: your-github-profile


https://github.com/user-attachments/assets/848a33fc-e26a-4928-9968-94741d63232b

