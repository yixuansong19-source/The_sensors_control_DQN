# Simulation 文件夹说明

## 📂 文件结构

```
simulation/
├── __init__.py                    # Python 包初始化
├── quick_simulate.py              # 快速测试脚本（推荐新手）
├── simulate_and_visualize.py      # 完整仿真脚本
├── launcher.py                    # 菜单式启动器
├── run.bat                        # Windows 启动脚本
├── run.sh                         # Linux/Mac 启动脚本
├── README.md                      # 详细使用指南
└── results/                       # 输出目录（自动创建）
    ├── episode_01_trajectory.png
    ├── episode_01_statistics.png
    └── ...
```

## 🚀 快速使用

### Windows 用户
双击 `run.bat` 或在 cmd 中运行：
```bash
cd simulation
run.bat
```

### Linux/Mac 用户
在终端运行：
```bash
cd simulation
bash run.sh
```

### 所有平台
在 simulation 文件夹中使用 Python 直接运行：

**方式1：快速测试**
```bash
python quick_simulate.py
```

**方式2：完整仿真**
```bash
python simulate_and_visualize.py --episodes 3 --save-dir ./results
```

**方式3：菜单启动器**
```bash
python launcher.py
```

## 🔑 关键特性

### ✅ 自动路径处理
- 脚本自动查找项目根目录的 `model.ckpt`
- 无需手动修改路径
- 支持相对路径和绝对路径

### ✅ 模块导入
- 通过 `sys.path` 自动添加父目录
- 正确导入 `Envir`、`CartpoleModel` 等模块
- 即使模型不存在也能继续运行（使用随机模型）

### ✅ 灵活的输出
- 快速测试：实时显示图表，无文件保存
- 完整仿真：保存高分辨率 PNG 图表
- 支持多 episode 对比和统计

## 📖 使用示例

### 示例 1：快速验证模型
```bash
python quick_simulate.py --seed 42
```
**用途**：快速检查模型是否能正常运行
**输出**：轨迹图 + 奖励分析 + 统计数据

### 示例 2：生成实验报告
```bash
python simulate_and_visualize.py \
  --episodes 5 \
  --max-steps 250 \
  --seed 2023 \
  --save-dir ./exp_001
```
**用途**：生成详细的仿真报告
**输出**：5 个 episodes × 2 个图表 + 对比图 = 11 张图表

### 示例 3：交互式菜单
```bash
python launcher.py
```
**用途**：通过菜单选择不同的运行模式
**功能**：
- 快速测试
- 完整仿真
- 批量实验
- 打开结果文件夹

### 示例 4：批量实验
通过菜单启动器或直接脚本：
```bash
python launcher.py
# 选择选项 3 (Batch Experiment)
# 输入运行次数、参数等
```

## 🔍 文件说明

### quick_simulate.py
**用途**：快速验证模型效果
**特点**：
- 运行单个 episode
- 实时显示图表
- 快速反馈（无保存延迟）
- 适合快速调试

**输出**：
- 左图：目标轨迹 + 传感器位置
- 右图：奖励分析（双轴）
- 统计：总奖励、检测率、传感器使用频率

### simulate_and_visualize.py
**用途**：完整的仿真和分析
**特点**：
- 支持多 episodes
- 生成详细报告
- 高分辨率输出
- 支持结果对比

**输出**：
- trajectory.png：轨迹图
- statistics.png：4 个统计子图
- episodes_comparison.png：episode 对比
- 控制台统计摘要

### launcher.py
**用途**：交互式菜单启动器
**功能**：
1. 快速测试
2. 完整仿真
3. 批量实验（多 seed）
4. 打开结果文件夹
5. 退出

### run.bat / run.sh
**用途**：一键启动脚本
**功能**：
- 自动激活虚拟环境
- 显示菜单
- 执行选定的仿真模式

## ⚙️ 常用参数

### 所有脚本通用参数
```
--model <filename>      模型文件名（默认：model.ckpt）
--max-steps <int>       每个 episode 最多步数（默认：200）
--seed <int>            随机种子（用于可复现性）
```

### simulate_and_visualize.py 额外参数
```
--episodes <int>        仿真 episodes 数（默认：3）
--save-dir <path>       输出目录（默认：./results）
--show                  显示图表（可选标志）
```

## 🎯 工作流程

### 模型训练后的仿真流程
```
1. 完成模型训练（生成 model.ckpt）
   ↓
2. 进入 simulation 文件夹
   ↓
3. 运行 quick_simulate.py 快速检验
   ↓
4. 如果效果良好，运行 simulate_and_visualize.py 生成报告
   ↓
5. 分析结果并根据需要调参
```

## 🐛 故障排查

### 错误：ModuleNotFoundError
```
ModuleNotFoundError: No module named 'parl'
```
**解决**：需要激活虚拟环境
```bash
# Windows
..\parl-env\Scripts\activate.bat

# Linux/Mac
source ../parl-env/bin/activate
```

### 错误：model.ckpt not found
```
[WARNING] Model not found at ...
```
**解决**：这是正常的，脚本会使用随机模型继续
- 如果需要使用已训练的模型，确保 `model.ckpt` 在项目根目录

### 错误：图表为空白
**解决**：
- 尝试添加 `--show` 参数
- 检查 `results/` 文件夹中的 PNG 文件
- 确保已安装 matplotlib

## 📊 输出文件示例

### 快速测试
**实时显示**：
- 单个窗口，包含 2 个子图
- 左：轨迹图
- 右：奖励分析

### 完整仿真
```
results/
├── episode_01_trajectory.png       (1200×1000 px, 150 DPI)
├── episode_01_statistics.png       (1400×1000 px, 150 DPI)
├── episode_02_trajectory.png
├── episode_02_statistics.png
└── episodes_comparison.png         (1000×600 px, 150 DPI)
```

## 💡 最佳实践

### 对于模型评估
1. 使用固定 seed 进行可复现实验
2. 运行至少 10 个 episodes 以获得稳定的统计
3. 检查检测率、平均奖励等指标

### 对于性能对比
1. 在相同条件下测试不同模型
2. 使用相同的 seed 和参数
3. 保存结果到不同的文件夹便于对比

### 对于调参
1. 先用 `quick_simulate.py` 快速测试
2. 如果效果不理想，返回训练脚本调参
3. 重新训练模型并在 simulation 中测试

## 📝 相关文档

- [SIMULATION_GUIDE.md](../SIMULATION_GUIDE.md) - 详细的可视化和功能说明
- [SIMULATION_QUICK_START.md](../SIMULATION_QUICK_START.md) - 快速参考卡
- [IMPROVEMENTS.md](../IMPROVEMENTS.md) - 改进方案说明

## 🔄 后续改进

- [ ] 添加动画输出（MP4/GIF）
- [ ] 支持实时交互式看板（Plotly/Dash）
- [ ] 数据导出为 CSV/Excel
- [ ] 对接 TensorBoard 进行实时监控
- [ ] 支持多模型对比

---

**准备好了吗？现在就可以运行仿真脚本了！**

```bash
cd simulation
python quick_simulate.py
```
