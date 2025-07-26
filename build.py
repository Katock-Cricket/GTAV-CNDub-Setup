import argparse
import json
import multiprocessing
import shutil
import subprocess

import py7zr

from config import *
from encrypt import get_pwd


def package_exe(dist_path) -> bool:
    try:
        os.system(f'conda activate GTAV-CNDub-Setup && pyinstaller build.spec --distpath {dist_path}')
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

    if isinstance(v, str):
        v = [v]

    for dir in v:
        rpf_dir_path = os.path.join(cn_dub_mod, dir)

        if not os.path.exists(rpf_dir_path):
            print(f'RPF {dir} not found in mod directory.')
            return

        inner_path = f'{cn_dub_mod}/{dir}'
        print(f'Processing {dir}...')
        with py7zr.SevenZipFile(mod_zip_path, 'w', password=get_pwd(), header_encryption=True) as archive:
            archive.writeall(rpf_dir_path, inner_path)
            print(f'Dir {dir} compressed to {mod_zip_path}.')


def copy_sign_to_rpf_dirs(rpf_dir_list):
    sign_file = os.path.join(cn_dub_mod, sign_filename)
    if not os.path.exists(sign_file):
        print("Sign File doesn't exist, skip copying")
        return

    for i, v, _ in rpf_dir_list:
        if isinstance(v, str):
            v = [v]

        for dir in v:
            rpf_dir = os.path.join(cn_dub_mod, dir)
            if not os.path.exists(rpf_dir):
                continue

            shutil.copy(sign_file, os.path.join(rpf_dir, sign_filename))


def zip_mod_with_encrypt(args_list):
    """
    使用多进程并行打包并加密MOD
    """
    # 准备参数列表

    if not os.path.exists(paks_dir):
        os.makedirs(paks_dir, exist_ok=True)

    # 创建进程池
    with multiprocessing.Pool(processes=max(1, multiprocessing.cpu_count() - 2)) as pool:
        pool.map(process_file, args_list)


def signtool(filename):
    signtool_exe = r'C:/Program Files (x86)/Windows Kits/10/bin/10.0.22621.0/x64/signtool.exe'  # signtool exe
    pfx_file = r'./sig/certificate.pfx'  # pfx位置
    if not os.path.exists(signtool_exe) or not os.path.exists(pfx_file):
        print('signtool.exe or certificate.pfx not found. Skip signing.')
        return
    pwd = json.loads(open('sig/pwd.json', 'r').read())['pwd']
    cmd = f'%s sign /f %s /p {pwd} /v /fd SHA256 %s' % (signtool_exe, pfx_file, filename)
    proc = subprocess.Popen(cmd)
    proc.wait()


def build_main(args):
    args_list = [(i, v, cn_dub_mod) for i, (k, v) in enumerate(rpfs_to_install_static.items())]

    if args.build_frontend:
        build_frontend()
        print('Frontend built.')

    if args.copy_sign_file:
        copy_sign_to_rpf_dirs(args_list)
        print('Copied sign files to rpf dirs.')

    if args.zip_and_encrypt_mod:
        zip_mod_with_encrypt(args_list)
        print('MOD compressed and encrypted.')

    if args.pack_exe:
        package_exe(args.dist_path)
        signtool(os.path.join(args.dist_path, 'GTAV中配MOD安装器.exe'))
        print('Executable built.')

    if args.copy_utils:
        for item in ['gtautil', 'pre_install']:
            if os.path.exists(item):
                shutil.copytree(item, os.path.join(args.dist_path, item), dirs_exist_ok=True)
        print('Utils copied.')

    if args.copy_paks:
        shutil.copytree(paks_dir, os.path.join(args.dist_path, 'paks'), dirs_exist_ok=True)
        print('Paks copied.')

    print('Build finished.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--build_frontend', action='store_true', default=True, help='是否重新编译前端页面')
    parser.add_argument('--copy-sign-file', action='store_true', default=True, help='拷贝签名文件到每个RPF文件夹')
    parser.add_argument('--zip-and-encrypt-mod', action='store_true', default=False, help='是否压缩并加密MOD，更新pak')
    parser.add_argument('--pack-exe', action='store_true', default=True, help='是否打包exe')
    parser.add_argument('--copy-utils', action='store_true', default=False, help='是否拷贝其他工具依赖')
    parser.add_argument('--copy-paks', action='store_true', default=False, help='是否拷贝pak')
    parser.add_argument('--dist_path', default='E:/ai/GTA5_Chinese/gta5_chinese_dubbed', help='最终路径')
    args = parser.parse_args()

    build_main(args)
