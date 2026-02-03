# 项目文档索引

本项目包含一个完整的强化学习目标跟踪系统，包括训练、评估和可视化模块。

## 📚 文档导航

### 🚀 快速开始
**新用户请从这里开始：**

1. **[SIMULATION_SETUP_COMPLETE.md](SIMULATION_SETUP_COMPLETE.md)** ⭐ START HERE
   - 仿真系统安装完成说明
   - 快速开始指南
   - 目录结构说明
   - 故障排除

2. **[simulation/README.md](simulation/README.md)**
   - simulation 文件夹的使用指南
   - 常用命令
   - 参数说明

### 📖 详细文档

3. **[SIMULATION_GUIDE.md](SIMULATION_GUIDE.md)**
   - 完整的功能说明
   - 图表解读
   - 自定义选项
   - 传感器观测说明

4. **[SIMULATION_QUICK_START.md](SIMULATION_QUICK_START.md)**
   - 快速参考卡
   - 常用场景示例
   - 进阶用法

5. **[IMPROVEMENTS.md](IMPROVEMENTS.md)**
   - 模型收敛性改进方案
   - 超参数优化说明
   - 奖励设计说明

### 🛠️ 设置与配置

6. **[simulation/SETUP_GUIDE.md](simulation/SETUP_GUIDE.md)**
   - 详细的设置说明
   - 文件说明
   - 自定义修改

## 📁 项目结构

```
单目标调度/
├── 📄 SIMULATION_SETUP_COMPLETE.md  ⭐ 从这里开始
├── 📄 SIMULATION_GUIDE.md
├── 📄 SIMULATION_QUICK_START.md
├── 📄 IMPROVEMENTS.md
├── 📄 SIMULATION_QUICK_START.md
│
├── 🐍 训练脚本
│   ├── train(2).py                 # 训练脚本
│   ├── cartpole_model.py           # 网络模型
│   ├── cartpole_agent.py           # 代理
│   └── Envir.py                    # 环境定义
│
├── 🐍 评估脚本
│   └── evaluate.py                 # 离线评估
│
├── 💾 模型文件
│   ├── model.ckpt                  # 模型检查点
│   ├── model.ckpt.pdparams         # 参数
│   └── model.ckpt.pdopt            # 优化器状态
│
└── 📁 simulation/                  # 仿真工作空间 ⭐ 新增
    ├── 📄 README.md                # 文件夹使用指南
    ├── 📄 SETUP_GUIDE.md           # 详细设置说明
    │
    ├── 🚀 启动脚本
    │   ├── quick_simulate.py       # 快速测试 ⭐ 推荐
    │   ├── simulate_and_visualize.py # 完整仿真 ⭐ 推荐
    │   ├── launcher.py             # 菜单启动器
    │   ├── verify_environment.py   # 环境验证
    │   ├── run.bat                 # Windows 启动脚本
    │   └── run.sh                  # Linux/Mac 启动脚本
    │
    ├── 📁 results/                 # 输出目录（自动创建）
    │   ├── episode_01_trajectory.png
    │   ├── episode_01_statistics.png
    │   └── ...
    │
    └── __init__.py
```

## 🎯 使用场景快速导航

### 场景 1：我是新手，想快速了解系统
```
1. 阅读：SIMULATION_SETUP_COMPLETE.md
2. 运行：python simulation/verify_environment.py
3. 尝试：python simulation/quick_simulate.py
```

### 场景 2：我想生成一份仿真报告
```
1. 阅读：simulation/README.md
2. 运行：python simulation/simulate_and_visualize.py --episodes 5
3. 查看：simulation/results/ 文件夹中的图表
```

### 场景 3：我想对比模型性能
```
1. 阅读：SIMULATION_QUICK_START.md
2. 运行：python simulation/launcher.py (选择选项3：批量实验)
3. 分析：对比多个 episodes 的性能
```

### 场景 4：我想修改仿真参数
```
1. 阅读：IMPROVEMENTS.md
2. 编辑：Envir.py 中的环境参数
3. 测试：python simulation/quick_simulate.py
4. 重新训练：python train(2).py
5. 验证：python simulation/simulate_and_visualize.py
```

### 场景 5：我想深入理解图表
```
1. 阅读：SIMULATION_GUIDE.md
2. 查看：各个图表的解读部分
3. 实验：修改绘图参数后重新运行
```

## 🔄 工作流程

### 开发流程
```
1. 修改环境参数 (Envir.py)
2. 重新训练模型 (train(2).py)
3. 快速测试 (simulation/quick_simulate.py)
4. 生成报告 (simulation/simulate_and_visualize.py)
5. 分析结果 (查看图表和统计数据)
6. 如果满意，进行下一步改进
```

### 发布流程
```
1. 确认模型效果满足要求
2. 运行完整仿真 (20+ episodes)
3. 生成最终报告到专门文件夹
4. 备份所有代码和模型
5. 准备文档和演示文件
```

## 📊 关键参数速查

