#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速测试脚本：快速运行仿真并显示基本可视化
用于快速验证模型效果，无需保存文件

使用示例：
  python quick_simulate.py
  python quick_simulate.py --max-steps 300 --seed 42
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# 添加父目录到路径以导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Envir import Env
from cartpole_model import CartpoleModel
from cartpole_agent import CartpoleAgent
from parl.algorithms import DQN


def get_model_path(model_name="model.ckpt"):
    """获取模型路径（相对于项目根目录）"""
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(parent_dir, model_name)


def quick_simulate(model_path="model.ckpt", max_steps=200, seed=None):
    """快速仿真并绘制结果"""
    
    # 转换模型路径
    if not os.path.isabs(model_path):
        model_path = get_model_path(model_path)
    
    # 初始化环境和模型
    env = Env(seed=seed)
    obs_dim = 6  # 固定：[x, y, x_prev, y_prev, last_action, lost_flag]
    act_dim = env.act_dim  # 从环境自动读取传感器数量
    
    model = CartpoleModel(obs_dim=obs_dim, act_dim=act_dim)
    alg = DQN(model, gamma=0.95, lr=0.001)
    agent = CartpoleAgent(alg, act_dim=env.act_dim, e_greed=0.0, e_greed_decrement=0.0)
    
    # 尝试加载模型
    if os.path.exists(model_path) or os.path.exists(model_path + ".pdparams"):
        try:
            agent.load_model(model_path)
            print(f"[OK] Model loaded from {model_path}")
        except Exception as e:
            print(f"[WARNING] Model load failed: {e}")
            print("[INFO] Using random agent")
    else:
        print(f"[WARNING] Model not found at {model_path}")
        print("[INFO] Using random agent")
    
    # 运行仿真并收集数据
    print("Running simulation...")
    obs = env.reset()
    
    positions = []
    actions = []
    rewards = []
    detects = []
    total_reward = 0
    
    for step in range(max_steps):
        action = agent.predict(obs)
        next_obs, reward, done, info = env.step(action)
        
        positions.append([obs[0], obs[1]])
        actions.append(action)
        rewards.append(reward)
        detects.append(info['detect'])
        total_reward += reward
        
        obs = next_obs
        
        if (step + 1) % 50 == 0:
            print(f"  Step {step+1}: reward={reward:.2f}, cumsum={total_reward:.2f}")
        
        if done:
            print(f"  Episode ended at step {step+1}")
            break
    
    # 转换为数组
    positions = np.array(positions)
    actions = np.array(actions)
    rewards = np.array(rewards)
    detects = np.array(detects)
    
    # 绘图
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # 左图：轨迹
    ax = axes[0]
    ax.set_xlim(-10, 120)
    ax.set_ylim(-10, 120)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X (m)', fontsize=11)
    ax.set_ylabel('Y (m)', fontsize=11)
    ax.set_title(f'Target Trajectory (Total Reward: {total_reward:.2f})', fontsize=12, fontweight='bold')
    
    # 传感器
    # 动态颜色配置：支持任意数量的传感器
    color_palette = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
    colors = []
    for i in range(len(env.sensors)):
        if i < len(color_palette):
            colors.append(color_palette[i])
        else:
            # 如果传感器数超过调色板，使用随机颜色
            import random as rand_module
            colors.append(f'#{rand_module.randint(0, 0xFFFFFF):06x}')
    
    for i, sensor in enumerate(env.sensors):
        pos = sensor['position']
        rng = sensor['range']
        
        # 覆盖圆
        circle = Circle(pos, rng, color=colors[i], alpha=0.1)
        ax.add_patch(circle)
        
        # 传感器
        ax.plot(pos[0], pos[1], marker='s', markersize=10, color=colors[i], zorder=5)
        ax.text(pos[0], pos[1]-8, f'S{i}', ha='center', fontsize=10, fontweight='bold')
    
    # 轨迹点
    for i in range(len(positions)):
        color = colors[int(actions[i])]
        alpha = 0.8 if detects[i] else 0.2
        ax.plot(positions[i, 0], positions[i, 1], 'o', color=color, markersize=4, alpha=alpha)
    
    # 起终点
    ax.plot(positions[0, 0], positions[0, 1], 'go', markersize=10, label='Start', zorder=4)
    ax.plot(positions[-1, 0], positions[-1, 1], 'ro', markersize=10, label='End', zorder=4)
    ax.plot(positions[:, 0], positions[:, 1], 'k--', linewidth=1, alpha=0.3)
    
    ax.legend(loc='upper left', fontsize=10)
    
    # 右图：统计
    ax = axes[1]
    steps = np.arange(len(rewards))
    
    # 双轴
    ax1 = ax
    ax2 = ax1.twinx()
    
    # 奖励
    bar = ax1.bar(steps, rewards, alpha=0.6, color='steelblue', label='Reward')
    ax1.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax1.set_ylabel('Reward', color='steelblue', fontsize=11)
    ax1.tick_params(axis='y', labelcolor='steelblue')
    ax1.set_xlabel('Time Step', fontsize=11)
    
    # 累积奖励
    cumsum = np.cumsum(rewards)
    line = ax2.plot(steps, cumsum, 'r-', linewidth=2, label='Cumulative', marker='o', markersize=3)
    ax2.set_ylabel('Cumulative Reward', color='red', fontsize=11)
    ax2.tick_params(axis='y', labelcolor='red')
    
    ax1.set_title('Reward Analysis', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='x')
    
    # 图例
    lines = [bar] + line
    labels = ['Reward', 'Cumulative']
    ax1.legend(lines, labels, loc='upper left', fontsize=10)
    
    plt.tight_layout()
    plt.show()
    
    # 输出统计
    print("\n" + "="*50)
    print("STATISTICS")
    print("="*50)
    print(f"Total steps: {len(rewards)}")
    print(f"Total reward: {total_reward:.2f}")
    print(f"Avg reward: {np.mean(rewards):.3f}")
    print(f"Detection rate: {np.mean(detects)*100:.1f}%")
    # 传感器使用统计（支持动态传感器数量）
    num_sensors = len(env.sensors)
    print(f"\nSensor usage ({num_sensors} sensors total):")
    
    for sensor_id in range(num_sensors):
        usage = np.sum(actions == sensor_id)
        if usage > 0:
            print(f"  Sensor {sensor_id}: {usage} times ({usage/len(actions)*100:.1f}%)")
            detect_count = np.sum(detects[actions == sensor_id])
            print(f"    Detection rate: {detect_count/usage*100:.1f}%")
    print("="*50)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Quick simulation and visualization')
    parser.add_argument('--model', type=str, default='model.ckpt', help='Model filename')
    parser.add_argument('--max-steps', type=int, default=200, help='Max steps')
    parser.add_argument('--seed', type=int, default=None, help='Random seed')
    args = parser.parse_args()
    
    quick_simulate(model_path=args.model, max_steps=args.max_steps, seed=args.seed)
