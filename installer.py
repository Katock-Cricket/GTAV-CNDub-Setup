import datetime
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Tuple, List

import psutil

from config import *
from gta_utils import import2rpf

installed_count = 0
total_count = len(rpfs_to_install_static)
log_cache = ''

game_dir = ''
mods_path = ''
is_enhanced = False


def get_install_progress():
    return (installed_count / total_count) * 100


def install_modloader():
    if game_dir == '' or mods_path == '':
        raise AssertionError('游戏目录、mods目录或解压后的MOD目录未设置')

    if is_enhanced:
        if not os.path.exists(os.path.join(game_dir, 'OpenRPF.asi')):
            shutil.copy(modloader_path, os.path.join(game_dir, 'OpenRPF.asi'))
            append_output("提示: OpenRPF.asi, 已自动为你安装")
        if not os.path.exists(os.path.join(game_dir, 'dsound.dll')):
            shutil.copy(hook_path, os.path.join(game_dir, 'dsound.dll'))
            append_output("提示: 未安装asi_loader, 已自动为你安装dsound.dll")
    else:
        if not os.path.exists(os.path.join(game_dir, 'OpenIV.asi')):
            shutil.copy(modloader_path, os.path.join(game_dir, 'OpenIV.asi'))
            append_output("提示: 未安装OpenIV.asi, 已自动为你安装")
        if not any(os.path.exists(os.path.join(game_dir, dll)) for dll in asi_loaders):
            shutil.copy(hook_path, os.path.join(game_dir, 'dinput8.dll'))
            append_output("提示: 未安装asi_loader, 已自动为你安装dinput8.dll")


def import_dir_to_rpf(rpf_dir_in_mod: str, rpf_name: str, rpf_in_game: str, rpf_in_modloader: str):
    global installed_count

    if not os.path.exists(rpf_in_modloader):
        os.makedirs(os.path.dirname(rpf_in_modloader), exist_ok=True)
        shutil.copy(rpf_in_game, rpf_in_modloader)
        append_output(f'拷贝{rpf_name}完成')

    append_output(f'导入MOD到{rpf_name}中...')
    success, msg = import2rpf(rpf_dir_in_mod, rpf_in_modloader, is_enhanced, game_dir)
    return success, msg


def install_an_rpf(rpf_path: str, mod_dir_paths: List[str]) -> Tuple[bool, str]:
    if game_dir == '' or mods_path == '':
        raise AssertionError('游戏目录、mods目录或解压后的MOD目录未设置')

    global installed_count
    rpf_name = os.path.basename(rpf_path).split('.')[0]
    rpf_in_game = os.path.join(game_dir, rpf_path)

    append_output(f'开始安装: {rpf_name}')
    if not os.path.exists(rpf_in_game):
        append_output(f'原{rpf_name} 不存在，跳过')
        installed_count += 1
        return True, ''

    rpf_in_modloader = os.path.join(mods_path, rpf_path)

    for mod_dir_path in mod_dir_paths:
        module = mod_dir_to_module[mod_dir_path]
        if module not in get_modules():
            append_output(f'未选择{mod_dir_path}，跳过')
            continue

        rpf_dir_in_mod = os.path.join(cn_dub_mod, mod_dir_path)
        if not os.path.exists(rpf_dir_in_mod) or not os.listdir(rpf_dir_in_mod):
            append_output(f'MOD {rpf_name} 不存在或为空，可能尚未制作，敬请等待后续更新')
            continue

        success, msg = import_dir_to_rpf(rpf_dir_in_mod, rpf_name, rpf_in_game, rpf_in_modloader)
        if not success:
            return False, msg

    append_output(f'{rpf_name} 安装完成')
    installed_count += 1
    return True, ''


def append_output(text):
    print(text)
    with open('installer.log', 'a', encoding='utf-8') as f:
        f.write(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {text}\n')
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
                # print("GTAUtil进程不存在或权限不足")
                pass
    # append_output("已停止所有后台GTAUtil进程")


def check_game_version() -> Tuple[bool, str]:
    global is_enhanced
    if (not os.path.exists(game_dir) or
            not os.path.exists(os.path.join(game_dir, 'x64')) or
            not os.path.exists(os.path.join(game_dir, 'update'))):
        return False, '游戏目录无效，请检查路径是否正确'

    if os.path.exists(os.path.join(game_dir, 'GTA5_Enhanced.exe')):
        is_enhanced = True
        return True, '游戏目录已识别为增强版'

    is_enhanced = False
    return True, '游戏目录已识别为传承版'


def install_pipeline():
    try:
        append_output("开始安装...完成前请勿关闭安装器")
        global installed_count
        installed_count = 0

        check, msg = check_game_version()
        append_output(msg)
        if not check:
            return

        os.system('chcp 65001 > nul')
        kill_gtautil_processes()

        if not os.path.exists(mods_path):
            os.makedirs(mods_path)
            append_output("提示: mods目录不存在，已自动创建")

        install_modloader()

        # 获取逻辑处理器数量
        cpu_count = os.cpu_count()
        if cpu_count is None:
            cpu_count = 1
        append_output(f'CPU逻辑处理器数量: {cpu_count}')
        if cpu_count >= 4:
            # 使用线程池并行安装RPF，最多8个同时安装
            append_output('并行安装RPF文件...')
            with ThreadPoolExecutor(max_workers=max(8, cpu_count - 2)) as executor:
                futures = []
                for _, (rpf_path, mod_dir_path) in enumerate(rpfs_to_install_static.items()):  # paks的idx是static的idx
                    future = executor.submit(install_an_rpf, rpf_path, mod_dir_path)
                    futures.append(future)

                for future in as_completed(futures):
                    # try:
                    success, msg = future.result()
                    if not success:
                        raise Exception(msg)
                    # except Exception as e:
                    #     append_output(f"安装过程中出现错误: {str(e)}")
        else:
            # 串行安装
            append_output('串行安装RPF文件...')
            for _, (rpf_path, mod_dir_path) in enumerate(rpfs_to_install_static.items()):  # paks的idx是static的idx
                # try:
                success, msg = install_an_rpf(rpf_path, mod_dir_path)
                if not success:
                    raise Exception(msg)
                # except Exception as e:
                #     append_output(f"安装过程中出现错误: {str(e)}")

        if installed_count == total_count:
            append_output('安装完成！')
        else:
            append_output(f'安装结束，发生错误')

    except Exception as e:
        append_output(f"错误: {str(e)}")
    finally:
        set_installing(False)


def install_main(new_game_dir):
    global game_dir, mods_path
    if is_installing():
        append_output("正在执行操作，请勿操作")
        return

    set_installing(True)
    game_dir = new_game_dir
    mods_path = os.path.join(game_dir, 'mods')

    threading.Thread(target=install_pipeline, daemon=True).start()


def uninstall_main(new_game_dir):
    global game_dir, mods_path
    if is_installing():
        append_output("正在执行操作，请稍后再试")
        return

    set_installing(True)
    game_dir = new_game_dir
    mods_path = os.path.join(game_dir, 'mods')

    check, msg = check_game_version()
    append_output(msg)
    if not check:
        return

    append_output("开始卸载...完成前请勿关闭安装器")
    for rpf_path, _ in rpfs_to_install_static.items():
        rpf_in_mods = os.path.join(mods_path, rpf_path)
        if os.path.exists(rpf_in_mods):
            os.remove(rpf_in_mods)
            append_output(f'删除{rpf_path}完成')
    append_output('卸载完成！')
