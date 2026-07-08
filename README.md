# PUBG 距离测量工具

## 功能
- 在PUBG游戏地图上标记两个点，自动计算游戏内距离
- 基于地图网格校准（1格=100米）
- 快捷键截图：Shift+Alt+A

## 安装使用

### 方法一：直接运行Python脚本
```bash
pip install keyboard Pillow pystray
python pubg_distance.py
```

### 方法二：打包为EXE
1. 运行 `安装打包.bat`
2. 生成的EXE在 `dist` 文件夹中

## 使用说明

### 首次使用 - 初始化校准
1. 启动工具
2. 在PUBG中打开地图（按M键）
3. 按 Shift+Alt+A 截图
4. 点击「初始化校准」按钮
5. 在地图上点击两个相距100米的点（同一网格线上的两点）
6. 校准完成，以后只需测量模式

### 日常使用 - 测量距离
1. 按 Shift+Alt+A 截图
2. 点击「测量模式」
3. 在地图上点击两个点
4. 直接显示距离

## 技术说明
- 截图自动识别PUBG窗口（全屏模式）
- 校准值保存在 config.json，下次启动自动加载
- 基于像素距离与游戏距离的比例计算

## 文件说明
- `pubg_distance.py` - 主程序
- `config.json` - 校准配置（自动生成）
- `requirements.txt` - Python依赖
- `build.py` - 打包脚本
- `安装打包.bat` - 一键安装打包
