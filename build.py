import argparse
import multiprocessing
import shutil

import py7zr

from config import *
from encrypt import get_pwd


def package_exe(dist_path) -> bool:
    try:
        os.system(f'pyinstaller build.spec --distpath {dist_path}')
    except Exception as e:
        print(f'Build failed: {e}')
        return False

    return True


def build_frontend():
    """构建前端资源"""
    os.chdir('Frontend')
    os.system('npm run build')
    os.chdir('..')


def process_file(args):
    """单个文件的打包处理函数"""
    i, v, cn_dub_mod = args
    mod_zip_path = os.path.join(paks_dir, f'{cn_dub_mod}_{i}.pak')
    rpf_dir_path = os.path.join(cn_dub_mod, v)

    if not os.path.exists(rpf_dir_path):
        print(f'RPF {v} not found in mod directory.')
        return

    inner_path = f'{cn_dub_mod}/{v}'
    print(f'Processing {v}...')
    with py7zr.SevenZipFile(mod_zip_path, 'w', password=get_pwd(), header_encryption=True) as archive:
        archive.writeall(rpf_dir_path, inner_path)
        print(f'RPF {v} compressed to {mod_zip_path}.')


def zip_mod_with_encrypt():
    """
    使用多进程并行打包并加密MOD
    """
    # 准备参数列表
    args_list = [(i, v, cn_dub_mod) for i, (k, v) in enumerate(rpfs_to_install.items())]

    if not os.path.exists(paks_dir):
        os.makedirs(paks_dir, exist_ok=True)

    # 创建进程池
    with multiprocessing.Pool(processes=6) as pool:
        pool.map(process_file, args_list)


def build_main(args):
    if args.build_frontend:
        build_frontend()
        print('Frontend built.')

    if args.zip_and_encrypt_mod:
        zip_mod_with_encrypt()
        print('MOD compressed and encrypted.')

    if args.pack_exe:
        package_exe(args.dist_path)
        print('Executable built.')

    # 拷贝组件到dist_path
    for item in ['gtautil', 'pre_install']:
        if os.path.exists(item):
            shutil.copytree(item, os.path.join(args.dist_path, item), dirs_exist_ok=True)
    shutil.copytree(paks_dir, os.path.join(args.dist_path, 'paks'), dirs_exist_ok=True)

    print('Build finished.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--build_frontend', action='store_true', default=False,
                        help='是否重新编译前端页面')
    parser.add_argument('--zip-and-encrypt-mod', action='store_true', default=False, help='是否压缩并加密MOD')
    parser.add_argument('--pack-exe', action='store_true', default=True, help='是否打包exe')
    parser.add_argument('--mod_path', default='', help='MOD本体文件路径')
    parser.add_argument('--dist_path', default='E:/ai/GTA5_Chinese/gta5_chinese_dubbed',
                        help='最终MOD包路径')
    args = parser.parse_args()

    build_main(args)
