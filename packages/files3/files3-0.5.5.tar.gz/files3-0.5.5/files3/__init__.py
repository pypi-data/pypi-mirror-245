import os
import sys
import time

# 内核工具                      backend
from files3.basic_files import pyfile_basic_files  # 最基本的Files     basic Files
from files3.standard_files import pyfile_files  # 通用Files         normal Files

# 加壳工具(主要用于用户交互)                    shell tool(user frendly API)
from files3.pyfile_shell import pyfile_shell_basic, pyfile_shell
from files3._pfbool import PfBool, PfTrue, PfFalse
from files3._ipackage import PF_DTYPE as _PF_DTYPE
from files3._cmd_entry import _cmd_open, _cmd_show, _cmd_assoc, _cmd_unassoc

files = pyfile_shell  # std   files       # 标准功能files-shell(std)类
bfiles = pyfile_shell_basic  # basic files       # 内核files-shell(base)类

"""
files 带有魔法方法
bfiles只能进行最基本的单个增删改查(但是原理最简单，封装程度最浅，利于效率)

files with magic methods
bfiles can only perform the most basic single addition, deletion, modification and query (but the principle is the simplest and the encapsulation degree is the shallowest, which is conducive to efficiency)
"""

# 默认值                          default
files = files  # 作者常用        (the way author like)
Files = files
PyFile = files
PyFiles = files
pyfile = files
pyfiles = files

__version__ = "0.5.x"
__author__ = "Eagle'sBaby"
__doc__ = """
    (Based on pickle and lz4) save python object to file system and manage it (more convenient)
    install:
        pip install files3
        
        * After installation, you can use the command 'f3assoc .inst' to associate the '.inst' file with the 'f3open' program.
    
    quick start:
        from files3 import files
        f = files()  # save pyfile in current directory with default suffix '.inst'
        
        ## save python object (modify is also like save)
        f.set('a', 1)
        
        ## check if file exist
        f.has('a')  # True
        
        ## load python object
        print(f.get('a'))  # 1
        
        ## delete file
        f.delete('a')

    advanced:
        :Magic method is strongly recommended. It's more convenient and more powerful.
        
        from files3 import files
        f = files()
        
        ## Save
        f.a = 1
        # f['a'] = 1
        
        ## load
        print(f.a)  # 1
        # print(f['a'])  # 1
        
        ## delete
        del f.a
        # del f['a']
        
        ## check if file exist
        'a' in f  # False
        
        :Use other key not only str:
        1. tuple or list
        f[('a', 'b')] = [1, 2]
        print(f.a, f.b, f['a'], f['b'])  # 1, 2, [1, 2]
        
        2. slice
        print(f[:])  # [1, 2]
        # print(f[...])  # [1, 2]
        
        3. function
        print(f[lambda x: x == 'a'])  # 1
        
        4. re
        print(f[re.compile('a')])  # 1
        
        del f[...]
    Notice:
        There are some special case that you can't save:
        1. use f_A to save instance which contain f_A.
        2. use f_A to save pfbool object
        3. save object which do not have __getstate__ and __setstate__ method
    
    Cmd:
        f3 [name] [type] -d [dir]  # open a files3 object
        f3open [fpath]  # open a files3 object
        f3assoc [type]  # associate the '.type' file with the 'f3open' program
    Last: 
        It's really convinent but, because pickle is not safe, so mayn't use it to load the file you don't trust.
        However, if you do not care about it like me, you can use it to bring you a great programming experience.
"""


def cmd_show():
    if not _cmd_show():
        os.system("pause")


def cmd_open():
    if not _cmd_open():
        os.system("pause")


def cmd_assoc():
    if not _cmd_assoc():
        os.system("pause")


def cmd_unassoc():
    if not _cmd_unassoc():
        os.system("pause")


if __name__ == '__main__':
    import numpy as np

    f = files(r"C:\Users\22290\Desktop")
    # f.test = np.random.uniform(1, 10000, size=(10000, 10000))
    print(f.test)
    ...
    # files().a = [1, 2, 3]
    # exit(0)
    # import os
    # import sys
    # import winreg
    #
    #
    # def set_association(extension, exe_path):
    #     key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Classes', 0, winreg.KEY_SET_VALUE)
    #     winreg.SetValue(key, extension, winreg.REG_SZ, 'Python.File')
    #     winreg.SetValue(key, extension + '\\DefaultIcon', winreg.REG_SZ, exe_path + ',0')
    #     winreg.SetValue(key, extension + '\\shell\\open\\command', winreg.REG_SZ, exe_path + ' "%1" %*')
    #     print('File association set successfully.')
    #
    #
    # set_association('.inst', 'f3open.exe')
    # sys.argv = ["f3open", "a", ".inst"]
    # _cmd_show()
