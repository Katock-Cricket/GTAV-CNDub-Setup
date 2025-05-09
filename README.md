# GTAV-CNDub-Setup
 GTAV中配模组安装器

感谢gtautil，在此基础上添加了一些自定义功能：https://github.com/gizzdev/gtautil

感谢UI：https://github.com/gtamodxcom/GTA-Vice-City-Nextgen-Edition-Launcher

构建命令：
```
cd Frontend
npm install
npm run build
cd..
pip install -r requirements.txt
pyinstaller build.spec --distpath 'E:\ai\GTA5_Chinese\gta5_chinese_dubbed'
```