import os
import subprocess

from typing_extensions import Tuple

util_path = os.path.join('gtautil', 'GTAUtil.exe')


def get_inner_path(input_path: str, rpf_path: str) -> str:
    rpf_name = os.path.basename(rpf_path)
    if rpf_name == 'update2.rpf':
        rpf_name = 'update.rpf'  # 兼容update2.rpf，依旧从update.rpf中获取内部路径

    # 标准化路径，确保路径分隔符一致
    normalized_input = os.path.normpath(input_path)
    parts = normalized_input.split(os.sep)

    try:
        # 找到rpf_name在输入路径中的位置
        rpf_index = parts.index(rpf_name)
    except ValueError:
        return f"错误：输入路径中不包含目标RPF文件名 '{rpf_name}'"

    # 获取rpf_name之后的部分
    remaining_parts = parts[rpf_index + 1:]

    if not remaining_parts:
        # 如果input_path就是rpf文件本身，没有内部路径
        inner_path = ""
    else:
        if os.path.isfile(input_path):
            # 如果是文件，去掉最后一个文件名部分
            inner_path = os.path.join(*remaining_parts[:-1])
            if inner_path:  # 如果不是根目录，添加路径分隔符
                inner_path += os.sep
        else:
            # 如果是文件夹，保留全部剩余部分
            inner_path = os.path.join(*remaining_parts)
            if inner_path:  # 如果不是根目录，添加路径分隔符
                inner_path += os.sep

    return inner_path


def import2rpf(input_path: str, rpf_path: str) -> Tuple[bool ,str]:
    """
    将文件夹内的文件导入游戏原rpf文件。

    :param
    rpf_path: 目标rpf文件完整路径
    input_path: 待导入的文件或文件夹完整路径

    :return: 导入成功返回空字符串，失败返回错误信息
    """
    inner_path = get_inner_path(input_path, rpf_path)
    command = [util_path, 'import2rpf', '--input', input_path, '--output', rpf_path, '--path', inner_path]
    # print(command)
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    stdout, stderr = process.communicate()

    process.wait()

    # print(stdout.decode(errors='ignore'), stderr.decode(errors='ignore'))

    if stderr:
        return False, stderr.decode(errors='ignore')
    return True, ''


def encrypt_rpf(rpf_path: str) -> Tuple[bool, str]:
    """
    加密RPF文件

    :param rpf_path: 已经拷贝到mods文件夹的RPF文件路径
    :return: 加密成功返回空字符串，失败返回错误信息
    """
    command = [util_path, 'fixarchive ', '--input', rpf_path, '--recursive']
    # print(command)
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    stdout, stderr = process.communicate()

    process.wait()

    # print(stdout.decode(errors='ignore'), stderr.decode(errors='ignore'))

    if stderr:
        return False, stderr.decode(errors='ignore')
    return True, ''
