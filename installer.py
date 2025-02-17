import os
import shutil
import sys
import threading
import tkinter as tk
from time import sleep
from tkinter import messagebox
from tkinter import scrolledtext

from base_utils import extract_rpf, build_rpf

game_dir = ''
mods_path = os.path.join(game_dir, 'mods')
sfx_root = os.path.join(game_dir, 'x64', 'audio', 'sfx')
update_rpf = os.path.join(game_dir, 'update', 'update.rpf')
update2_rpf = os.path.join(game_dir, 'update', 'update2.rpf')
tv_rpf = os.path.join(game_dir, 'x64d.rpf')
tmp_path = os.path.join(game_dir, 'tmp')
cn_dub_mod = 'gta5_chinese_dubbed'
# if getattr(sys, 'frozen', False):
#     modloader_path = os.path.join(sys._MEIPASS, 'pre_install', 'OpenIV.asi')
# else:
#     modloader_path = os.path.join('pre_install', 'OpenIV.asi')
modloader_path = os.path.join('pre_install', 'OpenIV.asi')

sfx_rpf_list: list[str] = [
    'CUTSCENE_MASTERED_ONLY.rpf'
    'PAIN.rpf',
    'PROLOGUE.rpf',
    'S_MISC.rpf',
    'SS_AC.rpf',
    'SS_DE.rpf',
    'SS_FF.rpf',
    'SS_GM.rpf',
    'SS_NP.rpf',
    'SS_QR.rpf',
    'SS_ST.rpf',
    'SS_UZ.rpf',
]


def set_game_dir(new_dir: str):
    global game_dir, mods_path, sfx_root, update_rpf, update2_rpf, tv_rpf, tmp_path
    game_dir = new_dir
    mods_path = os.path.join(game_dir, 'mods')
    sfx_root = os.path.join(game_dir, 'x64', 'audio', 'sfx')
    update_rpf = os.path.join(game_dir, 'update', 'update.rpf')
    update2_rpf = os.path.join(game_dir, 'update', 'update2.rpf')
    tv_rpf = os.path.join(game_dir, 'x64d.rpf')
    tmp_path = os.path.join(game_dir, 'tmp')


def clear_cache():
    if os.path.exists(tmp_path):
        shutil.rmtree(tmp_path)


def is_installed(game_dir):
    set_game_dir(game_dir)
    if os.path.exists(os.path.join(mods_path, 'x64d.rpf')):
        return True

    for rpf in sfx_rpf_list:
        if os.path.exists(os.path.join(mods_path, 'x64', 'audio', 'sfx', rpf)):
            return True

    return False


def install_modloader():
    if not os.path.exists(os.path.join(game_dir, 'OpenIV.asi')):
        shutil.copy(modloader_path, os.path.join(game_dir, 'OpenIV.asi'))
        append_output("提示: 未安装挂载器OpenIV.asi，已自动为你安装\n")


def install_tv():
    append_output(f'解析原电视节目{tv_rpf}...\n')
    ret = extract_rpf(game_dir, tmp_path, tv_rpf)
    append_output(ret + f'\n解析原电视节目{tv_rpf}完成\n')

    append_output(f'拷贝电视节目MOD到{tv_rpf}...\n')
    mod_root = os.path.join(cn_dub_mod, 'x64d.rpf', 'movies')
    for file in os.listdir(mod_root):
        mod_file = os.path.join(mod_root, file)
        ori_file = os.path.join(tmp_path, 'x64d.rpf', 'movies', file)
        os.remove(ori_file)
        shutil.copy(mod_file, ori_file)
    append_output(f'拷贝电视节目MOD到{tv_rpf}完成\n')

    append_output(f'构建电视节目 mod {tv_rpf}...\n')
    ret = build_rpf(game_dir, os.path.join(tmp_path, 'x64d.rpf'), mods_path)
    append_output(ret + f'\n构建电视节目 mod {tv_rpf} 完成\n')


def install_sfx():
    for rpf in sfx_rpf_list:
        mod_root = os.path.join(cn_dub_mod, 'x64', 'audio', 'sfx', rpf)
        if not os.path.exists(mod_root):
            continue

        append_output(f'解析原音频{rpf}...\n')
        ret = extract_rpf(game_dir, tmp_path, os.path.join(sfx_root, rpf))
        append_output(ret + f'\n解析音频{rpf}完成\n')

        append_output(f'拷贝音频MOD到{rpf}...\n')
        for file in os.listdir(mod_root):
            mod_file = os.path.join(mod_root, file)
            ori_file = os.path.join(tmp_path, rpf, file)
            os.remove(ori_file)
            shutil.copy(mod_file, ori_file)
        append_output(f'拷贝音频MOD到{rpf}完成\n')

        target_path = os.path.join(mods_path, 'x64', 'audio', 'sfx')
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        append_output(f'构建音频 mod {rpf}...\n')
        ret = build_rpf(game_dir, os.path.join(tmp_path, rpf), target_path)
        append_output(ret + f'\n构建音频 mod {rpf} 完成，请等待其他部件安装完成\n')


