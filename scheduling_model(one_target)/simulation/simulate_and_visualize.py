#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
仿真脚本：运行训练好的模型进行目标跟踪仿真，并可视化
- 目标实时位置
- 传感器位置与覆盖范围
- 模型选择的活跃传感器
- 传感器观测的(角度, 距离)数据

使用示例：
  python simulate_and_visualize.py
  python simulate_and_visualize.py --episodes 5 --max-steps 300 --show
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import argparse

# 添加父目录到路径以导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Envir import Env
from cartpole_model import CartpoleModel
from cartpole_agent import CartpoleAgent
from parl.algorithms import DQN

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class SimulationRecorder:
    """记录仿真数据"""
    def __init__(self, env=None):
        self.env = env  # 环境引用，用于获取传感器配置
        self.positions = []        # 目标位置 [(x, y), ...]
        self.actions = []          # 选择的传感器 [0, 1, 0, ...]
        self.rewards = []          # 每步奖励
        self.detects = []          # 检测结果 [True, False, ...]
        self.distances = []        # 到传感器的距离
        self.angles = []           # 相对角度 (仅当检测到时)
        self.times = []            # 时间步
        
    def record(self, pos, action, reward, detect, dist, time_step):
        """记录一步的数据"""
        self.positions.append(pos)
        self.actions.append(action)
        self.rewards.append(reward)
        self.detects.append(detect)
        self.distances.append(dist)
        self.times.append(time_step)
        
        # 计算角度
        if detect and self.env is not None:
            # 从环境动态获取传感器位置
            if action < len(self.env.sensors):
                sensor_pos = self.env.sensors[action]["position"]
                rel_pos = pos - sensor_pos
                angle = np.arctan2(rel_pos[1], rel_pos[0]) * 180 / np.pi
                self.angles.append(angle)
            else:
                self.angles.append(None)
        else:
            self.angles.append(None)


def get_model_path(model_name="model.ckpt"):
    """获取模型路径（相对于项目根目录）"""
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(parent_dir, model_name)


def load_agent(obs_dim, act_dim, model_path=None):
    """加载已训练的模型"""
    if model_path is None:
        model_path = get_model_path()
    
    # 转换为绝对路径
    if not os.path.isabs(model_path):
        model_path = get_model_path(model_path)
    
    model = CartpoleModel(obs_dim=obs_dim, act_dim=act_dim)
    alg = DQN(model, gamma=0.95, lr=0.001)
    agent = CartpoleAgent(alg, act_dim=act_dim, e_greed=0.0, e_greed_decrement=0.0)
    
    if os.path.exists(model_path) or os.path.exists(model_path + ".pdparams"):
        try:
            agent.load_model(model_path)
            print(f"[OK] Model loaded from {model_path}")
            return agent
        except Exception as e:
            print(f"[WARNING] Could not load model: {e}")
    else:
        print(f"[WARNING] Model not found at {model_path}")
    
    print("[INFO] Using untrained model with random weights")
    return agent


def run_simulation(agent, env, max_steps=200, verbose=True):
    """运行一次仿真并记录数据"""
    recorder = SimulationRecorder(env=env)
    obs = env.reset()
    total_reward = 0
    
    for step in range(max_steps):
        # 代理预测动作（确定性）
        action = agent.predict(obs)
        
        # 环境执行动作
        next_obs, reward, done, info = env.step(action)
        total_reward += reward
        
        # 记录数据
        pos = np.array([obs[0], obs[1]])
        recorder.record(
            pos=pos,
            action=action,
            reward=reward,
            detect=info['detect'],
            dist=info['dist'],
            time_step=step
        )
        
        if verbose and (step + 1) % 20 == 0:
            detect_str = "DETECT" if info['detect'] else "LOST"
            print(f"  Step {step+1:3d}: action={action}, {detect_str}, reward={reward:7.2f}")
        
        obs = next_obs
        if done:
            if verbose:
                print(f"  Episode ended at step {step+1}")
            break
    
    if verbose:
        print(f"  Total reward: {total_reward:.2f}")
    
    return recorder, total_reward


