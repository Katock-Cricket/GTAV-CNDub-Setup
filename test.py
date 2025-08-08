import sys

import clr

# 0. 把 DLL 所在目录加入搜索路径（按需修改）
DLL_DIR = r"E:\ai\GTA5_Chinese\tools\GTAV-CNDub-Setup\rpf_utils\CodeWalker"          # 你的 DLL 所在目录
sys.path.append(DLL_DIR)

# 1. 加载需要的 .NET 程序集
clr.AddReference("CodeWalker")
from CodeWalker.GameFiles import GTA5Keys, RpfFile

# 2. 运行参数（对应 C# 的局部变量）
RPF_PATH   = r"F:\GTAVE\update\update2.rpf"
INNER_PATH = "common"
GTA_FOLDER = r"F:\GTAVE"
IS_GEN9    = True

def find_directory(root, path: str):
    """
    递归查找目录，等价于 C# 的 FindDirectory
    """
    if not path:
        return root
    parts = [p for p in path.replace('\\', '/').split('/') if p]
    current = root
    for part in parts:
        # 注意 .NET 的属性/方法区分大小写，NameLower 返回小写
        current = next((d for d in current.Directories
                        if d.NameLower == part.lower()), None)
        if current is None:
            return None
    return current


def main():
    try:
        # 3. 加载密钥
        GTA5Keys.LoadFromPath(GTA_FOLDER, IS_GEN9, None)

        # 4. 加载并扫描 RPF
        rpf_file = RpfFile(RPF_PATH, "")
        rpf_file.ScanStructure(
            lambda status: print(f"[Status] {status}"),
            lambda error:  print(f"[Error]  {error}")
        )

        # 5. 查找内部目录
        inner_dir = find_directory(rpf_file.Root, INNER_PATH)
        if inner_dir:
            print(f"✅ Found directory: {inner_dir.Name}")
        else:
            print("❌ Directory not found.")

    except Exception as ex:
        print("❌ 程序运行时出错：", ex)


if __name__ == "__main__":
    main()