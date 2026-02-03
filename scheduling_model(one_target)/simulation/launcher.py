#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
启动脚本：菜单式界面选择运行模式
"""

import os
import sys
import subprocess

def show_menu():
    """显示菜单"""
    print("\n" + "="*60)
    print("RADAR TARGET TRACKING - SIMULATION LAUNCHER")
    print("="*60)
    print("1. Quick Test         [快速测试单个episode]")
    print("2. Full Simulation    [完整仿真多个episodes]")
    print("3. Batch Experiment   [批量实验（多个seeds）]")
    print("4. Open Results       [打开结果文件夹]")
    print("5. Exit               [退出]")
    print("="*60)
    print("💡 TIP: 修改 Envir.py 中的 sensors 列表即可添加/修改传感器")
    print("   所有仿真脚本都会自动适配新的传感器配置")
    print("="*60)

def run_quick_test():
    """运行快速测试"""
    print("\n--- Quick Test Configuration ---")
    max_steps = input("Max steps per episode (default 200): ").strip() or "200"
    seed = input("Random seed (default None): ").strip() or "None"
    
    cmd = f"python quick_simulate.py --max-steps {max_steps}"
    if seed != "None":
        cmd += f" --seed {seed}"
    
    print(f"\nRunning: {cmd}\n")
    subprocess.run(cmd, shell=True)

def run_full_simulation():
    """运行完整仿真"""
    print("\n--- Full Simulation Configuration ---")
    episodes = input("Number of episodes (default 3): ").strip() or "3"
    max_steps = input("Max steps per episode (default 200): ").strip() or "200"
    seed = input("Random seed (default None): ").strip() or "None"
    save_dir = input("Save directory (default ./results): ").strip() or "./results"
    show = input("Show plots? (y/n, default n): ").strip().lower() == 'y'
    
    cmd = f"python simulate_and_visualize.py --episodes {episodes} --max-steps {max_steps} --save-dir {save_dir}"
    if seed != "None":
        cmd += f" --seed {seed}"
    if show:
        cmd += " --show"
    
    print(f"\nRunning: {cmd}\n")
    subprocess.run(cmd, shell=True)

def run_batch_experiment():
    """运行批量实验"""
    print("\n--- Batch Experiment Configuration ---")
    num_runs = input("Number of runs (default 5): ").strip() or "5"
    max_steps = input("Max steps per episode (default 200): ").strip() or "200"
    base_dir = input("Base output directory (default ./batch_results): ").strip() or "./batch_results"
    
    print(f"\nRunning {num_runs} experiments...\n")
    
    for i in range(int(num_runs)):
        seed = i + 1
        save_dir = os.path.join(base_dir, f"run_{i+1:02d}")
        cmd = f"python simulate_and_visualize.py --episodes 1 --max-steps {max_steps} --seed {seed} --save-dir {save_dir}"
        print(f"[{i+1}/{num_runs}] Running: {cmd}")
        subprocess.run(cmd, shell=True)
        print()
    
    print(f"\nAll experiments completed. Results saved to: {base_dir}")
    print(f"Run: explorer {base_dir}")

def open_results():
    """打开结果文件夹"""
    results_dir = "./results"
    if os.path.exists(results_dir):
        if sys.platform == "win32":
            os.startfile(results_dir)
        elif sys.platform == "darwin":
            subprocess.run(["open", results_dir])
        else:
            subprocess.run(["xdg-open", results_dir])
        print(f"Opened: {os.path.abspath(results_dir)}")
    else:
        print(f"Results directory not found: {results_dir}")
        print("Run simulations first to generate results.")

def main():
    """主菜单循环"""
    while True:
        show_menu()
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            run_quick_test()
        elif choice == "2":
            run_full_simulation()
        elif choice == "3":
            run_batch_experiment()
        elif choice == "4":
            open_results()
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
