#   Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import parl
import paddle
import numpy as np


class CartpoleAgent(parl.Agent):        # 代理的实现，并继承自 parl.Agent 类；代理是一个决策者，它与环境互动，观察环境状态，采取动作，并获得奖励。代理的任务是通过学习来优化其策略，以获得最大的累积奖励
    """Agent of Cartpole env.       # 表明该代理是用于与 Cartpole 环境交互的代理

    Args:   # 列出构造函数的参数及其含义
        algorithm(parl.Algorithm): algorithm used to solve the problem. # 构造函数的一个参数，表示用于解决问题的强化学习算法。该参数将传递给代理，以指定它所使用的算法

    """

    def __init__(self, algorithm, act_dim, e_greed=0.1, e_greed_decrement=0):   # 初始化函数：用于解决问题的算法；动作空间的维度（整数）；ε-greedy策略的ε值，它的默认值是0.1；衰减值默认0
        super(CartpoleAgent, self).__init__(algorithm)  # 调用了父类 parl.Agent 的构造函数，以初始化代理。它将 algorithm 参数传递给父类的构造函数，这是用于实现代理行为的算法
        assert isinstance(act_dim, int) # 断言语句，用于检查 act_dim 是否是整数类型。如果 act_dim 不是整数，将引发AssertionError异常。这是一种有效的输入参数验证方式
        self.act_dim = act_dim  # 将传入的 act_dim 参数赋值给代理对象的 act_dim 成员变量，以便在后续的方法中使用

        self.global_step = 0    # 初始化代理的全局步数
        self.update_target_steps = 200  # 降低更新频率以稳定Q值估计

        self.e_greed = e_greed  # 初始ε值
        self.e_greed_decrement = e_greed_decrement  # ε衰减值

    def sample(self, obs):      # 采样一个动作，以进行探索，通常在ε-greedy策略中使用
        """Sample an action `for exploration` when given an observation     # 当给出观察结果时，对“探索”动作进行采样（采样一个动作，用于探索，根据给定的观察值

        Args:
            obs(np.float32): shape of (obs_dim,)    # 观察值，通常是一个形状为 (obs_dim,) 的NumPy数组

        Returns:
            act(int): action    #动作
        """
        sample = np.random.random()     # 从均匀分布中随机采样一个值（0到1之间）
        if sample < self.e_greed:       # 如果随机采样的值小于ε（epsilon），进行探索
            act = np.random.randint(self.act_dim)   # 随机选择一个动作 范围act_dim
        else:
            if np.random.random() < 0.01:       # 如果随机采样的值小于0.01，进行探索
                act = np.random.randint(self.act_dim)       # 随机选择一个动作
            else:                       # 否则，根据学到的策略预测动作（若以上两种都不满足
                act = self.predict(obs)         # 使用predict方法预测动作
        self.e_greed = max(0.01, self.e_greed - self.e_greed_decrement)     # 逐渐减小ε的值 确保代理在训练过程中逐渐依赖于学到的策略而不是随机探索
        return act                              # 返回选择的动作

    def predict(self, obs):     # 用于根据给定的观察值（状态）预测应该采取的动作
        """Predict an action when given an observation  # 根据给定的观察值预测一个动作

        Args:
            obs(np.float32): shape of (obs_dim,)    # 形状为 (obs_dim,) 的观察值

        Returns:
            act(int): action
        """
        obs = paddle.to_tensor(obs, dtype='float32')    # 将观察值转换为PaddlePaddle张量 以便与模型进行计算
        pred_q = self.alg.predict(obs)              # 使用算法预测给定观察值下动作的Q值
        act = int(pred_q.argmax())                  # 选择具有最高Q值的动作
        return act                                  # 返回选择的动作

    def learn(self, obs, act, reward, next_obs, terminal):          # 用于更新模型（通常是强化学习算法中的Q值函数）以适应一段时间内的观察和奖励数据
        """Update model with an episode data            # 使用一段时间内的观察和奖励数据更新模型

        Args:
            obs(np.float32): shape of (batch_size, obs_dim)     # 形状为 (batch_size, obs_dim) 的观察数据，表示一批观察序列
            act(np.int32): shape of (batch_size)
            reward(np.float32): shape of (batch_size)
            next_obs(np.float32): shape of (batch_size, obs_dim)
            terminal(np.float32): shape of (batch_size)         # 终止标志

        Returns:
            loss(float)     # 训练过程中的损失值

        """
        if self.global_step % self.update_target_steps == 0:
            self.alg.sync_target()          # 定期同步目标网络
        self.global_step += 1               # 更新全局步数

        act = np.expand_dims(act, axis=-1)                  # 扩展动作的维度
        reward = np.expand_dims(reward, axis=-1)           # 扩展奖励的维度
        terminal = np.expand_dims(terminal, axis=-1)        # 扩展终止标志的维度

        obs = paddle.to_tensor(obs, dtype='float32')         # 将观察数据转换为PaddlePaddle张量
        act = paddle.to_tensor(act, dtype='int32')
        reward = paddle.to_tensor(reward, dtype='float32')
        next_obs = paddle.to_tensor(next_obs, dtype='float32')
        terminal = paddle.to_tensor(terminal, dtype='float32')
        loss = self.alg.learn(obs, act, reward, next_obs, terminal)      # 使用算法（self.alg）学习，并获取训练过程中的损失值
        return float(loss)               # 返回损失值
    
    def load_model(self, model_path):
        """加载训练好的模型"""
        self.alg.model.set_state_dict(paddle.load(model_path))  # 假设 self.alg 是包含模型的算法