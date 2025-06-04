import os

cn_dub_mod = 'gta5_chinese_dubbed'
modloader_path = os.path.join('pre_install', 'OpenIV.asi')
hook_path = os.path.join('pre_install', 'dinput8.dll')
paks_dir = 'paks'

# key: rpf_path, value: mod_dir_path
rpfs_to_install = {
    'x64d.rpf': 'x64d.rpf/movies',
    'update/update.rpf': 'update/update.rpf/x64/data/lang/chinesesimp_rel.rpf',
    'update/update2.rpf': 'update/update.rpf/x64/data/lang/chinesesimp_rel.rpf',
    'x64/audio/sfx/CUTSCENE_MASTERED_ONLY.rpf': 'x64/audio/sfx/CUTSCENE_MASTERED_ONLY.rpf',
    'x64/audio/sfx/POLICE_SCANNER.rpf': 'x64/audio/sfx/POLICE_SCANNER.rpf',
    'x64/audio/sfx/S_FULL_AMB_F.rpf': 'x64/audio/sfx/S_FULL_AMB_F.rpf',
    'x64/audio/sfx/S_FULL_AMB_M.rpf': 'x64/audio/sfx/S_FULL_AMB_M.rpf',
    'x64/audio/sfx/S_FULL_GAN.rpf': 'x64/audio/sfx/S_FULL_GAN.rpf',
    'x64/audio/sfx/S_FULL_SER.rpf': 'x64/audio/sfx/S_FULL_SER.rpf',
    'x64/audio/sfx/S_MINI_AMB.rpf': 'x64/audio/sfx/S_MINI_AMB.rpf',
    'x64/audio/sfx/S_MINI_GAN.rpf': 'x64/audio/sfx/S_MINI_GAN.rpf',
    'x64/audio/sfx/S_MINI_SER.rpf': 'x64/audio/sfx/S_MINI_SER.rpf',
    'x64/audio/sfx/PAIN.rpf': 'x64/audio/sfx/PAIN.rpf',
    'x64/audio/sfx/PROLOGUE.rpf': 'x64/audio/sfx/PROLOGUE.rpf',
    'x64/audio/sfx/S_MISC.rpf': 'x64/audio/sfx/S_MISC.rpf',
    'x64/audio/sfx/SS_AC.rpf': 'x64/audio/sfx/SS_AC.rpf',
    'x64/audio/sfx/SS_DE.rpf': 'x64/audio/sfx/SS_DE.rpf',
    'x64/audio/sfx/SS_FF.rpf': 'x64/audio/sfx/SS_FF.rpf',
    'x64/audio/sfx/SS_GM.rpf': 'x64/audio/sfx/SS_GM.rpf',
    'x64/audio/sfx/SS_NP.rpf': 'x64/audio/sfx/SS_NP.rpf',
    'x64/audio/sfx/SS_QR.rpf': 'x64/audio/sfx/SS_QR.rpf',
    'x64/audio/sfx/SS_ST.rpf': 'x64/audio/sfx/SS_ST.rpf',
    'x64/audio/sfx/SS_UZ.rpf': 'x64/audio/sfx/SS_UZ.rpf'
}

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
