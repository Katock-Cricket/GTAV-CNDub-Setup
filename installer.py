import os
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from tkinter import messagebox

import psutil

from base_utils import import2rpf

game_dir = ''
mods_path = os.path.join(game_dir, 'mods')

cn_dub_mod = 'gta5_chinese_dubbed'
modloader_path = os.path.join('pre_install', 'OpenIV.asi')
hook_path = os.path.join('pre_install', 'dinput8.dll')

# key: rpf_path, value: mod_dir_path
rpfs_to_install = {
    'x64d.rpf': 'x64d.rpf/movies',
    'update/update.rpf': 'update/update.rpf/x64/data/lang/chinesesimp_rel.rpf',
    'update/update2.rpf': 'update/update.rpf/x64/data/lang/chinesesimp_rel.rpf',
    'x64/audio/sfx/CUTSCENE_MASTERED_ONLY.rpf': 'x64/audio/sfx/CUTSCENE_MASTERED_ONLY.rpf',
    'x64/audio/sfx/PAIN.rpf': 'x64/audio/sfx/PAIN.rpf',
    'x64/audio/sfx/PROLOGUE.rpf': 'x64/audio/sfx/PROLOGUE.rpf',
    'x64/audio/sfx/S_MISC.rpf': 'x64/audio/sfx/S_MISC.rpf',
    'x64/audio/sfx/SS_AC.rpf': 'x64/audio/sfx/SS_AC.rpf',
    'x64/audio/sfx/SS_DE.rpf': 'x64/audio/sfx/SS_DE.rpf',
    'x64/audio/sfx/SS_FF.rpf': 'x64/audio/sfx/SS_FF.rpf',
    'x64/audio/sfx/SS_GM.rpf': 'x64/audio/sfx/SS_GM.rpf',
    'x64/audio/sfx/SS_NP.rpf': 'x64/audio/sfx/SS_NP.rpf',
    'x64/audio/sfx/SS_QR.rpf': 'x64/audio/sfx/SS_QR.rpf',
    'x64/audio/sfx/SS_ST.rpf': 'x64/audio/sfx/SS_ST.rpf',
    'x64/audio/sfx/SS_UZ.rpf': 'x64/audio/sfx/SS_UZ.rpf'
}

installed_count = 0
total_count = len(rpfs_to_install)
log_cache = ''

def get_install_progress():
    return (installed_count / total_count) * 100


def install_modloader():
    if not os.path.exists(os.path.join(game_dir, 'OpenIV.asi')) or not os.path.exists(
            os.path.join(game_dir, 'dinput8.dll')):
        shutil.copy(modloader_path, os.path.join(game_dir, 'OpenIV.asi'))
        shutil.copy(hook_path, os.path.join(game_dir, 'dinput8.dll'))
        append_output("提示: 未安装ASI Loader或OpenIV.asi，已自动为你安装")


def install_an_rpf(rpf_path: str, mod_dir_path: str):
    global installed_count

    rpf_in_game = os.path.join(game_dir, rpf_path)
    rpf_in_modloader = os.path.join(mods_path, rpf_path)
    rpf_dir_in_mod = os.path.join(cn_dub_mod, mod_dir_path)

    append_output(f'开始安装RPF: {rpf_path}')
    if not os.path.exists(rpf_in_game):
        append_output(f'原RPF {rpf_path} 不存在，跳过')
        installed_count += 1
        return
    if not os.path.exists(rpf_dir_in_mod) or not os.listdir(rpf_dir_in_mod):
        append_output(f'MOD目录 {rpf_dir_in_mod} 不存在或为空，可能尚未制作，跳过')
        installed_count += 1
        return

    if not os.path.exists(rpf_in_modloader):
        os.makedirs(os.path.dirname(rpf_in_modloader), exist_ok=True)
        shutil.copy(rpf_in_game, rpf_in_modloader)
        append_output(f'拷贝{rpf_path}到{mods_path}完成')

    import2rpf(rpf_dir_in_mod, rpf_in_modloader)
    append_output(f'导入MOD到{rpf_path}完成')
    installed_count += 1


def append_output(text):
    print(text)
    global log_cache
    log_cache = text + '\n'


def get_output():
    return log_cache


def kill_gtautil_processes():
    # 遍历所有正在运行的进程
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'GTAUtil.exe':
            # 如果进程的名字是 GTAUtil
            try:
                proc.kill()  # 尝试终止该进程
                append_output(f"进程 {proc.info['name']} (PID: {proc.info['pid']}) 已终止")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # 处理权限不足或者进程已消失的情况
                print("GTAUtil进程不存在或权限不足")
    append_output("已停止所有后台GTAUtil进程")


def install_pipeline():
    try:
        append_output("开始安装...程序结束前请勿关闭此窗口和安装器")
        global installed_count
        installed_count = 0

        if (not os.path.exists(game_dir) or
                not os.path.exists(os.path.join(game_dir, 'x64')) or
                not os.path.exists(os.path.join(game_dir, 'update'))):
            raise AssertionError('游戏目录无效，请检查路径是否正确')

        kill_gtautil_processes()

        os.system('chcp 65001 > nul')
        if not os.path.exists(mods_path):
            os.makedirs(mods_path)
            append_output("提示: mods目录不存在，已自动创建")

        install_modloader()

        # 获取逻辑处理器数量
        cpu_count = os.cpu_count()
        if cpu_count is None:
            cpu_count = 1
        append_output(f'CPU逻辑处理器数量: {cpu_count}')
        if cpu_count >= 5:
            # 使用线程池并行安装RPF，最多8个同时安装
            append_output('并行安装RPF文件...')
            with ThreadPoolExecutor(max_workers=max(8, cpu_count - 3)) as executor:
                futures = []
                for rpf_path, mod_dir_path in rpfs_to_install.items():
                    future = executor.submit(install_an_rpf, rpf_path, mod_dir_path)
                    futures.append(future)

                # 等待所有任务完成
                for future in as_completed(futures):
                    try:
                        future.result()  # 获取结果，如果有异常会在这里抛出
                    except Exception as e:
                        append_output(f"安装过程中出现错误: {str(e)}")
        else:
            # 串行安装
            append_output('串行安装RPF文件...')
            for rpf_path, mod_dir_path in rpfs_to_install.items():
                install_an_rpf(rpf_path, mod_dir_path)

        append_output('安装完成！')

    except Exception as e:
        append_output(f"错误: {str(e)}")
        # messagebox.showerror("安装错误", f"安装过程中出现错误: {str(e)}")


def install_main(new_game_dir):
    global game_dir, mods_path
    game_dir = new_game_dir
    mods_path = os.path.join(game_dir, 'mods')

    threading.Thread(target=install_pipeline, daemon=True).start()