### 训练参数 (train(2).py)
```
LEARN_FREQ = 10           # 训练频率
MEMORY_WARMUP_SIZE = 1000 # 预热大小
BATCH_SIZE = 128          # 批大小
LEARNING_RATE = 0.001     # 学习率
GAMMA = 0.95              # 折扣因子
```

### 环境参数 (Envir.py)
```
dt = 1.0                  # 时间步长
k_loss = 3                # 丢失容限
max_steps = 200           # 最大步数
loss_penalty_base = -5    # 基础惩罚
```

### 仿真参数
```
--episodes 3              # 仿真 episodes 数
--max-steps 200           # 每个 episode 最多步数
--seed 42                 # 随机种子
--save-dir ./results      # 输出目录
--show                    # 显示图表
```

## 🎓 学习资源

### 理论基础
- [IMPROVEMENTS.md](IMPROVEMENTS.md) - 强化学习基本概念和改进方案
- [simulation/SETUP_GUIDE.md](simulation/SETUP_GUIDE.md) - 系统架构说明

### 实践教程
- [SIMULATION_GUIDE.md](SIMULATION_GUIDE.md) - 完整功能演示
- [SIMULATION_QUICK_START.md](SIMULATION_QUICK_START.md) - 快速参考

### 代码示例
- `quick_simulate.py` - 简单示例（100 行）
- `simulate_and_visualize.py` - 完整示例（300 行）

## 🚀 快速命令

### 验证安装
```bash
cd simulation
python verify_environment.py
```

### 快速测试
```bash
cd simulation
python quick_simulate.py
```

### 完整仿真
```bash
cd simulation
python simulate_and_visualize.py --episodes 5 --seed 42
```

### 菜单启动器
```bash
cd simulation
python launcher.py
```

### 查看帮助
```bash
cd simulation
python quick_simulate.py --help
python simulate_and_visualize.py --help
```

## 🐛 常见问题

### Q: 哪个脚本最简单？
**A**: `quick_simulate.py` 最简单，直接显示图表，无需配置。

### Q: 如何保存结果？
**A**: 使用 `simulate_and_visualize.py`，结果自动保存到 `results/` 文件夹。

### Q: 模型在哪里？
**A**: 默认在项目根目录 `model.ckpt`。训练后自动生成。

### Q: 如何修改仿真参数？
**A**: 编辑 `Envir.py` 中的环境参数，见 [IMPROVEMENTS.md](IMPROVEMENTS.md)。

### Q: 可以运行多个 episodes 吗？
**A**: 可以，使用 `simulate_and_visualize.py --episodes N`。

### Q: 图表在哪里？
**A**: 保存在 `simulation/results/` 文件夹中（PNG 格式，可用任何看图软件打开）。

## 📞 获取帮助

1. 查看相应文档中的"常见问题"部分
2. 检查控制台输出的错误信息
3. 运行 `verify_environment.py` 检查环境配置
4. 查看各脚本的 `--help` 参数

## 📈 下一步建议

### 如果模型效果良好
```
1. 增加训练 episodes 数
2. 运行长期仿真（max_steps=500+）
3. 进行压力测试
4. 准备演示和报告
```

### 如果模型效果不理想
```
1. 检查 IMPROVEMENTS.md 中的改进建议
2. 调整超参数 (学习率、折扣因子等)
3. 修改奖励设计
4. 重新训练并测试
```

### 如果想深入研究
```
1. 查看 cartpole_model.py 和 cartpole_agent.py
2. 学习 DQN 算法原理
3. 尝试其他强化学习算法（A3C、PPO等）
4. 考虑添加更复杂的传感器模型
```

---

## 📋 文件完整清单

| 文件 | 类型 | 用途 | 优先级 |
|------|------|------|--------|
| SIMULATION_SETUP_COMPLETE.md | 文档 | 系统安装完成说明 | 🔴 必读 |
| simulation/README.md | 文档 | 仿真文件夹使用指南 | 🔴 必读 |
| SIMULATION_GUIDE.md | 文档 | 完整功能文档 | 🟡 推荐 |
| SIMULATION_QUICK_START.md | 文档 | 快速参考卡 | 🟡 推荐 |
| IMPROVEMENTS.md | 文档 | 改进说明 | 🟡 推荐 |
| simulation/SETUP_GUIDE.md | 文档 | 详细设置说明 | 🟢 可选 |
| simulation/quick_simulate.py | 脚本 | 快速测试 | 🔴 必用 |
| simulation/simulate_and_visualize.py | 脚本 | 完整仿真 | 🟡 常用 |
| simulation/launcher.py | 脚本 | 菜单启动器 | 🟢 可选 |
| simulation/verify_environment.py | 脚本 | 环境验证 | 🔴 初次使用 |
| train(2).py | 脚本 | 训练 | 🟡 需要时用 |

---

**版本**：1.0  
**最后更新**：2026-02-01  
**状态**：✅ 安装完成，可正常使用

**建议**：首先阅读 [SIMULATION_SETUP_COMPLETE.md](SIMULATION_SETUP_COMPLETE.md)，然后运行 `simulation/verify_environment.py` 验证环境。
