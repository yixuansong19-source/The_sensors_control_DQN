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

import paddle
import paddle.nn as nn      # 导入了PaddlePaddle深度学习框架的神经网络模块。nn 模块包含了用于创建神经网络模型的类和函数，例如用于定义神经网络层的类和激活函数等
import paddle.nn.functional as F        # 导入了PaddlePaddle深度学习框架的 functional 模块，其中包含了一些用于进行深度学习操作的函数，例如激活函数、损失函数等。通过 F，你可以使用这些函数来构建和操作神经网络
import parl     # 导入了Parl（Parallel Reinforcement Learning）强化学习库。Parl是一个用于构建强化学习模型的Python库，它提供了一种简单且高度可扩展的方式来开发和训练强化学习代理。你可以使用Parl来实现各种强化学习算法

# 模型的目的是逼近状态-动作值函数，以便在强化学习任务中进行决策
class CartpoleModel(parl.Model):        # 继承自 parl.Model 的类，用于定义 Cartpole 问题的神经网络模型
    """ Linear network to solve Cartpole problem.

    Args:
        obs_dim (int): Dimension of observation space. #状态空间维度
        act_dim (int): Dimension of action space.   #动作空间维度
    """

    def __init__(self, obs_dim, act_dim):   # 构造函数用于初始化模型。它接受两个参数，obs_dim 表示观察空间的维度，act_dim 表示动作空间的维度
        super(CartpoleModel, self).__init__()       # 调用父类 parl.Model 的构造函数以初始化模型
        hid1_size = 256         # 定义第一个隐藏层的大小为 256（增加神经元数量）
        hid2_size = 256         # 定义第二个隐藏层的大小为 256
        hid3_size = 128         # 添加第三个隐藏层
        self.fc1 = nn.Linear(obs_dim, hid1_size)        # 创建一个全连接（线性）层，将输入维度为 obs_dim（观察空间的维度）映射到第一个隐藏层的大小
        self.fc2 = nn.Linear(hid1_size, hid2_size)      # 创建第二个全连接层，将第一个隐藏层的输出映射到第二个隐藏层的大小
        self.fc3 = nn.Linear(hid2_size, hid3_size)      # 创建第三个全连接层
        self.fc4 = nn.Linear(hid3_size, act_dim)        # 创建第四个全连接层，映射到动作空间的维度        输入->隐层->输出

    def forward(self, obs):     # 定义了前向传播方法，接受观察值 obs 作为输入，返回预测的状态-动作值函数 Q
        h1 = F.relu(self.fc1(obs))      # 首先将输入 obs 经过第一个全连接层，并应用 ReLU 激活函数。这将计算第一个隐藏层的激活值
        h2 = F.relu(self.fc2(h1))       # 然后将第一个隐藏层的激活值传递给第二个全连接层，并再次应用 ReLU 激活函数，计算第二个隐藏层的激活值
        h3 = F.relu(self.fc3(h2))       # 第三个隐藏层
        Q = self.fc4(h3)                # 最后，将第三个隐藏层的激活值传递给第四个全连接层，计算 Q 值，即状态-动作值函数
        return Q        # 输出