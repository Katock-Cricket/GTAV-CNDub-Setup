import os

cn_dub_mod = 'gta5_chinese_dubbed'
modloader_path = os.path.join('pre_install', 'OpenIV.asi')
hook_path = os.path.join('pre_install', 'dinput8.dll')

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
