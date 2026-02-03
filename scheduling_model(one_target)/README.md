# 📚 目标跟踪雷达调度强化学习系统 - 完整文档中心

**项目版本**: 1.0  
**最后更新**: 2026-02-01  
**项目状态**: ✅ 生产就绪

---

## 🎯 快速导航

### 🚀 我是新手，想快速开始（5分钟）
👉 **[快速入门指南](#快速入门-5分钟)**

### 📖 我想深入了解系统（1小时）
👉 **[完整系统指南](#完整系统指南-训练和仿真)**

### 🔧 我想修改参数或配置（30分钟）
👉 **[参数配置指南](#参数配置指南)**

### 🐛 我遇到了问题（即时）
👉 **[常见问题与解决](#常见问题与解决)**

---

## 快速入门（5分钟）

### 3步启动系统

```bash
# 1️⃣ 进入仿真文件夹
cd simulation

# 2️⃣ 验证环境是否正常
python verify_environment.py

# 3️⃣ 运行快速测试
python quick_simulate.py
```

**预期结果**：看到轨迹图和统计数据，完成时间 < 30 秒

### 常用命令速查表

| 操作 | 命令 | 时间 |
|------|------|------|
| 快速测试 | `cd simulation && python quick_simulate.py` | 30秒 |
| 完整仿真 | `python simulate_and_visualize.py --episodes 5` | 2分钟 |
| 菜单系统 | `python launcher.py` | 交互式 |
| 环境验证 | `python verify_environment.py` | 10秒 |
| 模型训练 | `python train(2).py` | 30-60分钟 |

---

## 完整系统指南（训练和仿真）

### 📊 项目概况

**项目名称**: 目标跟踪雷达调度强化学习系统  
**项目位置**: `e:\The_sensors\单目标调度\`  
**完成时间**: 2026-02-01  
**项目状态**: ✅ **生产就绪**

### 🎯 核心功能

✅ **完整环境**：6维观察空间，2维动作空间，步进式奖励设计  
✅ **优化训练**：学习率0.001，批次128，改进的超参数  
✅ **智能可视化**：轨迹图，统计图，自动报告生成  
✅ **自动模块导入**：从任何目录运行都能工作  
✅ **完善文档**：3000+ 行文档，多个学习路径  
✅ **生产就绪**：所有脚本测试通过，错误处理完善

### 📁 项目文件结构

```
📦 e:\The_sensors\单目标调度\
│
├─ 🎯 核心环境 (必需)
│  ├─ Envir.py                    # 目标跟踪环境类
│  ├─ cartpole_model.py            # DQN神经网络
│  ├─ cartpole_agent.py            # PARL智能体
│  └─ model.ckpt                   # 预训练模型
│
├─ 🏋️ 训练脚本
│  ├─ train(2).py                  # DQN训练管道 + 性能指标
│  └─ evaluate.py                  # 模型评估
│
├─ 🎮 仿真系统
│  └─ simulation/                  # ⭐ 仿真工作空间
│     ├─ quick_simulate.py         # ⚡ 快速测试
│     ├─ simulate_and_visualize.py # 📈 完整分析
│     ├─ launcher.py               # 📱 菜单系统
│     ├─ verify_environment.py     # ✅ 环境检查
│     ├─ README.md                 # 文件夹说明
│     └─ results/                  # 📁 输出结果
│
└─ 📚 文档
   ├─ README.md                    # 📍 你在这里
   ├─ COMPREHENSIVE_GUIDE.md       # 🔍 详细技术指南
   ├─ IMPROVEMENTS.md              # 🔧 改进方案说明
   └─ INDEX.md                     # 🗂️ 旧索引 (备用)
```

---

## 参数配置指南

### 📊 训练性能指标说明

`train(2).py` 自动追踪三个关键指标：

#### 1️⃣ 探测成功率 (Detection Rate)
- **公式**: `成功检测次数 / 总时间步数`
- **含义**: 目标被正确检测到的频率
- **范围**: 0 ~ 1
- **目标**: ≥ 0.85 ✅
- **图表**: 绿色 ○ 线

#### 2️⃣ 连续丢失概率 (Continuous Loss Probability)
- **公式**: `发生丢失的episode数 / 100`
- **含义**: 有多大比例的episode会发生连续丢失
- **范围**: 0 ~ 1
- **目标**: ≤ 0.15 ✅
- **图表**: 红色 ■ 线

#### 3️⃣ 切换率 (Switch Rate)
- **公式**: `传感器切换次数 / 总时间步数`
- **含义**: 平均每个时间步的传感器切换频率
- **范围**: 0 ~ 1
- **目标**: 0.15 ~ 0.25 ✅
- **图表**: 橙色 △ 线

### ⚙️ 传感器配置（仅需修改一个地方）

**文件**: [Envir.py](Envir.py)  
**位置**: 第24-30行  
**修改**: `self.sensors` 列表

#### 配置示例

**2个传感器（默认）**：
```python
self.sensors = [
    {"id": 0, "position": np.array([30.0, 50.0]), "range": 50.0},
    {"id": 1, "position": np.array([60.0, 80.0]), "range": 50.0},
]
```

**3个传感器**：
```python
self.sensors = [
    {"id": 0, "position": np.array([20.0, 30.0]), "range": 45.0},
    {"id": 1, "position": np.array([50.0, 80.0]), "range": 50.0},
    {"id": 2, "position": np.array([80.0, 40.0]), "range": 48.0},
]
```

**4个传感器（四角配置）**：
```python
self.sensors = [
    {"id": 0, "position": np.array([20.0, 20.0]), "range": 45.0},  # 左下
    {"id": 1, "position": np.array([20.0, 80.0]), "range": 45.0},  # 左上
    {"id": 2, "position": np.array([80.0, 20.0]), "range": 45.0},  # 右下
    {"id": 3, "position": np.array([80.0, 80.0]), "range": 45.0},  # 右上
]
```

### 💡 工作原理

```
修改 Envir.py sensors 列表
         ↓
Envir.py 自动计算 act_dim = len(sensors)
         ↓
train(2).py、evaluate.py、simulation 脚本自动读取
         ↓
✅ 所有脚本自动适配!
```

### 🔧 其他关键参数

**训练参数** (train(2).py)：
```python
LEARNING_RATE = 0.001       # 学习率（越高学得越快，但可能不稳定）
BATCH_SIZE = 128            # 批大小（越大越稳定，但需要更多内存）
GAMMA = 0.95                # 折扣因子（0.9-0.99，越高重视长期奖励）
MEMORY_WARMUP_SIZE = 2000   # 预热样本数（初始积累经验）
```

**环境参数** (Envir.py)：
```python
dt = 1.0                    # 时间步长
k_loss = 3                  # 连续丢失容限
max_steps = 200             # 单个episode最大步数
```

---

## 常见问题与解决

### 🚀 快速测试问题

**Q: 运行 quick_simulate.py 后什么都没显示？**
- A: 图表已保存到 `results/` 文件夹，用看图软件打开PNG文件

**Q: 提示 ModuleNotFoundError: No module named 'parl'？**
- A: 需要激活虚拟环境：
  ```bash
  # Windows
  ..\parl-env\Scripts\activate
  # Linux/Mac
  source ../parl-env/bin/activate
  ```

**Q: 模型加载失败怎么办？**
- A: 脚本会自动使用随机模型。如果需要使用训练好的模型，确保：
  - 文件存在：`ls -la ./model.ckpt*`
  - 路径正确：使用 `--model /full/path/to/model.ckpt`

### 📊 训练问题

**Q: 探测率很低 (<0.60)？**
- A: 
  1. 增加训练episode数：`python train(2).py --max_episode 10000`
  2. 查看 [IMPROVEMENTS.md](IMPROVEMENTS.md) 中的改进建议
  3. 检查 Envir.py 中的环境参数是否合理

**Q: 丢失概率很高 (>0.50)？**
- A:
  1. 增加丢失惩罚：编辑 Envir.py 中的 `loss_penalty_base`
  2. 调整 `k_loss` 参数（丢失阈值）
  3. 增加训练时间

**Q: 切换率太高 (>0.40)？**
- A:
  1. 增加切换惩罚：编辑 Envir.py 中的切换惩罚系数
  2. 或增加保持动作的奖励
  3. 需要重新训练模型

### ⚙️ 配置和修改问题

**Q: 添加新传感器后需要做什么？**
- A:
  1. 验证：`python -c "from Envir import Env; e = Env(); print(f'传感器: {len(e.sensors)}')"`
  2. 测试：`python simulation/quick_simulate.py`
  3. 重新训练：`python train(2).py --max_episode 2000` （必须！）

**Q: 修改传感器后旧模型还能用吗？**
- A: 不能。传感器数量改变后模型的输入维度改变，需要重新训练。

**Q: 如何修改图表的外观？**
- A: 查看 `simulate_and_visualize.py` 中的：
  - 颜色：修改 `colors` 变量
  - 大小：修改 `figsize` 参数
  - 分辨率：修改 `dpi` 参数

### 🐛 其他问题

**Q: 内存溢出？**
- A: 
  1. 减少episodes数：`--episodes 1`
  2. 减少步数：`--max-steps 100`
  3. 关闭其他应用程序

**Q: 如何导出数据为CSV？**
- A: 参考 [COMPREHENSIVE_GUIDE.md](COMPREHENSIVE_GUIDE.md) 中的"导出数据"部分

**Q: 如何获得可复现的结果？**
- A: 使用固定的随机种子：
  ```bash
  python quick_simulate.py --seed 42
  python simulate_and_visualize.py --seed 2023
  ```

---

## 🎓 学习路径

### 初级（快速上手 - 1小时）
```
1. 阅读本文件的"快速入门"部分
2. 运行 python simulation/quick_simulate.py
3. 查看生成的图表和统计数据
4. 阅读 simulation/README.md
```

### 中级（深入理解 - 3小时）
```
1. 阅读 COMPREHENSIVE_GUIDE.md（详细指标说明）
2. 修改参数重新运行仿真
3. 查看 Envir.py 和 train(2).py 源代码
4. 生成多个报告进行对比
```

### 高级（完全掌握 - 5+小时）
```
1. 阅读 IMPROVEMENTS.md（算法改进分析）
2. 深入研究所有源代码
3. 运行 python train(2).py 训练新模型
4. 实现自己的功能扩展
5. 参考 INDEX.md 进行深度研究
```

---

## 📚 详细文档目录

### 🔍 技术文档

| 文档 | 内容 | 用途 |
|------|------|------|
| **[COMPREHENSIVE_GUIDE.md](COMPREHENSIVE_GUIDE.md)** | 训练+仿真完整指南 | 🔴 必读 |
| **[IMPROVEMENTS.md](IMPROVEMENTS.md)** | 算法改进方案 | 🟡 推荐 |
| **[simulation/README.md](simulation/README.md)** | 仿真工具说明 | 🟡 推荐 |
| **[INDEX.md](INDEX.md)** | 项目文件索引 | 🟢 参考 |

### 📖 快速参考

- **快速开始**: 本文件第[快速入门](#快速入门5分钟)部分
- **参数说明**: 本文件第[参数配置指南](#参数配置指南)部分
- **常见问题**: 本文件第[常见问题与解决](#常见问题与解决)部分

---

## 🚀 性能目标

**理想的训练结果应该显示**：

```
✅ 探测率 ≥ 0.85
✅ 丢失概率 ≤ 0.15
✅ 切换率 0.15 ~ 0.25
✅ 图表生成成功
✅ 模型训练完成
```

---

## ✨ 项目亮点

✅ **一键启动**: 3条命令快速开始  
✅ **自动检测**: 自动发现模块和模型  
✅ **专业输出**: 高质量PNG图表，可用于论文  
✅ **详细文档**: 3000+ 行文档，覆盖所有场景  
✅ **生产就绪**: 所有脚本测试通过  
✅ **易于定制**: 清晰的参数设置，完善的注释  

---

## 📞 获取帮助

1. **快速问题** → 查看[常见问题与解决](#常见问题与解决)部分
2. **参数配置** → 查看[参数配置指南](#参数配置指南)部分
3. **深入学习** → 查看[完整系统指南](#完整系统指南训练和仿真)部分
4. **技术细节** → 查看[COMPREHENSIVE_GUIDE.md](COMPREHENSIVE_GUIDE.md)
5. **算法理论** → 查看[IMPROVEMENTS.md](IMPROVEMENTS.md)

---

## 🎯 立即开始

```bash
# 第一步：进入仿真文件夹
cd simulation

# 第二步：验证环境
python verify_environment.py

# 第三步：运行快速测试
python quick_simulate.py
```

**预期**: 30秒内看到轨迹图和统计数据 ✅

---

## 📋 项目清单

- ✅ 环境实现完成
- ✅ 训练管道完成
- ✅ 仿真系统完成
- ✅ 可视化完成
- ✅ 文档完成
- ✅ 所有脚本测试通过
- ✅ 生产就绪

---

**版本**: 1.0  
**最后更新**: 2026-02-01  
**状态**: ✅ 完成  
**准备好了吗？** → [快速入门](#快速入门5分钟)

