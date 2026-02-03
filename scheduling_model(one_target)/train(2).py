#parl-env\Scripts\activate 激活虚拟环境     deactivate 退出虚拟环境

import argparse
from parl.utils import logger, ReplayMemory
from cartpole_model import CartpoleModel
from cartpole_agent import CartpoleAgent
from parl.env import CompatWrapper, is_gym_version_ge
from parl.algorithms import DQN

import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

import matplotlib.pyplot as plt
import numpy as np

from Envir import Env

LEARN_FREQ = 10  # training frequency   # 训练频率
MEMORY_SIZE = 200000            # replay memory的大小
MEMORY_WARMUP_SIZE = 1000         # 减少预热大小以加快初始训练
BATCH_SIZE = 128             # 增加批大小以稳定梯度
LEARNING_RATE = 0.001       # 提高学习率以加快收敛
GAMMA = 0.95                # 适度降低gamma以平衡长期和短期奖励

# train an episode
def run_train_episode(agent, env, rpm): #agent智能体，用于执行动作和学习策略;env智能体与之互动的模拟环境，它提供了状态、奖励等信息;rpm：Replay Memory，经验回放缓冲区，用于存储智能体的经验，以便后续训练
    total_reward = 0        # 初始化总奖励
    obs = env.reset()      # 初始化为环境的初始观察值（状态）
    step = 0
    # sum_rate = 0
    flag = False
    
    # 新增：用于统计指标的变量
    total_detect = 0  # 探测成功次数
    total_steps = 0   # 总步数
    lost_episode = 0  # 该episode是否发生了连续丢失 (lost_steps >= k_loss)
    switch_count = 0  # 传感器切换次数
    last_action = None  # 上一个动作
    
    while True:         # 进入无限循环，直到一个训练周期结束
        step += 1       # 计算步数
        total_steps += 1  # 累计总步数
        
        action = agent.sample(obs)      #代理根据当前状态obs从策略中选择一个动作
        
        # 检测切换
        if last_action is not None and action != last_action:
            switch_count += 1
        last_action = action
        
        # 调用环境 step（环境内部会更新真实位置并返回 obs）
        next_obs, reward, done, info = env.step(action)        #代理执行动作，与环境互动，获取下一个状态 next_obs、奖励 reward、是否完成 done 等信息
        # print("时刻: "+str(step) + " 调度传感器编号: "+str(action))
        
        # 统计探测成功（通过info字典判断）
        if info.get('detect', False):
            total_detect += 1
        
        # 判断是否发生连续丢失
        if info.get('lost_steps', 0) >= env.k_loss:
            lost_episode = 1
        
        rpm.append(obs, action, reward, next_obs, done)     #将这一步的经验存储到经验回放缓冲区中
        # train model       检查经验回放缓冲区中是否有足够的经验用于训练，并且每隔一定的步数执行一次模型的学习（训练操作
        if (len(rpm) > MEMORY_WARMUP_SIZE) and (step % LEARN_FREQ == 0):
            # s,a,r,s',done
            (batch_obs, batch_action, batch_reward, batch_next_obs,      # 从经验回放缓冲区中抽样一批数据
             batch_done) = rpm.sample_batch(BATCH_SIZE)
            train_loss = agent.learn(batch_obs, batch_action, batch_reward,     # 使用抽样数据来训练智能体的模型
                                     batch_next_obs, batch_done)

        total_reward += reward      # 累积当前步的奖励到总奖励
        obs = next_obs      # 更新当前观察状态
        if done:            # 如果训练周期结束（例如，达到最大步数），则退出循环
            break
    
    # 计算指标
    detect_rate = total_detect / total_steps if total_steps > 0 else 0  # 探测成功率
    lost_prob = lost_episode  # 是否发生连续丢失 (0 or 1)
    switch_rate = switch_count / total_steps if total_steps > 0 else 0  # 切换率
    
    return total_reward, action, detect_rate, lost_prob, switch_rate     # 返回奖励、动作、探测率、丢失概率、切换率


