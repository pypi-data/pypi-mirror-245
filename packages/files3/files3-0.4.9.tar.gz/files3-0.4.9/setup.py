#!/usr/bin/env python
# coding:utf-8
import os
import sys
import tempfile

from setuptools import find_packages, setup
from setuptools.command.install import install


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

class PostInstallCommand(install):
    # Post-installation for installation mode
    def run(self):
        # Run the original install command
        super().run()
        # Run the custom code to modify file association
        set_association('.inst', 'f3open.exe')
        print('Done.')


setup(
    name='files3',
    version='0.4.9',
    description='(pickle+lz4 based) save Python objects in binary to the file system and manage them.',
    author_email='2229066748@qq.com',
    maintainer="Eagle'sBaby",
    maintainer_email='2229066748@qq.com',
    packages=find_packages(),
    license='Apache Licence 2.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
    ],
    keywords=['pickle', 'lz4', 'file system', 'file management'],
    python_requires='>=3',
    install_requires=[
        "lz4",
    ],
    entry_points={
        'console_scripts': [
            'f3 = files3:_cmd_show',
            'f3open = files3:_cmd_open',
            'f3assoc = files3:_cmd_assoc',
            'f3unassoc = files3:_cmd_unassoc',
        ],
    },
    # cmdclass={
    #     'install': PostInstallCommand,
    # },
)
