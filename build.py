import argparse
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


def zip_mod_with_encrypt(mod_zip_path: str = f'{cn_dub_mod}.pak'):
    """
    打包时使用，压缩并加密MOD
    """
    with py7zr.SevenZipFile(mod_zip_path, 'w', password=get_pwd()) as archive:
        archive.writeall(cn_dub_mod)


def build_main(args):
    if args.build_frontend:
        build_frontend()
        print('Frontend built.')

    if args.zip_and_encrypt_mod:
        zip_mod_with_encrypt()
        print('MOD compressed and encrypted.')

    ret = package_exe(args.dist_path)
    if not ret:
        return

    print('Executable built.')

    # 拷贝组件到dist_path
    for item in ['gtautil', 'pre_install']:
        if os.path.exists(item):
            shutil.copytree(item, os.path.join(args.dist_path, item), dirs_exist_ok=True)
    shutil.copyfile(f'{cn_dub_mod}.pak', os.path.join(args.dist_path, f'{cn_dub_mod}.pak'))
    print('Build finished.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--build_frontend', action='store_true', default=False,
                        help='是否重新编译前端页面')
    parser.add_argument('--zip-and-encrypt-mod', action='store_true', default=False, help='是否压缩并加密MOD')
    parser.add_argument('--mod_path', default='', help='MOD本体文件路径')
    parser.add_argument('--dist_path', default='E:/ai/GTA5_Chinese/gta5_chinese_dubbed',
                        help='最终MOD包路径')
    args = parser.parse_args()

    build_main(args)