def plot_trajectory(recorder, env, save_path=None):
    """绘制目标轨迹和传感器"""
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # 提取数据
    positions = np.array(recorder.positions)
    x_traj = positions[:, 0]
    y_traj = positions[:, 1]
    
    # 绘制区域边界
    ax.set_xlim(-10, 120)
    ax.set_ylim(-10, 120)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X (m)', fontsize=12)
    ax.set_ylabel('Y (m)', fontsize=12)
    ax.set_title('Target Tracking Simulation - Trajectory', fontsize=14, fontweight='bold')
    
    # 绘制传感器和覆盖范围
    # 动态颜色配置：支持任意数量的传感器
    color_palette = ['#FF6B6B', "#4ECD5B", '#45B7D1', '#FFA07A', "#165646", '#F7DC6F']
    colors = []
    for i in range(len(env.sensors)):
        if i < len(color_palette):
            colors.append(color_palette[i])
        else:
            # 如果传感器数超过调色板，使用随机颜色
            import random as rand_module
            colors.append(f'#{rand_module.randint(0, 0xFFFFFF):06x}')
    
    for i, sensor in enumerate(env.sensors):
        sensor_pos = sensor['position']
        sensor_range = sensor['range']
        
        # 覆盖圆
        circle = Circle(sensor_pos, sensor_range, color=colors[i], alpha=0.1, label=f'Sensor {i} coverage')
        ax.add_patch(circle)
        
        # 传感器位置
        ax.plot(sensor_pos[0], sensor_pos[1], marker='s', markersize=12, color=colors[i],
                label=f'Sensor {i} position', zorder=5)
    
    # 绘制目标轨迹
    ax.plot(x_traj, y_traj, 'k--', linewidth=1.5, alpha=0.5, label='Target trajectory')
    
    # 标注起点和终点
    ax.plot(x_traj[0], y_traj[0], 'go', markersize=10, label='Start', zorder=4)
    ax.plot(x_traj[-1], y_traj[-1], 'ro', markersize=10, label='End', zorder=4)
    
    # 按动作着色轨迹点
    for i in range(len(x_traj)):
        color = colors[int(recorder.actions[i])]
        alpha = 0.8 if recorder.detects[i] else 0.3
        ax.plot(x_traj[i], y_traj[i], 'o', color=color, markersize=4, alpha=alpha)
    
    ax.legend(loc='upper left', fontsize=10)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path) or '.', exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"[OK] Trajectory plot saved to {save_path}")
    
    return fig


