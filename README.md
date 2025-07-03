# Python编译工具

## 项目简介
本项目是一个基于 Python + tkinter 的图形界面工具，用于一键调用 pyinstaller 打包 Python 脚本，支持自定义软件名称、开发者、版本号、联系邮箱、图标、是否显示控制台等参数。

## 主要功能
- 选择 Python 脚本文件进行打包
- 支持设置是否显示控制台窗口
- 支持自定义软件图标（.ico 文件）
- 支持填写软件名称、开发者、版本号、联系邮箱等元信息
- 一键调用 pyinstaller 打包，日志实时输出

## 使用方法
### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行本工具
```bash
python main.py
```

### 3. 打包你的 Python 脚本
- 选择你的 .py 文件
- 可选设置图标、元信息等
- 点击"开始打包"按钮
- 查看日志栏输出，打包完成后在 dist 目录下获取生成的 exe 文件

### 4. 打包依赖
- 需提前安装 pyinstaller
- 本工具会自动生成 version.txt 资源信息文件

## 界面截图
（自行截图）

## 联系方式
如有问题或建议，请联系开发者邮箱：top777@sina.com

## 许可证
MIT License 
