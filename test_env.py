from environment.custom_env import WasteSortingEnv
import pygame

env = WasteSortingEnv()
state, _ = env.reset()
done = False

print("Initial State:", state)

# Start a rendering loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    action = env.action_space.sample()
    state, reward, done, _ = env.step(action)

    print(f"Action Taken: {action}, New State: {state}, Reward: {reward}")
    
    env.render()
    pygame.time.wait(500)  # Delay to visualize movements

    if done:
        state, _ = env.reset()

env.close()
