#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证脚本：检查仿真环境是否正常配置
"""

import os
import sys

def check_environment():
    """检查环境配置"""
    print("\n" + "="*60)
    print("SIMULATION ENVIRONMENT VERIFICATION")
    print("="*60)
    
    checks_passed = 0
    checks_total = 0
    
    # 检查 1：当前目录
    print("\n[1] Current Directory")
    cwd = os.getcwd()
    print(f"    Working directory: {cwd}")
    if "simulation" in cwd:
        print("    [OK] Running from simulation directory")
        checks_passed += 1
    else:
        print("    [WARNING] Not in simulation directory")
    checks_total += 1
    
    # 检查 2：Python 版本
    print("\n[2] Python Version")
    version = sys.version
    print(f"    {version}")
    if sys.version_info.major >= 3 and sys.version_info.minor >= 6:
        print("    [OK] Python version compatible")
        checks_passed += 1
    else:
        print("    [ERROR] Python 3.6+ required")
    checks_total += 1
    
    # 检查 3：必需模块
    print("\n[3] Required Modules")
    required_modules = ['numpy', 'matplotlib', 'paddle', 'parl']
    for module in required_modules:
        try:
            __import__(module)
            print(f"    [OK] {module}")
            checks_passed += 1
        except ImportError:
            print(f"    [ERROR] {module} not found")
        checks_total += 1
    
    # 检查 4：项目模块
    print("\n[4] Project Modules")
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    
    project_modules = ['Envir', 'cartpole_model', 'cartpole_agent']
    for module in project_modules:
        try:
            __import__(module)
            print(f"    [OK] {module}")
            checks_passed += 1
        except ImportError as e:
            print(f"    [ERROR] {module}: {e}")
        checks_total += 1
    
    # 检查 5：模型文件
    print("\n[5] Model File")
    model_path = os.path.join(parent_dir, "model.ckpt")
    if os.path.exists(model_path) or os.path.exists(model_path + ".pdparams"):
        print(f"    [OK] Model found at {model_path}")
        checks_passed += 1
    else:
        print(f"    [WARNING] Model not found at {model_path}")
        print("             This is OK - will use random model for testing")
    checks_total += 1
    
    # 检查 6：本地脚本
    print("\n[6] Local Scripts")
    scripts = ['quick_simulate.py', 'simulate_and_visualize.py', 'launcher.py']
    for script in scripts:
        if os.path.exists(script):
            print(f"    [OK] {script}")
            checks_passed += 1
        else:
            print(f"    [ERROR] {script} not found")
        checks_total += 1
    
    # 检查 7：虚拟环境
    print("\n[7] Virtual Environment")
    venv_path = os.path.join(parent_dir, "parl-env")
    if os.path.exists(venv_path):
        print(f"    [OK] Virtual environment found at {venv_path}")
        checks_passed += 1
    else:
        print(f"    [WARNING] Virtual environment not found at {venv_path}")
    checks_total += 1
    
    # 总结
    print("\n" + "="*60)
    print(f"SUMMARY: {checks_passed}/{checks_total} checks passed")
    print("="*60)
    
    if checks_passed >= checks_total - 1:  # 允许一个可选检查失败
        print("\n[SUCCESS] Environment is ready for simulation!")
        print("\nYou can now run:")
        print("  - python quick_simulate.py")
        print("  - python simulate_and_visualize.py")
        print("  - python launcher.py")
        return True
    else:
        print("\n[ERROR] Some critical checks failed!")
        return False

def quick_test():
    """快速功能测试"""
    print("\n" + "="*60)
    print("QUICK FUNCTIONALITY TEST")
    print("="*60)
    
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    
    try:
        print("\n[1] Importing modules...")
        from Envir import Env
        from cartpole_model import CartpoleModel
        from cartpole_agent import CartpoleAgent
        from parl.algorithms import DQN
        print("    [OK] All imports successful")
        
        print("\n[2] Creating environment...")
        env = Env(seed=42)
        print("    [OK] Environment created")
        print(f"    [INFO] Sensors detected: {len(env.sensors)}, act_dim: {env.act_dim}")
        
        print("\n[3] Creating agent...")
        obs_dim = 6  # 固定：[x, y, x_prev, y_prev, last_action, lost_flag]
        act_dim = env.act_dim  # 从环境自动读取传感器数量
        model = CartpoleModel(obs_dim=obs_dim, act_dim=act_dim)
        alg = DQN(model, gamma=0.95, lr=0.001)
        agent = CartpoleAgent(alg, act_dim=act_dim, e_greed=0.0, e_greed_decrement=0.0)
        print("    [OK] Agent created")
        
        print("\n[4] Running 10-step simulation...")
        obs = env.reset()
        total_reward = 0
        for step in range(10):
            action = agent.predict(obs)
            obs, reward, done, info = env.step(action)
            total_reward += reward
            if done:
                break
        print(f"    [OK] Simulation successful (total reward: {total_reward:.2f})")
        
        print("\n" + "="*60)
        print("[SUCCESS] All functionality tests passed!")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n    [ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("\nSimulation Environment Checker")
    print("==============================\n")
    
    # 环境检查
    env_ok = check_environment()
    
    # 功能测试
    if env_ok:
        func_ok = quick_test()
        if func_ok:
            print("\n" + "*"*60)
            print("* READY TO USE!")
            print("* Run: python quick_simulate.py")
            print("*"*60 + "\n")
    
    input("Press Enter to exit...")
