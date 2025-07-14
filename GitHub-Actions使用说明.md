# GitHub Actions 自动打包说明

## 概述

我已经为你创建了两个GitHub Actions工作流，可以在GitHub上自动打包Windows、macOS和Linux版本。

## 工作流文件

### 1. `.github/workflows/build.yml` - 全平台构建
- **触发条件**: 推送到main/master分支、创建标签、手动触发
- **构建平台**: Windows、macOS、Linux
- **输出**: 三个平台的可执行文件和分发包

### 2. `.github/workflows/build-windows.yml` - Windows专用构建
- **触发条件**: 手动触发
- **构建平台**: 仅Windows
- **输出**: Windows可执行文件和ZIP包
- **特性**: 可选择是否创建Release

## 使用方法

### 方法一：推送代码自动构建（全平台）
1. 将代码推送到GitHub仓库的main或master分支
2. GitHub Actions会自动开始构建
3. 构建完成后在Actions页面下载artifacts

### 方法二：手动触发构建
1. 进入GitHub仓库页面
2. 点击 "Actions" 标签
3. 选择对应的工作流：
   - "Build AugmentCode-Free" - 全平台构建
   - "Build Windows Only" - 仅Windows构建
4. 点击 "Run workflow" 按钮
5. 等待构建完成

### 方法三：创建标签自动发布
1. 创建以 `v` 开头的标签：
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
2. GitHub Actions会自动构建并创建Release
3. Release中包含所有平台的打包文件

## 构建输出

### Artifacts（构建产物）
每次构建会生成以下artifacts：
- `AugmentCode-Free-windows` - Windows版本目录
- `AugmentCode-Free-macos` - macOS版本目录  
- `AugmentCode-Free-linux` - Linux版本目录
- `AugmentCode-Free-windows-zip` - Windows ZIP包（仅Windows专用构建）

### Release文件（标签构建）
- `AugmentCode-Free-windows.zip` - Windows版本
- `AugmentCode-Free-macos.zip` - macOS版本
- `AugmentCode-Free-linux.tar.gz` - Linux版本

## 快速获取Windows版本

### 立即构建Windows版本：
1. 访问: https://github.com/你的用户名/AugmentCode-Free/actions
2. 选择 "Build Windows Only" 工作流
3. 点击 "Run workflow"
4. 勾选 "Create a release" 如果想直接创建发布
5. 点击绿色的 "Run workflow" 按钮

### 下载构建结果：
- **Artifacts**: 在构建完成页面点击下载
- **Release**: 在仓库的Releases页面下载

## 技术细节

### Python版本
- 使用Python 3.11避免3.13的外部管理环境问题
- 自动安装所有必需依赖

### 构建特性
- 单文件可执行程序
- 包含所有依赖库
- 自动生成使用说明
- 支持所有主流操作系统

### 文件结构
每个平台的分发包包含：
- 可执行文件（.exe/.app/无扩展名）
- README.md（项目说明）
- 使用说明.txt（详细使用指南）

## 故障排除

### 构建失败
1. 检查Actions页面的错误日志
2. 确认所有源文件都已提交
3. 检查Python语法错误

### 权限问题
- GitHub Actions需要GITHUB_TOKEN权限（自动提供）
- 创建Release需要仓库写入权限

### 下载问题
- Artifacts有90天有效期
- Release文件永久保存
- 建议重要版本创建Release

现在你可以直接在GitHub上构建Windows版本了！
