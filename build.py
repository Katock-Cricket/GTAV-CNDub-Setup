import argparse
import json
import shutil
import subprocess

from config import *


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


def copy_sign_to_rpf_dirs():
    if not os.path.exists(sign_file):
        print("Sign File doesn't exist, skip copying")
        return

    for root, dirs, files in os.walk(cn_dub_mod):
        for dir in dirs:
            shutil.copy(sign_file, os.path.join(root, dir, sign_filename))


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
    if args.build_frontend:
        build_frontend()
        print('Frontend built.')

    if args.copy_sign_file:
        copy_sign_to_rpf_dirs()
        print('Copied sign files to rpf dirs.')

    if args.pack_exe:
        package_exe(args.dist_path)
        signtool(os.path.join(args.dist_path, 'GTAV中配MOD安装器.exe'))
        print('Executable built.')

    if args.copy_utils:
        if os.path.exists('pre_install'):
            shutil.copytree('pre_install', os.path.join(args.dist_path, 'pre_install'), dirs_exist_ok=True)
        print('Utils copied.')

    if args.copy_mod_dir:
        shutil.copytree(cn_dub_mod, os.path.join(args.dist_path, cn_dub_mod), dirs_exist_ok=True)
        print('mods copied.')

    print('Build finished.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--build_frontend', action='store_true', default=True, help='是否重新编译前端页面')
    parser.add_argument('--copy-sign-file', action='store_true', default=True, help='拷贝签名文件到每个RPF文件夹')
    parser.add_argument('--pack-exe', action='store_true', default=True, help='是否打包exe')
    parser.add_argument('--copy-utils', action='store_true', default=True, help='是否拷贝其他工具依赖')
    parser.add_argument('--copy-mod-dir', action='store_true', default=True, help='是否拷贝mod本体')
    parser.add_argument('--dist_path', default='E:/ai/GTA5_Chinese/gta5_chinese_dubbed', help='最终路径')
    args = parser.parse_args()

    build_main(args)
