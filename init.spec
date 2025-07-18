# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['init.py'],
    pathex=[],
    binaries=[],
    datas=[('frontend/dist', 'frontend/dist')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Gestor de pacientes',
    icon='favicon.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # False = sin consola
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Gestor de pacientes',
)

app = BUNDLE(
    coll,
    name='Gestor de pacientes',
    bundle_identifier=None
)
