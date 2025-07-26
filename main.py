import json
import os
import tkinter as tk
import winreg
from tkinter import messagebox

import webview

from config import rpf_to_module, rpfs_to_install_static, update_rpfs_to_install
from installer import install_main, get_install_progress, get_output, uninstall_main

current_dir = os.path.dirname(os.path.realpath(__file__))
Assets = os.path.join(current_dir, 'Assets')


def is_webview2_installed():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}") as key:
            version = winreg.QueryValueEx(key, "pv")[0]
            return True
    except WindowsError:
        pass

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}") as key:
            version = winreg.QueryValueEx(key, "pv")[0]
            return True
    except WindowsError:
        pass

    return False


def check_dotnet_version():
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full") as key:
            release = winreg.QueryValueEx(key, "Release")[0]
            if release >= 461808:
                return True
            return False

    except WindowsError:
        return False


class API:
    def __init__(self):
        config = json.loads(open(f'{Assets}/config.json', 'r', encoding='utf-8').read())
        self.directory = config['game_dir']

    def select_directory(self):
        directory = webview.windows[0].create_file_dialog(webview.FOLDER_DIALOG)
        if directory:
            self.directory = directory[0]
            with open(f'{Assets}/config.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps({'game_dir': self.directory}, indent=4))
        return self.directory

    def install(self):
        install_main(self.directory)

    def uninstall(self):
        uninstall_main(self.directory)

    def install_progress(self):
        return get_install_progress()

    def get_log(self):
        return get_output()

    def update_modules(self, modules):
        rpf_list = []
        for rpf, module in rpf_to_module.items():
            if module in modules:
                rpf_list.append(rpf)

        new_val = {}
        for k, v in rpfs_to_install_static.items():
            if k in rpf_list:
                new_val[k] = v

        update_rpfs_to_install(new_val)

root = tk.Tk()
root.withdraw()

if __name__ == '__main__':
    api = API()

    if not check_dotnet_version():
        messagebox.showerror('错误',
                             '未检测到.NET Framework 4.7.2或更高版本，请先到pre_install文件夹中运行.NET安装程序。')

    if not is_webview2_installed():
        messagebox.showerror('错误', '未检测到WebView2运行时，请先到pre_install文件夹中运行WebView2安装程序。')

    webview.create_window(
        'GTAV中配MOD安装器丨Powered by Cyber蝈蝈总 和 鼠子Tomoriゞ ',
        f'{Assets}/UI/index.html',
        js_api=api,
        width=920,
        height=680
    )
    webview.start()
