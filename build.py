#!/usr/bin/env python3
"""
AugmentCode-Free 打包脚本
支持Windows和macOS平台的可执行文件打包
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print("✅ PyInstaller 已安装")
        return True
    except ImportError:
        print("❌ PyInstaller 未安装")
        print("正在安装 PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller>=5.0.0"])
            print("✅ PyInstaller 安装成功")
            return True
        except subprocess.CalledProcessError:
            print("❌ PyInstaller 安装失败")
            return False

def install_dependencies():
    """安装项目依赖"""
    print("正在安装项目依赖...")
    try:
        # 首先尝试正常安装
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "build_requirements.txt"])
        print("✅ 依赖安装成功")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  正常安装失败，尝试使用 --user 参数...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "-r", "build_requirements.txt"])
            print("✅ 依赖安装成功（用户模式）")
            return True
        except subprocess.CalledProcessError:
            print("⚠️  用户模式安装失败，尝试使用 --break-system-packages 参数...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "-r", "build_requirements.txt"])
                print("✅ 依赖安装成功（系统包模式）")
                return True
            except subprocess.CalledProcessError:
                print("❌ 所有安装方式都失败了")
                print("💡 建议手动创建虚拟环境：")
                print("   python3 -m venv venv")
                print("   source venv/bin/activate")
                print("   pip install -r build_requirements.txt")
                print("   python build.py")
                return False

def create_spec_file():
    """创建PyInstaller spec文件"""
    current_os = platform.system()
    
    # 根据操作系统设置不同的配置
    if current_os == "Windows":
        icon_file = "icon.ico"  # Windows使用.ico格式
        console = False  # GUI应用不显示控制台
        extension = ".exe"
    elif current_os == "Darwin":  # macOS
        icon_file = "icon.icns"  # macOS使用.icns格式
        console = False
        extension = ".app"
    else:  # Linux
        icon_file = None
        console = False
        extension = ""
    
    # 构建icon参数
    icon_param = ""
    if icon_file and Path(icon_file).exists():
        icon_param = f"icon='{icon_file}',"

    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('augment_tools_core', 'augment_tools_core'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'sqlite3',
        'json',
        'uuid',
        'threading',
        'queue',
        'platform',
        'subprocess',
        'pathlib',
        'shutil',
        'colorama',
        'click',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AugmentCode-Free',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console={console},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    {icon_param}
)
'''
    
    # 如果是macOS，添加app bundle配置
    if current_os == "Darwin":
        bundle_icon_param = ""
        if icon_file and Path(icon_file).exists():
            bundle_icon_param = f"icon='{icon_file}',"

        spec_content += f'''
app = BUNDLE(
    exe,
    name='AugmentCode-Free.app',
    {bundle_icon_param}
    bundle_identifier='com.augmentcode.free',
    info_plist={{
        'NSHighResolutionCapable': 'True',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'CFBundleDisplayName': 'AugmentCode-Free',
        'NSHumanReadableCopyright': 'Copyright © 2025',
    }},
)
'''
    
    with open("AugmentCode-Free.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("✅ Spec文件创建成功")

def build_executable():
    """构建可执行文件"""
    print("开始构建可执行文件...")
    
    try:
        # 使用spec文件构建
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "AugmentCode-Free.spec"]
        subprocess.check_call(cmd)
        print("✅ 构建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False

def create_dist_package():
    """创建分发包"""
    current_os = platform.system()
    dist_dir = Path("dist")
    
    if not dist_dir.exists():
        print("❌ dist目录不存在")
        return False
    
    # 创建最终的分发目录
    package_name = f"AugmentCode-Free-{current_os.lower()}"
    package_dir = Path(package_name)
    
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir()
    
    # 复制可执行文件
    if current_os == "Windows":
        exe_file = dist_dir / "AugmentCode-Free.exe"
        if exe_file.exists():
            shutil.copy2(exe_file, package_dir)
    elif current_os == "Darwin":
        app_bundle = dist_dir / "AugmentCode-Free.app"
        if app_bundle.exists():
            shutil.copytree(app_bundle, package_dir / "AugmentCode-Free.app")
    else:  # Linux
        exe_file = dist_dir / "AugmentCode-Free"
        if exe_file.exists():
            shutil.copy2(exe_file, package_dir)
    
    # 复制README文件
    if Path("README.md").exists():
        shutil.copy2("README.md", package_dir)
    
    # 创建使用说明
    usage_content = f"""# AugmentCode-Free 使用说明

## 运行方式

### {current_os}:
"""
    
    if current_os == "Windows":
        usage_content += """
- 双击 `AugmentCode-Free.exe` 启动程序
- 或在命令行中运行: `AugmentCode-Free.exe`
"""
    elif current_os == "Darwin":
        usage_content += """
- 双击 `AugmentCode-Free.app` 启动程序
- 或在终端中运行: `open AugmentCode-Free.app`
"""
    else:
        usage_content += """
- 在终端中运行: `./AugmentCode-Free`
- 确保文件有执行权限: `chmod +x AugmentCode-Free`
"""
    
    usage_content += """
## 功能说明

1. **清理数据库**: 清理VS Code数据库中的augment相关条目
2. **修改遥测ID**: 生成新的machineId和devDeviceId
3. **运行所有工具**: 执行完整的清理流程

## 注意事项

- 程序会自动备份原始文件
- 请确保VS Code已关闭再运行此工具
- 如遇问题，可查看备份文件进行恢复

## 支持的操作系统

- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu, CentOS等)
"""
    
    with open(package_dir / "使用说明.txt", "w", encoding="utf-8") as f:
        f.write(usage_content)
    
    print(f"✅ 分发包创建成功: {package_dir}")
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 AugmentCode-Free 打包工具")
    print("=" * 60)
    print()
    
    current_os = platform.system()
    print(f"当前操作系统: {current_os}")
    print(f"Python版本: {sys.version}")
    print()
    
    # 检查并安装依赖
    if not install_dependencies():
        sys.exit(1)
    
    if not check_pyinstaller():
        sys.exit(1)
    
    # 创建spec文件
    create_spec_file()
    
    # 构建可执行文件
    if not build_executable():
        sys.exit(1)
    
    # 创建分发包
    if not create_dist_package():
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("🎉 打包完成！")
    print("=" * 60)
    print()
    print("生成的文件:")
    print(f"- 可执行文件: dist/AugmentCode-Free{'(.exe)' if current_os == 'Windows' else '(.app)' if current_os == 'Darwin' else ''}")
    print(f"- 分发包: AugmentCode-Free-{current_os.lower()}/")
    print()
    print("你可以将分发包目录打包为zip文件进行分发。")

if __name__ == "__main__":
    main()