def plot_statistics(recorder, env=None, save_path=None):
    """绘制统计信息"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    times = np.array(recorder.times)
    rewards = np.array(recorder.rewards)
    actions = np.array(recorder.actions)
    detects = np.array(recorder.detects)
    
    # 1. 奖励曲线
    ax = axes[0, 0]
    ax.plot(times, rewards, 'b-', linewidth=1.5, label='Reward')
    ax.fill_between(times, rewards, alpha=0.3)
    ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Reward')
    ax.set_title('Reward per Step')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # 2. 累积奖励
    ax = axes[0, 1]
    cumulative_reward = np.cumsum(rewards)
    ax.plot(times, cumulative_reward, 'r-', linewidth=2, label='Cumulative reward')
    ax.fill_between(times, cumulative_reward, alpha=0.3, color='r')
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Cumulative Reward')
    ax.set_title('Cumulative Reward')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # 3. 动作序列（支持动态传感器数量）
    ax = axes[1, 0]
    ax.scatter(times, actions, c=actions, cmap='coolwarm', s=50, alpha=0.6)
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Selected Sensor')
    ax.set_title('Selected Sensor over Time')
    
    # 动态设置 y 轴刻度标签
    if env is not None:
        num_sensors = len(env.sensors)
    else:
        # 备值：从 actions 最大值推算
        num_sensors = int(np.max(actions)) + 1 if len(actions) > 0 else 2
    sensor_ticks = list(range(num_sensors))
    sensor_labels = [f'Sensor {i}' for i in range(num_sensors)]
    ax.set_yticks(sensor_ticks)
    ax.set_yticklabels(sensor_labels)
    ax.grid(True, alpha=0.3)
    
    # 4. 检测率
    ax = axes[1, 1]
    if len(detects) >= 10:
        # 如果足够长，使用 10 步滑动窗口
        detect_rate = np.convolve(detects.astype(float), np.ones(10)/10, mode='valid')
        window_times = times[9:]
        ax.plot(window_times, detect_rate * 100, 'g-', linewidth=2, label='Detection rate (10-step window)')
        ax.fill_between(window_times, detect_rate * 100, alpha=0.3, color='g')
        ax.set_title('Detection Rate (Sliding Window)')
    else:
        # 如果短于 10 步，显示总体检测率
        overall_detect_rate = np.mean(detects) * 100 if len(detects) > 0 else 0
        ax.axhline(y=overall_detect_rate, color='g', linestyle='-', linewidth=2, label=f'Detection rate: {overall_detect_rate:.1f}%')
        ax.set_title('Detection Rate')
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Detection Rate (%)')
    ax.set_ylim([0, 105])
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path) or '.', exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"[OK] Statistics plot saved to {save_path}")
    
    return fig


def print_summary(recorder, env=None):
    """打印仿真摘要（支持动态传感器数量）"""
    print("\n" + "="*60)
    print("SIMULATION SUMMARY")
    print("="*60)
    
    total_steps = len(recorder.times)
    total_reward = np.sum(recorder.rewards)
    detects = np.array(recorder.detects)
    detect_rate = np.mean(detects) * 100
    
    actions = np.array(recorder.actions)
    num_sensors = int(np.max(actions)) + 1  # 从action中推断传感器数量
    if env is not None:
        num_sensors = env.act_dim  # 如果有env，优先使用env的act_dim
    
    print(f"Total steps: {total_steps}")
    print(f"Total reward: {total_reward:.2f}")
    print(f"Average reward per step: {total_reward/total_steps:.2f}")
    print(f"Detection rate: {detect_rate:.1f}%")
    print(f"\nSensor usage ({num_sensors} sensors total):")
    
    # 传感器使用统计
    for sensor_id in range(num_sensors):
        count = np.sum(actions == sensor_id)
        percentage = count / total_steps * 100 if total_steps > 0 else 0
        print(f"  Sensor {sensor_id}: {count} times ({percentage:.1f}%)")
    
    # 检测统计
    detect_by_sensor = [0] * num_sensors
    for i, (action, detect) in enumerate(zip(actions, detects)):
        if detect and action < num_sensors:
            detect_by_sensor[int(action)] += 1
    
    print(f"\nDetection by sensor:")
    for sensor_id in range(num_sensors):
        count = np.sum(actions == sensor_id)
        if count > 0:
            detect_count = detect_by_sensor[sensor_id]
            detection_rate = detect_count / count * 100
            print(f"  Sensor {sensor_id}: {detect_count}/{count} ({detection_rate:.1f}%)")
    
    print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(description='Run simulation and visualization')
    parser.add_argument('--model', type=str, default='model.ckpt', help='Model filename (relative to project root)')
    parser.add_argument('--episodes', type=int, default=10, help='Number of episodes to simulate')
    parser.add_argument('--max-steps', type=int, default=200, help='Max steps per episode')
    parser.add_argument('--seed', type=int, default=None, help='Random seed')
    parser.add_argument('--save-dir', type=str, default='./results', help='Directory to save results')
    parser.add_argument('--show', action='store_true', help='Show plots interactively')
    args = parser.parse_args()
    
    # 创建输出目录
    os.makedirs(args.save_dir, exist_ok=True)
    
    # 初始化环境和代理
    env = Env(seed=args.seed)
    obs_dim = 6
    act_dim = env.act_dim  # 自动从环境获取
    
    agent = load_agent(obs_dim, act_dim, model_path=args.model)
    
    print("\n" + "="*60)
    print("RADAR TARGET TRACKING SIMULATION")
    print("="*60)
    print(f"Model: {get_model_path(args.model)}")
    print(f"Episodes: {args.episodes}")
    print(f"Max steps per episode: {args.max_steps}")
    print(f"Output directory: {args.save_dir}\n")
    
    # 运行多个episodes
    all_recorders = []
    all_rewards = []
    
    for ep in range(args.episodes):
        print(f"[Episode {ep+1}/{args.episodes}]")
        recorder, total_reward = run_simulation(agent, env, max_steps=args.max_steps, verbose=True)
        all_recorders.append(recorder)
        all_rewards.append(total_reward)
        print()
    
    # 绘制结果
    for ep, recorder in enumerate(all_recorders):
        print(f"Plotting episode {ep+1}...")
        
        # 轨迹图
        traj_path = os.path.join(args.save_dir, f'episode_{ep+1:02d}_trajectory.png')
        fig_traj = plot_trajectory(recorder, env, save_path=traj_path)
        plt.close(fig_traj)
        
        # 统计图
        stat_path = os.path.join(args.save_dir, f'episode_{ep+1:02d}_statistics.png')
        fig_stat = plot_statistics(recorder, env=env, save_path=stat_path)
        plt.close(fig_stat)
        
        # 摘要
        print_summary(recorder, env=env)
    
    # 绘制多episode对比
    if args.episodes > 1:
        fig, ax = plt.subplots(figsize=(10, 6))
        episodes_range = np.arange(1, args.episodes + 1)
        colors = plt.cm.viridis(np.linspace(0, 1, args.episodes))
        for i, reward in enumerate(all_rewards):
            ax.bar(i + 1, reward, color=colors[i], alpha=0.7, label=f'Episode {i+1}')
        ax.set_xlabel('Episode', fontsize=12)
        ax.set_ylabel('Total Reward', fontsize=12)
        ax.set_title('Reward Comparison Across Episodes', fontsize=14, fontweight='bold')
        ax.set_xticks(episodes_range)
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend()
        plt.tight_layout()
        
        compare_path = os.path.join(args.save_dir, 'episodes_comparison.png')
        plt.savefig(compare_path, dpi=150, bbox_inches='tight')
        print(f"[OK] Comparison plot saved to {compare_path}")
        plt.close(fig)
    
    # 总体统计
    print("\n" + "="*60)
    print("OVERALL STATISTICS")
    print("="*60)
    print(f"Average reward: {np.mean(all_rewards):.2f}")
    print(f"Max reward: {np.max(all_rewards):.2f}")
    print(f"Min reward: {np.min(all_rewards):.2f}")
    print(f"Std reward: {np.std(all_rewards):.2f}")
    print("="*60 + "\n")
    
    if args.show:
        plt.show()
    else:
        print(f"[INFO] Plots saved to {os.path.abspath(args.save_dir)}")
        print("[INFO] Use --show flag to display plots interactively")


if __name__ == '__main__':
    main()
