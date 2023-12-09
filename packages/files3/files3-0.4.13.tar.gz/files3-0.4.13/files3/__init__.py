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

__version__ = "0.4.11"
__author__ = "Eagle'sBaby"
__doc__ = """

zh-cn:
    (基于pickle)将python对象以二进制保存到文件系统中，并对其进行管理(更方便?)
    主要功能展示(files):
    新建:
        from pyfile import files
        f = files()  # 在当前目录下储存pyfile文件
    增:
        py_obj = ["hello, world!", 114514, lambda *args: print(*args)]
        
        # 以下方式均可:
        f.py_obj = py_obj
        f["py_obj"] = py_obj
        f.set("py_obj", py_obj)     # ---
    删:
        f.a = 1
        f.b = "poi"
        
        # 删除a 以下方式均可:
        f.delete("a")
        del f["a"]
        del f.a     # ---
        
        # 同时删除a和b，除上述方法外，还可以:
        del f[('a', 'b')]
        del f[...]      # 删除所有
        del f[:]        # 删除所有
        # 上述索引方式对'增'、'删'、'改'、'查'操作同样有效
    改:
        same as '增'
    查:
        f.cs = [1, 2, 3, 4, 5, 6]
    
        # 查看有无'cs'这个pyfile文件
        f.has("cs")
        "cs" in f
        # 如果一次传入多个参数，则输出是各条件的and关系
        
        # 获取cs文件中储存的python对象
        print(f.cs)  # [1, 2, 3, 4, 5, 6]
        print(f['cs'])  # [1, 2, 3, 4, 5, 6]
    其他:
        pyfile文件加密:
        f.password = "NEVER GONNA GIVE YOU UP"
        f.encrypt("password")  # 在文件系统中会生成对应加密文件
        
        加密的pyfile文件的读取:
        #同正常的文件一样读取(续上)
        print(f.password)  # "NEVER GONNA GIVE YOU UP"
        # 加密的目的在于防止被其他第三方操作
        
        pyfile文件解密:
        f.decrypt("password")  # 在文件系统中会将对应加密文件还原为原始pyfile文件
        
en: (machine translate:)
    (pickle based) save Python objects in binary to the file system and manage them (more convenient?)
    Main function display (files):
    newly build:
        from pyfile import files
        f = files()     # stores pyfile files in the current directory
    
    Add:
        py_obj = ["hello, world!",  114514, lambda *args: print(*args)]
        
        # The following methods can be used:
        f.py_obj = py_obj
        f["py_obj"] = py_obj
        f.set("py_obj", py_obj)     # ---
    
    Delete:
        f.a = 1
        f.b = "poi"
        
        # Delete a either:
        f.delete("a")
        del f["a"]
        del f.a     # ---
    
        #Delete a and B at the same time. In addition to the above methods, you can also:
        del f['a', 'b']
        del f[...]      #  delete all
        del f [:]       #  delete all
        # The above indexing methods are also valid for add, delete, modify and query operations
    
    Change:
        Same as' Add '
    
    Query:
        f.cs = [1, 2, 3, 4, 5, 6]
        # Check for the 'CS' pyfile
        f.has("cs")
        "cs" in f
        # If multiple parameters are passed in at one time, the output is the AND relationship of each condition
        # Gets the python object stored in the CS file
        print(f.cs)  # [1, 2, 3, 4, 5, 6]
        print(f['cs'])  # [1, 2, 3, 4, 5, 6]
    
    Other:
        Pyfile file encryption:
            f.password = "NEVER GONNA GIVE YOU UP"
            f.encrypt ("password") # generates the corresponding encrypted file in the file system
    
        Reading encrypted pyfile file:
            # Read as normal files (Continued)
            print(f.password)  # "NEVER GONNA GIVE YOU UP"
            # The purpose of encryption is to prevent operation by other third parties
    
        Pyfile decryption:
            f.decrypt ("password") # in the file system, the corresponding encrypted file will be restored to the original pyfile file
     
"""



if __name__ == '__main__':
    files().a = [1, 2, 3]
    sys.argv = ["f3open", 'a.inst']
    _cmd_open()
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
