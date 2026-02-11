import os

cn_dub_mod = 'gta5_chinese_dubbed'
modloader_path_legacy = os.path.join('pre_install', 'OpenIV.asi')
modloader_path_enhanced = os.path.join('pre_install', 'OpenRPF.asi')
hook_path_legacy = os.path.join('pre_install', 'dinput8.dll')
hook_path_enhanced = os.path.join('pre_install', 'xinput1_4.dll')
sign_file = 'Frontend/public/assets/GTA5中配MOD说明书.md'
sign_filename = 'GTAV_CNDub_Mod_By_CyberCricket_Bilibili.md'
_is_installing = False


def set_installing(value):
    global _is_installing
    _is_installing = value


def is_installing():
    global _is_installing
    return _is_installing


# key: rpf_path, value: mod_dir_path
rpfs_to_install_static = {
    'x64c.rpf': ['x64c.rpf/levels/gta5/props/lev_des/v_minigame.rpf'],
    'x64d.rpf': ['x64d.rpf/movies'],
    'update/update.rpf': ['update/update.rpf/x64/data/lang/chinesesimp_rel.rpf',
                          'update/update.rpf/x64/movies',
                          'update/update.rpf/x64/textures'],
    'update/update2.rpf': ['update/update.rpf/x64/data/lang/chinesesimp_rel.rpf'],
    'x64/audio/sfx/CUTSCENE_MASTERED_ONLY.rpf': ['x64/audio/sfx/CUTSCENE_MASTERED_ONLY.rpf'],
    'x64/audio/sfx/POLICE_SCANNER.rpf': ['x64/audio/sfx/POLICE_SCANNER.rpf'],
    'x64/audio/sfx/S_FULL_AMB_F.rpf': ['x64/audio/sfx/S_FULL_AMB_F.rpf'],
    'x64/audio/sfx/S_FULL_AMB_M.rpf': ['x64/audio/sfx/S_FULL_AMB_M.rpf'],
    'x64/audio/sfx/S_FULL_GAN.rpf': ['x64/audio/sfx/S_FULL_GAN.rpf'],
    'x64/audio/sfx/S_FULL_SER.rpf': ['x64/audio/sfx/S_FULL_SER.rpf'],
    'x64/audio/sfx/S_MINI_AMB.rpf': ['x64/audio/sfx/S_MINI_AMB.rpf'],
    'x64/audio/sfx/S_MINI_GAN.rpf': ['x64/audio/sfx/S_MINI_GAN.rpf'],
    'x64/audio/sfx/S_MINI_SER.rpf': ['x64/audio/sfx/S_MINI_SER.rpf'],
    'x64/audio/sfx/PAIN.rpf': ['x64/audio/sfx/PAIN.rpf'],
    'x64/audio/sfx/PROLOGUE.rpf': ['x64/audio/sfx/PROLOGUE.rpf'],
    'x64/audio/sfx/S_MISC.rpf': ['x64/audio/sfx/S_MISC.rpf'],
    'x64/audio/sfx/SS_AC.rpf': ['x64/audio/sfx/SS_AC.rpf'],
    'x64/audio/sfx/SS_DE.rpf': ['x64/audio/sfx/SS_DE.rpf'],
    'x64/audio/sfx/SS_FF.rpf': ['x64/audio/sfx/SS_FF.rpf'],
    'x64/audio/sfx/SS_GM.rpf': ['x64/audio/sfx/SS_GM.rpf'],
    'x64/audio/sfx/SS_NP.rpf': ['x64/audio/sfx/SS_NP.rpf'],
    'x64/audio/sfx/SS_QR.rpf': ['x64/audio/sfx/SS_QR.rpf'],
    'x64/audio/sfx/SS_ST.rpf': ['x64/audio/sfx/SS_ST.rpf'],
    'x64/audio/sfx/SS_UZ.rpf': ['x64/audio/sfx/SS_UZ.rpf']
}

mod_dir_to_module = {
    'x64c.rpf/levels/gta5/props/lev_des/v_minigame.rpf': '周边汉化',
    'x64d.rpf/movies': '周边汉化',
    'update/update.rpf/x64/movies': '主角配音',
    'update/update.rpf/x64/data/lang/chinesesimp_rel.rpf': '配套字幕',
    'update/update.rpf/x64/textures': '周边汉化',
    'x64/audio/sfx/CUTSCENE_MASTERED_ONLY.rpf': '剧情配音',
    'x64/audio/sfx/POLICE_SCANNER.rpf': 'NPC配音',
    'x64/audio/sfx/S_FULL_AMB_F.rpf': 'NPC配音',
    'x64/audio/sfx/S_FULL_AMB_M.rpf': 'NPC配音',
    'x64/audio/sfx/S_FULL_GAN.rpf': 'NPC配音',
    'x64/audio/sfx/S_FULL_SER.rpf': 'NPC配音',
    'x64/audio/sfx/S_MINI_AMB.rpf': 'NPC配音',
    'x64/audio/sfx/S_MINI_GAN.rpf': 'NPC配音',
    'x64/audio/sfx/S_MINI_SER.rpf': 'NPC配音',
    'x64/audio/sfx/PAIN.rpf': '主角配音',
    'x64/audio/sfx/PROLOGUE.rpf': '剧情配音',
    'x64/audio/sfx/S_MISC.rpf': '主角配音',
    'x64/audio/sfx/SS_AC.rpf': '剧情配音',
    'x64/audio/sfx/SS_DE.rpf': '剧情配音',
    'x64/audio/sfx/SS_FF.rpf': '剧情配音',
    'x64/audio/sfx/SS_GM.rpf': '剧情配音',
    'x64/audio/sfx/SS_NP.rpf': '剧情配音',
    'x64/audio/sfx/SS_QR.rpf': '剧情配音',
    'x64/audio/sfx/SS_ST.rpf': '剧情配音',
    'x64/audio/sfx/SS_UZ.rpf': '剧情配音'
}

modules = ['主角配音', '剧情配音', '周边汉化', '配套字幕', 'NPC配音']


def get_modules():
    return modules


def update_modules(new_modules):
    global modules
    modules = new_modules


asi_loaders = [
    "d3d8.dll",
    "d3d9.dll",
    "d3d10.dll",
    "d3d11.dll",
    "d3d12.dll",
    "ddraw.dll",
    "dinput.dll",
    "dinput8.dll",
    "dsound.dll",
    "msacm32.dll",
    "msvfw32.dll",
    "version.dll",
    "wininet.dll",
    "winmm.dll",
    "winhttp.dll",
    "xlive.dll",
    "binkw32.dll",
    "bink2w32.dll",
    "binkw64.dll",
    "bink2w64.dll",
    "vorbisFile.dll",
    "xinput1_1.dll",
    "xinput1_2.dll",
    "xinput1_3.dll",
    "xinput1_4.dll",
    "xinput9_1_0.dll",
    "xinputuap.dll"
]
