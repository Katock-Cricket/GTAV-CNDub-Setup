import os

import py7zr


def extract_7z_with_password(zip_path: str, pwd: str, out_path) -> tuple[bool, str]:
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


