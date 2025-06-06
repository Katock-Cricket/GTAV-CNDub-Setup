# GTAV-CNDub-Setup
 GTAV中配模组安装器

RPF导入功能基于gtautil，在此基础上添加了一些自定义功能：https://github.com/gizzdev/gtautil

感谢UI：https://github.com/gtamodxcom/GTA-Vice-City-Nextgen-Edition-Launcher

构建命令：
```shell
# 构建前端页面
cd Frontend
npm install
npm run build
cd..
# 安装py依赖
pip install -r requirements.txt
# 构建应用程序，请在源码args中设置构建选项
python build.py
```

