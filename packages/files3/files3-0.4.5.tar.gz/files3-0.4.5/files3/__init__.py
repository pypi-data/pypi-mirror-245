import os
import sys
import time
# 内核工具                      backend
from files3.basic_files import pyfile_basic_files  # 最基本的Files     basic Files
from files3.files import pyfile_files  # 通用Files         normal Files

# 加壳工具(主要用于用户交互)                    shell tool(user frendly API)
from files3.pyfile_shell import pyfile_shell_basic, pyfile_shell
from files3.PfBool import PfBool, PfTrue, PfFalse
from files3.InfoPackage import PF_DTYPE as _PF_DTYPE

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

__version__ = "0.4.5"
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

# add cmd
_cmd_show_doc_ = """
show files3 data by txt browser
f3 [fname] 
f3 [fname] [type]
f3 [fname] -i [dir]
f3 [fname] [type] -i [dir]
@example:
    f3 a [.inst]  # default type is .inst | default dir is ''
    f3 a .obj
    # f3 a obj  # is error
    f3 a -i /datum
    f3 a .obj -i /datum
"""


def _cmd_show():
    """
    f3 [fname]
    f3 [fname] [type]
    f3 [fname] -i [dir]
    f3 [fname] [type] -i [dir]
    :return:
    """
    args = sys.argv[1:]
    _len = len(args)
    # get dir fname type
    _dir, _fname, _type = "", "", _PF_DTYPE
    if (not _len and _len > 4) or \
            args[-1].startswith('-'):
        print(_cmd_show_doc_)
        return
    if _len > 1 and args[-2] == "-i":
        _dir = args[-1]
        args = args[:-2]

    if _len == 1:
        _fname = args[0]
    else:
        _fname, _type = args

    # check fname type dir |  1. not start with '-'
    if _fname.startswith("-") or _type.startswith("-") or _dir.startswith("-"):
        print(_cmd_show_doc_)
        return

    if _type is None:
        _f = files(_dir)
    else:
        _f = files(_dir, _type)

    _ = _f.get(_fname)

    if isinstance(_, PfBool):
        print("file not exists")
        return

    # 注入txt到临时目录
    _id = str(time.time())[::-1].replace('.', '')
    _path = os.path.join(_f.info.temp, f"{_fname},TEMP-{_id}.txt")
    with open(_path, "w", encoding="utf-8") as f:
        f.write(str(_))

    # 用系统默认打开方式打开txt, 不显示cmd窗口
    os.system(f"start /b {os.path.abspath(_path)}")

    print("open success")


_cmd_open_doc_ = """
open files3 data by txt browser
f3open [fpath]
@example:
    f3open -f /datum/a.inst
    f3open -f /datum/a.obj
    f3open -f /datum/a  # is error
"""


def _cmd_open():
    args = sys.argv[1:]
    # parse fname ftype dir
    _len = len(args)
    if _len != 2:
        print(_cmd_open_doc_)
        return
    _fpath = args[1]
    if not os.path.exists(_fpath):
        print("file not exists")
        return
    _fname, _type = os.path.splitext(os.path.basename(_fpath))
    _dir = os.path.dirname(_fpath)
    if _type == "":
        print("file type is empty")
        print(_cmd_open_doc_)
        return
    _f = files(_dir, _type)
    _ = _f.get(_fname)
    if isinstance(_, PfBool):
        print("file not exists")
        return

    # 注入txt到临时目录
    _id = str(time.time())[::-1].replace('.', '')
    _path = os.path.join(_f.info.temp, f"{_fname},TEMP-{_id}.txt")
    with open(_path, "w", encoding="utf-8") as f:
        f.write(str(_))

    # 用系统默认打开方式打开txt, 不显示cmd窗口
    os.system(f"start /b {os.path.abspath(_path)}")

    print("open success")


_cmd_assoc_doc_ = """
assoc specific file type to f3open
f3assoc [type]
@example:
    f3assoc .inst
    f3assoc .obj
    f3assoc .inst .obj  # is error
"""


def _cmd_assoc():
    # 获取python.exe的路径
    _python = sys.executable
    # 定位到Scripts/f3open.exe
    _f3open = os.path.join(os.path.dirname(_python), "Scripts", "f3open.exe")
    # 检查f3open.exe是否存在
    if not os.path.exists(_f3open):
        print("f3open.exe not exists")
        return
    # 获取文件类型
    args = sys.argv[1:]
    _len = len(args)
    if _len != 1:
        print(_cmd_assoc_doc_)
        return
    _type = args[0]
    if _type.startswith("."):
        _type = _type[1:]
    # 注册文件类型
    os.system(f"assoc .{_type}={_type}file")
    # 关联文件类型
    os.system(f"ftype {_type}file={_f3open} %1")
    print("assoc success")


if __name__ == '__main__':
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
