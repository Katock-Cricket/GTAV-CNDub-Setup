import os
import subprocess
import sys
from time import sleep

# if getattr(sys, 'frozen', False):
#     util_path = os.path.join(sys._MEIPASS, 'gtautil', 'GTAUtil.exe')
# else:
#     util_path = os.path.join('gtautil', 'GTAUtil.exe')
util_path = os.path.join('gtautil', 'GTAUtil.exe')


# def init_cache(game_dir: str):
#     command = [util_path, 'buildcache']
#     process = subprocess.Popen(
#         command,
#         stdin=subprocess.PIPE,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         shell=True,
#         creationflags=subprocess.CREATE_NO_WINDOW
#     )
#     process.stdin.write(f"{game_dir}\n".encode())
#     process.stdin.flush()
#
#     stdout, stderr = process.communicate()
#     process.wait()
#
#     if stdout or stderr:
#         print(stdout.decode(), stderr.decode())
#         return stdout.decode(), stderr.decode()


def extract_rpf(game_dir: str, tmp_path: str, rpf_path: str) -> str:
    """
    将游戏原rpf文件提取到tmp文件夹中对应命名的文件夹内。

    param:
    rpf_path (str): 游戏原rpf文件的完整路径。

    :return: 提取成功返回空字符串，失败返回错误信息
    """
    rpf_name = os.path.basename(rpf_path)
    extract_path = os.path.join(tmp_path, rpf_name)
    command = [util_path, 'extractarchive', '--input', rpf_path, '--output', extract_path]
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    sleep(2)
    input_data = f"{game_dir}\n".encode('utf-8')
    stdout, stderr = process.communicate(input=input_data)

    process.wait()

    if stdout or stderr:
        return stdout.decode(errors='ignore') + stderr.decode(errors='ignore')

    return ''


def build_rpf(game_dir: str, source_path, target_path) -> str:
    """
    将tmp文件夹中对应命名的文件夹内的文件打包成游戏原rpf文件。

    :param
    source_path: 待打包的.rpf文件夹完整路径
    target_path: 目标rpf文件完整路径, 不包含文件名

    :return: 打包成功返回空字符串，失败返回错误信息
    """
    rpf_name = os.path.basename(source_path).split('.')[0]
    command = [util_path, 'createarchive', '--input', source_path, '--output', target_path, '--name', rpf_name]
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    sleep(2)
    input_data = f"{game_dir}\n".encode('utf-8')
    stdout, stderr = process.communicate(input=input_data)

    process.wait()

    if stdout or stderr:
        return stdout.decode(errors='ignore') + stderr.decode(errors='ignore')
    return ''
