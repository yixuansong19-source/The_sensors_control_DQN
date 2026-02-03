#!/bin/bash
# 激活虚拟环境并运行快速仿真脚本

echo ""
echo "================================================"
echo "RADAR TARGET TRACKING - QUICK START"
echo "================================================"
echo ""

# 检查虚拟环境
if [ ! -f "../parl-env/bin/activate" ]; then
    echo "ERROR: Virtual environment not found at ../parl-env"
    exit 1
fi

# 激活虚拟环境
source ../parl-env/bin/activate

# 显示菜单
echo "Choose simulation mode:"
echo "1. Quick test (single episode)"
echo "2. Full simulation (multiple episodes)"
echo "3. Open menu launcher"
echo ""

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "Running quick simulation..."
        python quick_simulate.py
        ;;
    2)
        echo "Running full simulation..."
        python simulate_and_visualize.py --episodes 3 --save-dir ./results --show
        ;;
    3)
        echo "Opening menu launcher..."
        python launcher.py
        ;;
    *)
        echo "Invalid choice"
        ;;
esac
