import os
import sys
from typing import List

import clr
from typing_extensions import Tuple

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(ROOT_DIR, 'gtautil'))
clr.AddReference("RPFUtilsLib")
from RpfUtilsLib import RpfUtils


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
        else:
            # 如果是文件夹，保留全部剩余部分
            inner_path = os.path.join(*remaining_parts)

    return inner_path


def import2rpf(input_dir: str, rpf_path: str, is_gen9: bool, gta_folder: str) -> Tuple[bool, str]:
    inner_path = get_inner_path(input_dir, rpf_path)
    # 从input_dir中获取待导入的文件或文件夹列表
    files_to_import = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if
                       os.path.isfile(os.path.join(input_dir, f))]
    print(rpf_path, inner_path, is_gen9, gta_folder, files_to_import)
    logs: List[str] = RpfUtils.ImportFilesToRpf(rpf_path, inner_path, gta_folder, is_gen9, files_to_import)
    if not logs:
        return False, "导入失败"
    # 拼接输出信息
    output = ""
    for log in logs:
        output += log + "\n"
    print(output)
    return True, output


if __name__ == '__main__':
    RPF_PATH = r"F:/GTAVE/mods/x64/audio/sfx/PAIN.rpf"
    INPUT_DIR = "gta5_chinese_dubbed/x64/audio/sfx/PAIN.rpf"
    GTA_FOLDER = "F:/GTAVE"
    ret, msg = import2rpf(INPUT_DIR, RPF_PATH, True, GTA_FOLDER)
    print(msg)
