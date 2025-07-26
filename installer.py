import shutil
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Tuple, Union, List

import psutil

from config import *
from encrypt import get_pwd
from gta_utils import import2rpf
from zip_utils import extract_7z_with_password

installed_count = 0
total_count = len(rpfs_to_install_static)
log_cache = ''

game_dir = ''
mods_path = ''
unzipped_mod_path = ''


def get_install_progress():
    return (installed_count / total_count) * 100


def install_modloader():
    if game_dir == '' or mods_path == '' or unzipped_mod_path == '':
        raise AssertionError('游戏目录、mods目录或解压后的MOD目录未设置')

    if not os.path.exists(os.path.join(game_dir, 'OpenIV.asi')):
        shutil.copy(modloader_path, os.path.join(game_dir, 'OpenIV.asi'))
        append_output("提示: 未安装OpenIV.asi, 已自动为你安装")

    if not os.path.exists(os.path.join(game_dir, 'dinput8.dll')):
        shutil.copy(hook_path, os.path.join(game_dir, 'dinput8.dll'))
        append_output("提示: 未安装dinput8.dll, 已自动为你安装")


def unzip_rpf(zip_path: str) -> bool:
    if unzipped_mod_path == '':
        raise AssertionError('解压目录未设置')

    append_output(f'解压{zip_path}，请稍候...')
    ret, msg = extract_7z_with_password(zip_path, get_pwd(), unzipped_mod_path)
    append_output(msg)
    return ret


def import_dir_to_rpf(rpf_dir_in_mod: str, rpf_name: str, rpf_in_game: str, rpf_in_modloader: str):
    global installed_count

    if not os.path.exists(rpf_in_modloader):
        os.makedirs(os.path.dirname(rpf_in_modloader), exist_ok=True)
        shutil.copy(rpf_in_game, rpf_in_modloader)
        append_output(f'拷贝{rpf_name}完成')

    append_output(f'导入MOD到{rpf_name}中...')
    success, msg = import2rpf(rpf_dir_in_mod, rpf_in_modloader)
    shutil.rmtree(rpf_dir_in_mod)
    return success, msg


def install_an_rpf(rpf_path: str, mod_dir_paths: Union[List[str], str], idx: int) -> Tuple[bool, str]:
    if game_dir == '' or mods_path == '' or unzipped_mod_path == '':
        raise AssertionError('游戏目录、mods目录或解压后的MOD目录未设置')

    global installed_count

    rpf_attend_to_install = list(rpfs_to_install_static.keys())[idx]
    if rpf_attend_to_install not in list(get_rpfs_to_install().keys()):
        append_output(f'未选择安装{rpf_attend_to_install}，跳过')
        installed_count += 1
        return True, ''

    zip_path = os.path.join(paks_dir, f'{cn_dub_mod}_{idx}.pak')
    unzip_rpf(zip_path)

    rpf_name = os.path.basename(rpf_path).split('.')[0]
    rpf_in_game = os.path.join(game_dir, rpf_path)

    append_output(f'开始安装: {rpf_name}')
    if not os.path.exists(rpf_in_game):
        append_output(f'原{rpf_name} 不存在，跳过')
        installed_count += 1
        return True, ''

    rpf_in_modloader = os.path.join(mods_path, rpf_path)

    if isinstance(mod_dir_paths, str):
        mod_dir_paths = [mod_dir_paths]

    for mod_dir_path in mod_dir_paths:
        rpf_dir_in_mod = os.path.join(unzipped_mod_path, cn_dub_mod, mod_dir_path)
        if not os.path.exists(rpf_dir_in_mod) or not os.listdir(rpf_dir_in_mod):
            append_output(f'MOD {rpf_name} 不存在或为空，可能尚未制作，敬请等待后续更新')
            continue

        success, msg = import_dir_to_rpf(rpf_dir_in_mod, rpf_name, rpf_in_game, rpf_in_modloader)
        if not success:
            return False, msg

    installed_count += 1
    return True, ''


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
                # print("GTAUtil进程不存在或权限不足")
                pass
    # append_output("已停止所有后台GTAUtil进程")


def check_game_version() -> Tuple[bool, str]:
    if (not os.path.exists(game_dir) or
            not os.path.exists(os.path.join(game_dir, 'x64')) or
            not os.path.exists(os.path.join(game_dir, 'update'))):
        return False, '游戏目录无效，请检查路径是否正确'

    if not os.path.exists(os.path.join(game_dir, 'GTA5.exe')):
        return False, '游戏目录无效，请检查是否为GTA5传承版（安装器不支持增强版），请参见说明书为增强版安装MOD'

    if os.path.exists(os.path.join(game_dir, 'GTA5_Enhanced.exe')):
        return False, '游戏目录无效，请检查是否为GTA5传承版（安装器不支持增强版），请参见说明书为增强版安装MOD'

    return True, '游戏目录正确'


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
        if not os.path.exists(unzipped_mod_path):
            os.makedirs(unzipped_mod_path)

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
                for idx, (rpf_path, mod_dir_path) in enumerate(rpfs_to_install_static.items()):  # paks的idx是static的idx
                    future = executor.submit(install_an_rpf, rpf_path, mod_dir_path, idx)
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
            for idx, (rpf_path, mod_dir_path) in enumerate(rpfs_to_install_static.items()):  # paks的idx是static的idx
                # try:
                success, msg = install_an_rpf(rpf_path, mod_dir_path, idx)
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
        shutil.rmtree(unzipped_mod_path)
        set_installing(False)


def install_main(new_game_dir):
    global game_dir, mods_path, unzipped_mod_path
    if is_installing():
        append_output("正在执行操作，请勿操作")
        return

    set_installing(True)
    game_dir = new_game_dir
    mods_path = os.path.join(game_dir, 'mods')
    unzipped_mod_path = os.path.join(game_dir, 'x64', cn_dub_mod)

    threading.Thread(target=install_pipeline, daemon=True).start()


def uninstall_main(new_game_dir):
    global game_dir, mods_path, unzipped_mod_path
    if is_installing():
        append_output("正在执行操作，请稍后再试")
        return

    set_installing(True)
    game_dir = new_game_dir
    mods_path = os.path.join(game_dir, 'mods')
    unzipped_mod_path = os.path.join(game_dir, 'x64', cn_dub_mod)

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
