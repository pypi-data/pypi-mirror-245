#!/usr/bin/env python
# coding:utf-8
import os
import sys
import ctypes
import tempfile

from setuptools import find_packages, setup
from setuptools.command.install import install

class PostInstallCommand(install):
    # Post-installation for installation mode
    def run(self):
        # Run the original install command
        super().run()
        # Run the custom code to modify file association
        print("Associate .inst=f3open.exe")
        # Admin permission
        ctypes.windll.shell32.ShellExecuteW(None, 'runas', 'f3assoc', '.inst', None, 1)
        print('Done.')


setup(
    name='files3',
    version='0.4.14',
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
    cmdclass={
        'install': PostInstallCommand,
    },
)
