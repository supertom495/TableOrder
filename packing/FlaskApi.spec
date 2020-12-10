# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['..\\api\\run_server.py'],
             pathex=['C:\\Users\\PC-BURWOOD\\Documents\\TableOrder\\packing'],
             binaries=[('./api-ms-win-crt-runtime-l1-1-0.dll', '.')],
             datas=[('C:\\Users\\PC-BURWOOD\\Documents\\TableOrder\\api\\templates\\', 'templates')],
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='FlaskApi',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='iconfinder_shrimp-prawn-seafood-animal-marine_3558097.ico')
