# **Reinforcement Learning for Waste Management**  

This project uses **Reinforcement Learning** to train an **agent** that efficiently collects and disposes of waste in a grid-based environment. The agent learns to **navigate**, **pick up waste**, and **drop it in a bin** using and comparing **Proximal Policy Optimization (PPO)** and **Deep Q Network**.

![03 04 2025_18 14 34_REC](https://github.com/user-attachments/assets/4d89c771-0abf-417c-a25c-2f0a8dc536f1)



## **Features**
-  **Custom Gym Environment** for waste collection  
-  **Deep Reinforcement Learning** with PPO and DQN (Stable-Baselines3)  
-  **PyOpenGL + Pygame Rendering** for real-time visualization  
-  **Multi-Step Decision Making** (Navigation, Waste Pickup, Drop-off)  

## **Link to Video and Report:**

- https://youtu.be/1qjwMLIZvjk?si=zc-3fZJwVOBrNyDf
- https://docs.google.com/document/d/1z1ZBZ_H8c73ghdvtSInjSmp6TpgSIFe37YX_a3p8KNE/edit?usp=sharing

## **📂 Project Structure**
```bash
waste-management-rl/
├── dqn_logs/                
│   ├── cumulative_rewards.png          
│   ├── dqn_reward_history.npy         
│   ├── evaluation.npz          
│   ├── policy_entropy.png              
├── environment/                # Custom Gym environment for RL agent
│   ├── __init__.py             # Initializes the environment package
│   ├── custom_env.py           # Defines the custom environment logic
│   ├── rendering.py            # Handles visualization with PyOpenGL + Pygame
│
├── training/                   # Training scripts for RL models
│   ├── pg_training.py          # PPO training script (Stable-Baselines3)
│   ├── dqn_training.py         # DQN training script (Stable-Baselines3)
│
├── models/                      # Stores trained RL models
│   ├── pg/                      # PPO trained models
│   ├── dqn/                     # DQN trained models
│
├── logs/                
│   ├── cumulative_rewards.png          
│   ├── entropy_history.npy         
│   ├── evaluation.npz          
│   ├── policy_entropy.png 
|   ├── reward_history.npy 
|
├── plots/                      # Stores training results and logs
│   ├── dqncumulative.py      # Cumulative reward script for DQN
│   ├── cumulative.py      # Cumulative reward script for PPO
|   ├── dqnpolicy_entropy.py     # dqn script for policy
│   ├── policy_entropy.png     # PPO Policy entropy script
│   ├── logs/                      # TensorBoard logs for monitoring training
│
├── play.py                        # Run the untrained RL agent in the environment
├── playdqn.py                        # Run the trained dqn agent in the environment
├── playppo.py                        # Run the trained ppo agent in the environment
├── README.md                       # Documentation file (this file)
└── .gitignore                       # Ignore unnecessary files
```

## ** Setup Instructions**
### **1️. Clone the Repository**
```bash
git clone https://github.com/Sadickachuli/Mustapha_Sadick_rl_summative.git
cd Mustapha_Sadick_rl_summative
```
### **2️. Create and Activate a Virtual Environment**
```bash
# Create a virtual environment
python -m venv venv  

# Activate it
# On Windows:
venv\Scripts\activate  

# On macOS/Linux:
source venv/bin/activate
```
### **3️. Install Dependencies**
```bash
pip freeze > requirement.txt
pip install -r requirements.txt
```

## **Running the Trained Agent**
```bash
python play.py # To test the environment without training
python playdqn.py # To test the trained DQN agent
python playppo.py # To test the trained PPO agent
```

![wastepic](https://github.com/user-attachments/assets/24239635-1157-44d5-a254-ee7d45b8210b)




🛠 Future Improvements
- Fine-tuning hyperparameters for better performance for DQN
- Fix the agent being stuck in a loop for DQN
- Experimenting with alternative RL algorithms (SAC, TRPO)
- Implementing curriculum learning to gradually increase difficulty
- Add two bins(one for recyclable waste and the other for non-recyclable waste)

📜 License
This project is licensed under the MIT License. See LICENSE for details.

📞 Contact
👤 Achuli Mustapha Sadick
✉️ Email: [m.achuli@alustudent.com]


