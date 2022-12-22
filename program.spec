# -*- mode: python ; coding: UTF-8 -*-

import sys  
sys.setrecursionlimit(5000)

block_cipher = None

added_files = [ ('./face-alignment/utils.py', './face-alignment'),
                ('./face-alignment', './face-alignment')]

a = Analysis(['./ui.py'],
            pathex=['C:\\Users\\JeeheonKim\\id_photo2\\id_photo'],
            binaries=[],
            datas=added_files,
            hiddenimports=['scipy', 'cv2', 'torch', 'skimage', 'skimage.io', 'distutils.version', 'numba', 'numba.jit'],
            hookspath=[],
            runtime_hooks=[],
            excludes=[],
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=block_cipher,
            noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
            cipher=block_cipher)
            
exe = EXE(pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='Person De-ID',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        uac_admin=False,
        icon='./img.ico')
coll = COLLECT(exe,
            a.binaries,
            a.zipfiles,
            a.datas,
            strip=False,
            upx=True,
            upx_exclude=[],
            name='Person De-ID')