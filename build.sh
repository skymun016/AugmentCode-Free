#!/bin/bash

echo "===================================="
echo "   AugmentCode-Free macOS/Linux 打包工具"
echo "===================================="
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    echo "请先安装Python 3.7或更高版本"
    exit 1
fi

echo "✅ Python3 已安装"
echo

# 检查pip是否安装
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 未安装"
    echo "请先安装pip3"
    exit 1
fi

echo "✅ pip3 已安装"
echo

# 检查Python版本并选择合适的打包方式
PYTHON_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
PYTHON_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
echo "Python版本: $PYTHON_MAJOR.$PYTHON_MINOR"

if [ "$PYTHON_MAJOR" -gt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 12 ]); then
    echo "检测到Python 3.12+，使用虚拟环境方式打包..."
    python3 build_with_venv.py
else
    echo "使用标准方式打包..."
    python3 build.py
fi

echo
echo "打包完成！"