def install_subtitles():
    mod_root = os.path.join(cn_dub_mod, 'update', 'update.rpf', 'x64', 'data', 'lang', 'chinesesimp_rel.rpf')
    ori_rpf = update_rpf

    if not os.path.exists(os.path.join(game_dir, 'update', 'update.rpf')):
        if not os.path.exists(os.path.join(game_dir, 'update', 'update2.rpf')):
            raise AssertionError('无法找到update.rpf或update2.rpf')
        ori_rpf = update2_rpf

    rpf_name = os.path.basename(ori_rpf)

    append_output(f'解析原字幕{rpf_name}...\n')
    ret = extract_rpf(game_dir, tmp_path, ori_rpf)
    append_output(ret + f'\n解析字幕{rpf_name}完成\n')
    append_output(f'拷贝字幕MOD到{rpf_name}...\n')
    for file in os.listdir(mod_root):
        mod_file = os.path.join(mod_root, file)
        ori_file = os.path.join(tmp_path, rpf_name, 'x64', 'data', 'lang', 'chinesesimp_rel.rpf', file)
        os.remove(ori_file)
        shutil.copy(mod_file, ori_file)
    append_output(f'拷贝字幕MOD到{rpf_name}完成，请等待其他部件安装完成\n')

    target_path = os.path.join(mods_path, 'update')
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    append_output(f'构建字幕 mod {rpf_name}...\n')
    ret = build_rpf(game_dir, os.path.join(tmp_path, rpf_name), target_path)
    append_output(ret + f'构建字幕 mod {rpf_name} 完成，请等待其他部件安装完成\n')


window = None
text_box = None


def init_window():
    global window, text_box
    window = tk.Tk()
    window.title("工作进度")

    text_box = scrolledtext.ScrolledText(window, width=80, height=20, wrap=tk.WORD, state=tk.DISABLED)
    text_box.pack(padx=10, pady=10)


def append_output(text):
    if not window or not text_box:
        raise AssertionError("窗口未初始化")

    text_box.config(state=tk.NORMAL)
    text_box.insert(tk.END, text)
    text_box.yview(tk.END)  # Scroll to the bottom
    text_box.config(state=tk.DISABLED)





def install_main(game_dir, uninstall=False):
    working = [True]
    set_game_dir(game_dir)

    def install_tv_wrapper():
        append_output('--------安装中配电视节目...拷贝并挂载文件需要一段时间，请耐心等待\n')
        install_tv()
        if not working[0]:
            clear_cache()
            return

    def install_sfx_wrapper():
        append_output('--------安装中配音频...拷贝并挂载文件需要一段时间，请耐心等待\n')
        install_sfx()
        if not working[0]:
            clear_cache()
            return

    def install_subtitles_wrapper():
        append_output('--------安装中配字幕...拷贝并挂载文件需要一段时间，请耐心等待\n')
        install_subtitles()
        if not working[0]:
            clear_cache()
            return

    def install_pipeline():
        try:
            append_output("开始安装...程序结束前请勿关闭此窗口和安装器\n")

            if not os.path.exists(game_dir) or not os.path.exists(os.path.join(game_dir, 'x64')):
                raise AssertionError('游戏目录无效，请检查路径是否正确')
            clear_cache()
            os.makedirs(tmp_path)

            os.system('chcp 65001 > nul')
            if not os.path.exists(mods_path):
                os.makedirs(mods_path)
                append_output("提示: mods目录不存在，已自动创建\n")

            install_modloader()

            # append_output('初始化缓存...请耐心等待\n')
            # init_cache(game_dir)
            # if not working[0]:
            #     clear_cache()
            #     return
            # append_output('缓存初始化完成\n')

            # 并行安装音频、电视节目、字幕
            tv_thread = threading.Thread(target=install_tv_wrapper)
            sfx_thread = threading.Thread(target=install_sfx_wrapper)
            subtitles_thread = threading.Thread(target=install_subtitles_wrapper)

            tv_thread.start()
            sfx_thread.start()
            subtitles_thread.start()

            tv_thread.join()
            sfx_thread.join()
            subtitles_thread.join()

            append_output('--------清理缓存...\n')
            clear_cache()

            append_output('--------安装完成\n')
            sleep(2)
            window.quit()

        except Exception as e:
            append_output(f"错误: {str(e)}\n")
            messagebox.showerror("安装错误", f"安装过程中出现错误: {str(e)}")

    def uninstall_pipeline():
        try:
            append_output('卸载音频中...')
            for rpf in os.listdir(os.path.join(cn_dub_mod, 'x64', 'audio', 'sfx')):
                rpf_path = os.path.join(mods_path, 'x64', 'audio', 'sfx', rpf)
                if os.path.exists(rpf_path):
                    os.remove(rpf_path)

            append_output('卸载电视节目中...')
            tv_rpf_path = os.path.join(mods_path, 'x64d.rpf')
            if os.path.exists(tv_rpf_path):
                os.remove(tv_rpf_path)

            append_output('卸载完成！字幕请酌情手动卸载，删除mods/update可能影响其他已安装的MOD')

        except Exception as e:
            append_output(f"错误: {str(e)}\n")
            messagebox.showerror("卸载错误", f"卸载过程中出现错误: {str(e)}")

    init_window()

    if not uninstall:
        threading.Thread(target=install_pipeline, daemon=True).start()
    else:
        threading.Thread(target=uninstall_pipeline, daemon=True).start()

    def on_close():
        working[0] = False
        window.quit()

    window.protocol("WM_DELETE_WINDOW", on_close)

    window.mainloop()
