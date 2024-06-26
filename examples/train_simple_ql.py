# Run with `python3 -m examples.train_simple_ql`
import os
import numpy as np
from src.envs import SimpleEnvironment
from src.trainers import QLearningTrainer
from PIL import Image

# Inspired by https://huggingface.co/learn/deep-rl-course/unit2/hands-on

env = SimpleEnvironment()
print(f"Rewards space:\n{env.rewards}")


trainer = QLearningTrainer(env)

n_episodes = 10000
learning_rate = 0.9
gamma = 0.9  # Discount factor
epsilon = 0.1
max_steps = 100


q_table = np.zeros((env.shape[0], env.shape[1], len(env.actions)))
q_table = trainer.train(
    q_table = q_table,
    n_episodes = n_episodes,
    epsilon = epsilon,
    learning_rate = learning_rate,
    gamma = gamma,
)

if not os.path.exists("saves"):
    os.makedirs("saves")
with open('saves/simple_ql.npy', 'wb') as f:
    np.save(f, q_table)

def test(q_table: np.ndarray) -> tuple[float, list[tuple[int, int]]]:
    state, _ = env.reset()
    terminated = False
    total_reward = 0
    states = []

    i = 0
    while not terminated:
        env.render(show=False, save_path=f"images/render-{i}.png")

        action = trainer.greedy_policy(q_table, state)
        state, reward, terminated, _, _ = env.step(action)

        total_reward += reward
        states.append(state)

        i += 1

    return total_reward, states


total_reward, states = test(q_table)

print(f"Total reward: {total_reward}")
print(f"States: {states}")

# Save render as gif
frames = [Image.open(f"images/render-{i}.png") for i in range(len(states))]
frames[0].save(
    "images/render.gif",
    format="GIF",
    append_images=frames[1:],
    save_all=True,
    duration=100,
    loop=0,
)
