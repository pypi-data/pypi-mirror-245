import os
import tempfile

def set_association(extension, exe_path):
    reg_content = f'''
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\\Software\\Classes\\{extension}]
@="Python.File"

[HKEY_CURRENT_USER\\Software\\Classes\\{extension}\\DefaultIcon]
@="{exe_path},0"

[HKEY_CURRENT_USER\\Software\\Classes\\{extension}\\shell\\open\\command]
@="\\"{exe_path}\\" \\"%1\\" %*"
'''
    # Write the .reg file
    with tempfile.NamedTemporaryFile(suffix='.reg', delete=False, mode='w') as f:
        f.write(reg_content)
        reg_file = f.name

    # Execute the .reg file
    os.system(f'regedit /s {reg_file}')

set_association('.py', 'python.exe')