def main():
    env = Env()
    # Compatible for different versions of gym
    # env = CompatWrapper(env)                    # 确保与不同版本的gym兼容

    obs_dim = 6        # 获取状态空间的维度（x_t,y_t,x_{t-1},y_{t-1},last_sensor_id,lost_flag）
    act_dim = env.act_dim  # 自动从环境获取动作维度（传感器数量）
    # logger.info('obs_dim {}, act_dim {}'.format(obs_dim, act_dim))  # 用日志记录器记录状态和动作空间的维度

    # set action_shape = 0 while in discrete control environment    # 设置 action_shape = 0 在离散控制环境中
    rpm = ReplayMemory(MEMORY_SIZE, obs_dim, 0)                     # 创建经验回放内存 用于存储代理经验；obs_dim状态空间的维度；0 表示在离散动作环境中，不需要记录动作的维度

    # build an agent
    model = CartpoleModel(obs_dim=obs_dim, act_dim=act_dim)     # 创建代理的模型 该模型可能是一个神经网络模型，用于逼近状态-动作值函数
    alg = DQN(model, gamma=GAMMA, lr=LEARNING_RATE)             # 创建DQN算法 使用DQN）算法创建代理的算法。gamma 是折扣因子，lr 是学习率
    agent = CartpoleAgent(                                      # 创建Cartpole代理，将算法、动作空间维度、初始贪婪度（e_greed）和贪婪度递减率（e_greed_decrement）传递给代理
        alg, act_dim=act_dim, e_greed=1.0, e_greed_decrement=1e-4)

    # warmup memory     # 填充经验回放内存
    while len(rpm) < MEMORY_WARMUP_SIZE:        # 循环执行以下操作，直到经验回放内存的大小达到设定的 MEMORY_WARMUP_SIZE
        temp = run_train_episode(agent, env, rpm)  # 返回值现在为5个元素，这里不需要处理

    max_episode = args.max_episode          # 获取最大训练周期数

    # start training 开始训练代理
    episode = 0
    episodes = []  # 存储episode数
    rewards = []  # 存储reward值
    
    # 新增：用于收集每100集的指标
    detect_rates_100 = []  # 每100集的平均探测率
    lost_probs_100 = []    # 每100集的连续丢失概率 (发生连续丢失的集数占比)
    switch_rates_100 = []  # 每100集的平均切换率
    episodes_100 = []      # 标记点 (100, 200, 300, ...)
    
    # 用于临时存储100集的数据
    temp_detect_rates = []
    temp_lost_probs = []
    temp_switch_rates = []
    
    # 初始化episode_steps和episode_actions列表
    episode_steps = [0] * (max_episode + 1)
    episode_actions = [0] * (max_episode + 1)

    while episode < max_episode:
        episode += 1
        total_reward, episode_actions[episode], detect_rate, lost_prob, switch_rate = run_train_episode(agent, env, rpm)
        episode_steps[episode] = episode
        print("episode: " + str(episode) + " reward: " + str(total_reward))
        # 当前episode的reward记录
        rewards.append(total_reward)
        # 记录episode编号
        episodes.append(episode)
        
        # 新增：收集当前episode的指标
        temp_detect_rates.append(detect_rate)
        temp_lost_probs.append(lost_prob)
        temp_switch_rates.append(switch_rate)
        
        # 每100集计算和记录指标
        if episode % 100 == 0:
            avg_detect_rate = np.mean(temp_detect_rates)
            avg_lost_prob = np.mean(temp_lost_probs)  # 平均丢失概率
            avg_switch_rate = np.mean(temp_switch_rates)
            
            detect_rates_100.append(avg_detect_rate)
            lost_probs_100.append(avg_lost_prob)
            switch_rates_100.append(avg_switch_rate)
            episodes_100.append(episode)
            
            print(f"[Episode {episode}] 探测率: {avg_detect_rate:.4f}, 丢失概率: {avg_lost_prob:.4f}, 切换率: {avg_switch_rate:.4f}")
            
            # 清空临时列表
            temp_detect_rates = []
            temp_lost_probs = []
            temp_switch_rates = []

    print('episode:')
    print(episodes)
    print('Reward:')
    print(rewards)
    
    # 绘制原始奖励曲线
    plt.figure(figsize=(15, 12))
    
    # 第一个子图：奖励曲线
    plt.subplot(2, 2, 1)
    plt.plot(episodes, rewards, linestyle='-', color='b', linewidth=1)
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.title('Training Reward per Episode')
    plt.grid(True, alpha=0.3)
    
    # 第二个子图：每100集的探测成功率
    plt.subplot(2, 2, 2)
    plt.plot(episodes_100, detect_rates_100, marker='o', linestyle='-', color='g', linewidth=2)
    plt.xlabel('Episode (per 100)')
    plt.ylabel('Detection Rate')
    plt.title('1 Detection Rate (every 100 episodes)')
    plt.ylim([0, 1.05])
    plt.grid(True, alpha=0.3)
    for i, (ep, rate) in enumerate(zip(episodes_100, detect_rates_100)):
        plt.text(ep, rate + 0.02, f'{rate:.3f}', ha='center', fontsize=9)
    
    # 第三个子图：每100集的连续丢失概率
    plt.subplot(2, 2, 3)
    plt.plot(episodes_100, lost_probs_100, marker='s', linestyle='-', color='r', linewidth=2)
    plt.xlabel('Episode (per 100)')
    plt.ylabel('Lost Probability')
    plt.title('2 Continuous Loss Probability (every 100 episodes)')
    plt.ylim([0, 1.05])
    plt.grid(True, alpha=0.3)
    for i, (ep, prob) in enumerate(zip(episodes_100, lost_probs_100)):
        plt.text(ep, prob + 0.02, f'{prob:.3f}', ha='center', fontsize=9)
    
    # 第四个子图：每100集的切换率
    plt.subplot(2, 2, 4)
    plt.plot(episodes_100, switch_rates_100, marker='^', linestyle='-', color='orange', linewidth=2)
    plt.xlabel('Episode (per 100)')
    plt.ylabel('Switch Rate')
    plt.title('3 Switch Rate (every 100 episodes)')
    plt.ylim([0, max(switch_rates_100) * 1.2 if switch_rates_100 else 0.5])
    plt.grid(True, alpha=0.3)
    for i, (ep, rate) in enumerate(zip(episodes_100, switch_rates_100)):
        plt.text(ep, rate + max(switch_rates_100) * 0.02 if switch_rates_100 else 0.02, f'{rate:.3f}', ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('./training_metrics.png', dpi=150, bbox_inches='tight')
    print("\n✅ 训练指标图已保存为: ./training_metrics.png")
    plt.show()

    # 原始的传感器动作散点图
    plt.figure(figsize=(12, 4))
    plt.scatter(episode_steps, episode_actions, marker='.', color='r', alpha=0.5)
    plt.xlabel('Episode')
    plt.ylabel('Sensor ID')
    plt.title('Sensor Actions Over Episodes')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('./sensor_actions.png', dpi=150, bbox_inches='tight')
    print("✅ 传感器动作图已保存为: ./sensor_actions.png")
    plt.show()
    # train part
    # for i in range(10):     # 内循环，每次训练运行50个训练周期
    #     total_reward = run_train_episode(agent, env, rpm)       # 运行一个训练周期，返回该周期内获得的总奖励
    #     episode += 1            # 递增训练周期计数

    # save the parameters to ./model.ckpt   保存模型参数
    save_path = './model.ckpt'              # 保存路径
    agent.save(save_path)                   # 保存代理的模型参数

    # save the model and parameters of policy network for inference         保存用于推理的模型和参数
    save_inference_path = './inference_model'                       # 保存用于推理的模型参数路径
    input_shapes = [[None, env.observation_space.shape[0]]]         # 定义输入的形状
    input_dtypes = ['float32']                                       # 定义输入的数据类型
    agent.save_inference_model(save_inference_path, input_shapes, input_dtypes)     # 保存用于推理的模型和参数


if __name__ == '__main__':      # # 检查脚本是否被直接运行
    parser = argparse.ArgumentParser()      # 创建一个参数解析器对象，用于解析命令行参数
    parser.add_argument(                 # 添加一个命令行参数
        '--max_episode',
        type=int,
        default=16000,
        help='stop condition: number of max episode')
    args = parser.parse_args()          # 解析命令行参数

    main()          # 调用主函数进行训练和评估
