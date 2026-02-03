import random
import numpy as np
from types import SimpleNamespace


class Env:
    """目标跟踪雷达调度环境（二维，z=0）。

    obs = [x_t, y_t, x_{t-1}, y_{t-1}, last_sensor_id, lost_flag]
    action: 0 或 1（两个雷达）
    """

    def __init__(self, dt=1.0, k_loss=3, max_steps=200, seed=42, loss_penalty_base=-5):
        self.dt = float(dt)
        self.k_loss = int(k_loss)
        self.max_steps = int(max_steps)
        self.loss_penalty_base = float(loss_penalty_base)  # 基础丢失惩罚（减半以改善收敛）

        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)

        # 两个固定雷达（只用xy）
        # 📝 添加传感器：直接在这个列表中添加新的字典即可
        # 格式: {"id": N, "position": np.array([x, y]), "range": range_value}
        self.sensors = [
            {"id": 0, "position": np.array([30.0, 50.0]), "range": 50.0},
            {"id": 1, "position": np.array([60.0, 80.0]), "range": 50.0},
            {"id": 2, "position": np.array([50.0, 30.0]), "range": 45.0},  # 示例：第3个传感器
        ]
        
        # 自动计算动作维度（等于传感器数量）
        self.act_dim = len(self.sensors)

        # 兼容训练脚本使用
        self.observation_space = SimpleNamespace(shape=(6,))

        # 内部状态将在 reset 中初始化

    def reset(self):
        # 随机生成初始位置，要求至少被一个雷达覆盖
        while True:
            x = random.uniform(0, 100)
            y = random.uniform(0, 100)
            pos = np.array([x, y])
            # 找到所有能观测到该位置的雷达
            detectable_sensors = []
            for s in self.sensors:
                if np.linalg.norm(pos - s["position"]) <= s["range"]:
                    detectable_sensors.append(s["id"])
            if detectable_sensors:
                break

        self.x_true = pos.copy()
        # 目标速度：随机生成（匀速直线）
        self.v_true = np.array([random.uniform(-5.0, 5.0), random.uniform(-5.0, 5.0)])

        # 初始动作：随机选择一个能观测到目标的传感器
        self.last_action = random.choice(detectable_sensors)
        # 上一次被观测到的位置（初始为当前真值）
        self.last_obs = self.x_true.copy()
        # 连续丢失计数
        self.lost_steps = 0
        self.t = 0

        prev_pos = self.x_true - self.v_true * self.dt
        obs = np.array([self.x_true[0], self.x_true[1], prev_pos[0], prev_pos[1], float(self.last_action), 0.0], dtype=np.float32)
        return obs

    def step(self, action: int):
        # 更新时间步
        self.t += 1
        # 更新真实位置
        self.x_true = self.x_true + self.v_true * self.dt

        # 观测判断（以所选雷达为准）
        sensor = self.sensors[int(action)]
        dist = np.linalg.norm(self.x_true - sensor["position"])
        detect = dist <= sensor["range"]

        # 改进的奖励设计：使用平滑的奖励函数
        reward = 0.0
        lost_flag = 0.0
        
        if detect:
            # 检测成功：基础奖励 + 距离奖励（距离越近奖励越多）
            reward = 10.0
            # 加入距离相关的微调奖励
            distance_bonus = max(0, (sensor["range"] - dist) / sensor["range"] * 2)
            reward += distance_bonus
            # 更新上次观测到的位置
            self.last_obs = self.x_true.copy()
            self.lost_steps = 0
            lost_flag = 0.0
        else:
            # 丢失惩罚：采用阶跃而非线性递增，避免过度惩罚
            if self.lost_steps == 0:
                reward = -2.0  # 第一次丢失：轻微惩罚
            elif self.lost_steps == 1:
                reward = -5.0  # 第二次丢失：中等惩罚
            else:
                reward = -8.0  # 之后：较大惩罚
            self.lost_steps += 1
            lost_flag = 1.0

        # 切换惩罚/奖励（降低权重）
        if self.last_action == action:
            reward += 2.0  # 保持动作有较小的鼓励
        else:
            reward += -3.0  # 切换动作有较小的惩罚

        # 终止条件：连续丢失超过 k_loss 或达到最大时间步
        done = False
        if self.lost_steps >= self.k_loss:
            done = True
        if self.t >= self.max_steps:
            done = True

        # 返回 obs：[x_t, y_t, x_{t-1}, y_{t-1}, last_sensor_id, lost_flag]
        obs = np.array([
            float(self.x_true[0]), float(self.x_true[1]),
            float(self.last_obs[0]), float(self.last_obs[1]),
            float(self.last_action),
            lost_flag
        ], dtype=np.float32)

        info = {"detect": bool(detect), "dist": float(dist), "lost_steps": int(self.lost_steps)}

        # 更新 last_action（用于下一步 obs 中的 last_sensor_id）
        self.last_action = int(action)

        return obs, float(reward), bool(done), info





