import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import paddle
from parl.algorithms import DQN
from cartpole_model import CartpoleModel
from cartpole_agent import CartpoleAgent
from Envir import Env


def load_agent(obs_dim, act_dim):
    model = CartpoleModel(obs_dim=obs_dim, act_dim=act_dim)
    alg = DQN(model, gamma=0.99, lr=0.0005)
    agent = CartpoleAgent(alg, act_dim=act_dim, e_greed=0.0, e_greed_decrement=0.0)

    # Try common model paths
    loaded = False
    for path in ["./model.ckpt", "./inference_model"]:
        try:
            agent.load_model(path)
            print(f"Loaded model from {path}")
            loaded = True
            break
        except Exception as e:
            print(f"Could not load from {path}: {e}")
    if not loaded:
        print("No model loaded; agent will act with its random/initialized weights.")
    return agent


def evaluate(agent, env, num_episodes, max_steps=1000):
    rewards = []
    for ep in range(num_episodes):
        obs = env.reset()
        total_reward = 0.0
        step = 0
        while True:
            step += 1
            # deterministic action for evaluation
            action = agent.predict(obs)

            next_obs, reward, done, info = env.step(action)
            total_reward += reward
            obs = next_obs

            if done or step >= max_steps:
                break
        avg_reward = total_reward / step
        rewards.append(avg_reward)
        print(f"Episode {ep+1}/{num_episodes}: avg_step_reward={avg_reward:.3f}")
    return rewards


def plot_rewards(rewards, out_png="eval_rewards.png"):
    episodes = np.arange(1, len(rewards) + 1)
    plt.figure(figsize=(8,4))
    plt.plot(episodes, rewards, '-o', linewidth=1)
    plt.xlabel('Episode')
    plt.ylabel('Average Step Reward')
    plt.title('Evaluation Average Step Reward per Episode')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_png)
    print(f"Saved reward plot to {out_png}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--episodes', type=int, default=1000, help='number of evaluation episodes')
    parser.add_argument('--out', type=str, default='eval_rewards.png', help='output png path')
    args = parser.parse_args()

    env = Env()
    obs_dim = 6  # obs = [x_t, y_t, x_{t-1}, y_{t-1}, last_sensor_id, lost_flag]
    act_dim = env.act_dim  # 自动从环境获取（传感器数量）

    agent = load_agent(obs_dim, act_dim)

    rewards = evaluate(agent, env, args.episodes)

    mean = np.mean(rewards)
    std = np.std(rewards)
    print(f"Evaluation result over {len(rewards)} episodes: mean_avg_step_reward={mean:.3f}, std={std:.3f}")

    plot_rewards(rewards, out_png=args.out)

