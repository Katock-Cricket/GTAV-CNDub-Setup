import os
import sys

import py7zr


def load_password_from_file(password_filename: str = "pwd.txt") -> tuple[bool, str]:
    def get_resource_path(relative_path: str) -> str:
        try:
            # PyInstaller 创建一个临时文件夹并将路径存储在 _MEIPASS 中
            # (适用于单文件 --onefile 模式)
            base_path = sys._MEIPASS
        except AttributeError:
            # 如果 _MEIPASS 不存在，说明是在开发环境中运行 (不是打包后的 exe)
            # 或者是在 --onedir 模式下，文件在可执行文件旁边
            base_path = os.path.abspath(".")
            # 如果是 --onedir 模式，可执行文件和数据文件在同一目录
            # 如果脚本在子目录运行，可能需要调整为 os.path.dirname(sys.executable)
            # 对于大多数情况，os.path.abspath(".") 配合 .spec 文件中的 ('pwd.txt', '.') 即可
        return os.path.join(base_path, relative_path)

    try:
        password_file_path = get_resource_path(password_filename)
        if not os.path.exists(password_file_path):
            return False, f"密码文件 '{password_file_path}' 未找到。"

        with open(password_file_path, 'r', encoding='utf-8') as f:
            password = f.read().strip()
        if not password:
            return False, f"密码文件 '{password_file_path}' 为空。"
        return True, password
    except Exception as e:
        return False, f"读取密码文件时发生错误: {e}"


def extract_7z_with_password(zip_path: str, pwd: str, out_path: str) -> tuple[bool, str]:
    if not os.path.exists(zip_path):
        return False, f"压缩文件 '{zip_path}' 不存在。"

    if not os.path.exists(out_path) or not os.path.isdir(out_path):
        return False, f"输出路径 '{out_path}' 不合法"

    try:
        with py7zr.SevenZipFile(zip_path, mode='r', password=pwd) as z:
            z.extractall(path=out_path)
        return True, "解压成功！"
    except py7zr.exceptions.PasswordRequired:
        return False, "需要密码，但未提供或提供的密码不正确。"
    except py7zr.exceptions.Bad7zFile:
        return False, "文件不是有效的 7z 压缩文件，或者文件已损坏。"
    except Exception as e:
        return False, f"解压过程中发生未知错误: {e}"


if __name__ == '__main__':
    ret, pwd = load_password_from_file()
    print(ret, pwd)
    # if ret:
    #     ret, msg = extract_7z_with_password('gta5_chinese_dubbed.7z', pwd, './')
    #     print(ret, msg)
