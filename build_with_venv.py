#!/usr/bin/env python3
"""
AugmentCode-Free 虚拟环境打包脚本
专门处理Python 3.13+的外部管理环境限制
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

# 修复Windows控制台编码问题
if platform.system() == "Windows":
    import locale
    try:
        # 尝试设置UTF-8编码
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        # 如果失败，使用系统默认编码
        pass

def safe_print(text):
    """安全打印函数，处理编码问题"""
    try:
        print(text)
    except UnicodeEncodeError:
        # 如果遇到编码错误，移除特殊字符
        safe_text = text.encode('ascii', 'ignore').decode('ascii')
        print(safe_text)

def create_virtual_environment():
    """创建虚拟环境"""
    venv_path = Path("build_venv")
    
    if venv_path.exists():
        safe_print("🔄 删除现有虚拟环境...")
        shutil.rmtree(venv_path)

    safe_print("📦 创建虚拟环境...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_path)])
        safe_print("✅ 虚拟环境创建成功")
        return venv_path
    except subprocess.CalledProcessError:
        safe_print("❌ 虚拟环境创建失败")
        return None

def get_venv_python(venv_path):
    """获取虚拟环境中的Python路径"""
    if platform.system() == "Windows":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"

def install_dependencies_in_venv(venv_python):
    """在虚拟环境中安装依赖"""
    print("📥 在虚拟环境中安装依赖...")
    try:
        subprocess.check_call([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([str(venv_python), "-m", "pip", "install", "-r", "build_requirements.txt"])
        print("✅ 依赖安装成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ 依赖安装失败")
        return False

def build_with_venv(venv_python):
    """使用虚拟环境中的Python进行打包"""
    print("🔨 开始打包...")
    
    # 首先生成spec文件
    try:
        subprocess.check_call([str(venv_python), "build.py"])
        print("✅ 打包完成")
        return True
    except subprocess.CalledProcessError:
        print("❌ 打包失败")
        return False

def cleanup_venv(venv_path):
    """清理虚拟环境"""
    if venv_path.exists():
        print("🧹 清理虚拟环境...")
        shutil.rmtree(venv_path)
        print("✅ 清理完成")

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 AugmentCode-Free 虚拟环境打包工具")
    print("=" * 60)
    print()
    
    current_os = platform.system()
    print(f"当前操作系统: {current_os}")
    print(f"Python版本: {sys.version}")
    print()
    
    # 创建虚拟环境
    venv_path = create_virtual_environment()
    if not venv_path:
        sys.exit(1)
    
    try:
        # 获取虚拟环境Python路径
        venv_python = get_venv_python(venv_path)
        
        if not venv_python.exists():
            print(f"❌ 虚拟环境Python不存在: {venv_python}")
            sys.exit(1)
        
        # 在虚拟环境中安装依赖
        if not install_dependencies_in_venv(venv_python):
            sys.exit(1)
        
        # 使用虚拟环境进行打包
        if not build_with_venv(venv_python):
            sys.exit(1)
        
        print()
        print("=" * 60)
        print("🎉 打包完成！")
        print("=" * 60)
        print()
        print("生成的文件:")
        print(f"- 可执行文件: dist/AugmentCode-Free{'(.exe)' if current_os == 'Windows' else '(.app)' if current_os == 'Darwin' else ''}")
        print(f"- 分发包: AugmentCode-Free-{current_os.lower()}/")
        
    finally:
        # 清理虚拟环境
        cleanup_venv(venv_path)

if __name__ == "__main__":
    main()
