# 仿真脚本使用指南

## 📁 文件结构
```
simulation/
├── quick_simulate.py              # 快速测试脚本
├── simulate_and_visualize.py      # 完整仿真脚本
├── README.md                      # 本文件
└── results/                       # 输出结果目录（自动创建）
    ├── episode_01_trajectory.png
    ├── episode_01_statistics.png
    └── ...
```

## 🚀 快速开始

### 方式1：快速测试（推荐）
在 simulation 文件夹中运行：
```bash
cd simulation
python quick_simulate.py
```

**效果**：
- 实时显示目标轨迹和传感器位置
- 显示奖励曲线和累积奖励
- 输出性能统计数据
- 无需保存文件，快速反馈

### 方式2：完整仿真报告
```bash
cd simulation
python simulate_and_visualize.py --episodes 3 --max-steps 200
```

**效果**：
- 运行多个 episodes
- 生成详细的可视化图表
- 保存到 `results/` 文件夹
- 生成性能对比图表

---

## 💻 常用命令

### 快速测试脚本命令
```bash
# 使用默认模型
python quick_simulate.py

# 指定最大步数
python quick_simulate.py --max-steps 300

# 使用固定随机种子（可复现）
python quick_simulate.py --seed 42

# 指定模型文件
python quick_simulate.py --model model.ckpt
```

### 完整仿真脚本命令
```bash
# 基本运行
python simulate_and_visualize.py

# 运行5个episodes，每个200步
python simulate_and_visualize.py --episodes 5 --max-steps 200

# 保存到自定义文件夹
python simulate_and_visualize.py --save-dir ./my_results

# 可复现的实验（使用固定种子）
python simulate_and_visualize.py --seed 2023 --episodes 10

# 完整示例
python simulate_and_visualize.py \
  --model model.ckpt \
  --episodes 3 \
  --max-steps 300 \
  --seed 42 \
  --save-dir ./experiment_results \
  --show
```

---

## 📊 输出说明

### 快速测试输出
```
[OK] Model loaded from e:\The_sensors\单目标调度\model.ckpt
Running simulation...
  Step  50: reward=12.34, cumsum=234.56
  Step 100: reward=8.90, cumsum=567.89
  Episode ended at step 125

==================================================
STATISTICS
==================================================
Total steps: 125
Total reward: 1234.56
Avg reward: 9.88
Detection rate: 85.6%

Radar usage:
  Radar 0: 45 times (36.0%)
  Radar 1: 80 times (64.0%)

Radar 0 detection rate: 88.9%
Radar 1 detection rate: 83.8%
==================================================
```

### 完整仿真输出文件

**trajectory.png** - 轨迹图：
- 蓝色圆：Radar 0 覆盖范围
- 青色圆：Radar 1 覆盖范围
- 彩色点：目标位置（着色表示使用的传感器）
- 虚线：目标运动轨迹

**statistics.png** - 统计图（4个子图）：
- 左上：每步奖励
- 右上：累积奖励
- 左下：选择的传感器序列
- 右下：检测率（10步滑动窗口）

**episodes_comparison.png** - 多episode对比图：
- 柱状图显示每个episode的总奖励
- 便于对比不同runs的性能

---

## 🔧 参数详解

### quick_simulate.py 参数
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--model` | str | `model.ckpt` | 模型文件名 |
| `--max-steps` | int | 200 | 每个episode最多步数 |
| `--seed` | int | None | 随机种子 |

### simulate_and_visualize.py 参数
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--model` | str | `model.ckpt` | 模型文件名 |
| `--episodes` | int | 3 | 仿真episode数 |
| `--max-steps` | int | 200 | 每个episode最多步数 |
| `--seed` | int | None | 随机种子 |
| `--save-dir` | str | `./results` | 输出文件夹 |
| `--show` | flag | False | 显示图表 |

---

## ⚙️ 模型查找机制

脚本会自动在项目根目录查找模型文件：
```
e:\The_sensors\单目标调度\
├── model.ckpt              # ← 脚本会在这里查找
├── model.ckpt.pdparams
├── model.ckpt.pdopt
├── simulation/
│   ├── quick_simulate.py
│   └── simulate_and_visualize.py
```

### 模型路径说明
- 脚本会自动将模型文件名转换为绝对路径
- 支持的模型文件：`model.ckpt`（会自动查找 `.pdparams` 和 `.pdopt` 后缀）
- 如果找不到模型，脚本会使用随机初始化的模型继续运行

---

## 🐛 常见问题

### Q1: ModuleNotFoundError: No module named 'parl'
**解决**：需要激活虚拟环境
```bash
# Windows
..\parl-env\Scripts\activate

# Linux/Mac
source ../parl-env/bin/activate

# 然后运行脚本
python quick_simulate.py
```

### Q2: 模型加载失败，如何处理？
**解决**：脚本会自动降级到随机模型，继续仿真
```
[WARNING] Model not found at e:\The_sensors\单目标调度\model.ckpt
[INFO] Using random agent
```
这是正常的，说明还没有训练模型。模型训练后会自动加载。

### Q3: 图表显示为空白？
**解决**：
- 确保已安装 matplotlib
- 尝试添加 `--show` 参数强制显示
- 或检查 `results/` 文件夹中的 PNG 文件

### Q4: 如何保存仿真视频？
**解决**：目前不支持直接生成视频，但可以：
1. 运行完整仿真脚本生成图表序列
2. 使用 FFmpeg 等工具将图表转换为视频

---

## 📈 实验建议

### 对模型效果的初步评估
```bash
python quick_simulate.py --seed 42 --max-steps 300
```
检查：
- 检测率是否 > 80%
- 总奖励是否为正数
- 是否频繁切换传感器

### 多run实验对比
```bash
python simulate_and_visualize.py \
  --episodes 20 \
  --seed 2023 \
  --save-dir ./experiment_001
```
分析：
- 不同episodes的性能差异
- 模型的稳定性
- 平均性能指标

### 压力测试（长期追踪）
```bash
python simulate_and_visualize.py \
  --episodes 1 \
  --max-steps 500 \
  --seed 42
```
检查：
- 模型能否长时间保持目标追踪
- 是否会崩溃或性能急剧下降

---

## 🎓 进阶用法

### 修改仿真参数
编辑 `Envir.py` 中的环境参数：
```python
# 修改传感器位置/范围
self.sensors = [
    {"id": 0, "position": np.array([0.0, 50.0]), "range": 60.0},  # 改为60
    {"id": 1, "position": np.array([100.0, 70.0]), "range": 50.0},
]
```

### 自定义输出格式
修改 `quick_simulate.py` 或 `simulate_and_visualize.py` 中的绘图函数以满足需求

### 批量运行实验
```python
# batch_experiment.py
import subprocess
for seed in range(10):
    cmd = f"python quick_simulate.py --seed {seed}"
    subprocess.run(cmd)
```

---

## 📞 技术支持

有问题时，请检查：
1. 是否激活了虚拟环境
2. 是否在 simulation 文件夹中运行
3. 模型文件是否存在于项目根目录
4. 依赖包是否已安装

详细文档参见上级目录的 `SIMULATION_GUIDE.md` 和 `SIMULATION_QUICK_START.md`
