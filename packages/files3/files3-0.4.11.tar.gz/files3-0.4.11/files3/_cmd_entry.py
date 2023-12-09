import argparse
import os
import subprocess
import sys
import ctypes
import tempfile
import winreg
from files3.ipackage import PF_DTYPE, InfoPackage
from files3._pfbool import PfBool
from files3.pyfile_shell import pyfile_shell as files


def _read_inst(_dir, _fname, _type):
    try:
        _f = files(_dir, _type)
    except Exception as err:
        print(f"Failed to create Files parser. -For {err}")
        return
    try:
        _ = _f.get(_fname)
    except Exception as err:
        print(f"Failed to load & parse target. -For {err}")
        return

    if isinstance(_, PfBool):
        print("File not exists. -For read pf-False")
        return

    # 注入txt到临时目录
    with tempfile.NamedTemporaryFile('w+t', suffix='.txt', delete=False) as f:
        f.write(f'PythonInstance: {_fname}\n' + str(_))

    # open target
    path = os.path.abspath(f.name)
    os.system(f"start {path}")


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
    f3 [fname] [ftype]
    f3 [fname] -i [dir]
    f3 [fname] [ftype] -i [dir]
    :return:
    """
    parser = argparse.ArgumentParser("Files3.CMDFilePreview")
    parser.add_argument('fname', help="Instance File's name", type=str)
    parser.add_argument('-t', '--type', help="Instance File's user-defined type. (like .XXX)", default=PF_DTYPE, type=str)
    parser.add_argument('-d', '--dir', help="Files3 entry's directory.", default="")
    try:
        args = parser.parse_args()
    except Exception as err:
        print(f"Failed to parse arguments. -For: {err}\n\n{_cmd_show_doc_}")
    # print("debug:", args)
    # get dir fname type
    _read_inst(args.dir, args.fname, args.type)


_cmd_open_doc_ = """
open files3 data by txt browser
f3open [fpath]
@example:
    f3open /datum/a.inst
    f3open /datum/a.obj
    f3open /datum/a  # is error
"""


def _cmd_open():
    parser = argparse.ArgumentParser("Files3.CMDFileOpen")
    parser.add_argument('fpath', help="Instance File's path(like a/b/c.xxx)", type=str)
    try:
        args = parser.parse_args()
    except Exception as err:
        print(f"Failed to parse arguments. -For: {err}\n\n{_cmd_open_doc_}")

    try:
        dir, fname, ftype = InfoPackage.SplitPath(args.fpath)
    except Exception as err:
        print(f"Failed to locate File. -For: {err}\n\n{_cmd_open_doc_}")

    _read_inst(dir, fname, ftype)


_cmd_assoc_doc_ = """
assoc specific file type to f3open
f3assoc [ftype]
@example:
    f3assoc .inst
    f3assoc .obj
    f3assoc .inst .obj  # is error
*Program will provide you the .exepath in anycase. If it is not effect, please assoc .exepath with your file type by hand.
"""


def _cmd_assoc():
    """
    目前确定的注册表位置:
        计算机/HKEY_CLASSES_ROOT/{EXTENSION}/OpenWithProgids
            {EXTENSION}下创建 默认value = {PROG_ID}|(REG_SZ):str
            {EXTENSION}/OpenWithProgids下创建 默认value  = {BACKEND_PROG_ID}|(REG_SZ):str  # 可选
        *计算机/HKEY_CURRENT_USER/Software/Classes/{EXTENSION}/OpenWithProgids  # same as HKEY_CLASSES_ROOT/{EXTENSION}/OpenWithProgids
        计算机/HKEY_CLASSES_ROOT/{PROG_ID}/shell/open/command
            {PROG_ID}下创建 默认value = {Description}|(REG_SZ):str
            {PROG_ID}/shell下不创建value
            {PROG_ID}/shell/open下不创建value
            {PROG_ID}/shell/open/command下创建 默认value = {abs_exepath}|(REG_SZ):str
        *计算机/HKEY_CURRENT_USER/Software/Classes/{PROG_ID}/shell/open/command  # same as HKEY_CLASSES_ROOT/{PROG_ID}/shell/open/command
        # ApplicationAssociationToasts 是一个 Windows 注册表项，它的作用是存储用户对文件关联的选择和偏好。
        计算机/HKEY_CURRENT_USER/Software/Microsoft/Windows/CurrentVersion/ApplicationAssociationToasts下创建特定value:
            {PROG_ID}_{EXTENSION} = 0|(REG_DWORD):int
        计算机/HKEY_CURRENT_USER/Software/Microsoft/Windows/CurrentVersion/Explorer/FileExts/{EXTENSION}/OpenWithProgids
            {EXTENSION}下创建 默认value = |(REG_SZ):str  # 空的
            {EXTENSION}/OpenWithProgids下创建特定value: {PROG_ID} = |(REG_NONE):?  # 空的
    至此, 完成了文件类型的注册和关联
    因此,需要的参数有:
    EXTENSION, PROG_ID, Description, abs_exepath
    :return:
    """
    parser = argparse.ArgumentParser("Files3.CMDAssoc")
    parser.add_argument('ftype', help="Instance File's custom ftype(like .xxx)", type=str)
    try:
        args = parser.parse_args()
        _try = args.ftype  # try to get ftype
    except Exception as err:
        print(f"Failed to parse arguments. -For: {err}\n\n{_cmd_assoc_doc_}")
        return

    py_exe = sys.executable
    # f3open(under Scripts)
    f3open_exe = os.path.join(os.path.dirname(py_exe), "Scripts", "f3open.exe")
    # Check
    if not os.path.exists(f3open_exe):
        print(f"Failed to locate f3open.exe. -For: {f3open_exe} is not exists")
        return

    # check extension(whether start with .)
    if not args.ftype.startswith("."):
        print(f"Failed to parse arguments. -For: {args.ftype} is not start with '.'")
        return

    Description = f"Python Instance"  # Description
    PROG_ID = f"Files3.{args.ftype[1:]}_File"
    EXTENSION = args.ftype
    abs_exepath = os.path.abspath(f3open_exe)

    # 检查admin权限
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Failed to assoc. -For: Please run this program as administrator.(Modify registry need admin permission)")
        return

    # HKEY_CLASSES_ROOT/{EXTENSION}/OpenWithProgids
    # {EXTENSION}下创建 默认value = {PROG_ID}|(REG_SZ):str
    # {EXTENSION}/OpenWithProgids下创建 默认value  = {BACKEND_PROG_ID}|(REG_SZ):str  # 可选(这里暂选空)
    with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, EXTENSION) as key:
        winreg.SetValue(key, "", winreg.REG_SZ, PROG_ID)
        with winreg.CreateKey(key, "OpenWithProgids") as subkey:
            winreg.SetValue(subkey, "", winreg.REG_SZ, "")

    # *计算机/HKEY_CURRENT_USER/Software/Classes/{EXTENSION}/OpenWithProgids  # same as HKEY_CLASSES_ROOT/{EXTENSION}/OpenWithProgids
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{EXTENSION}") as key:
        winreg.SetValue(key, "", winreg.REG_SZ, PROG_ID)
        with winreg.CreateKey(key, "OpenWithProgids") as subkey:
            winreg.SetValue(subkey, "", winreg.REG_SZ, "")

    # HKEY_CLASSES_ROOT/{PROG_ID}/shell/open/command
    # {PROG_ID}下创建 默认value = {Description}|(REG_SZ):str
    # {PROG_ID}/shell下不创建value
    # {PROG_ID}/shell/open下不创建value
    # {PROG_ID}/shell/open/command下创建 默认value = {abs_exepath}|(REG_SZ):str
    with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, PROG_ID) as key:
        winreg.SetValue(key, "", winreg.REG_SZ, Description)
        with winreg.CreateKey(key, "shell") as subkey:
            with winreg.CreateKey(subkey, "open") as subsubkey:
                with winreg.CreateKey(subsubkey, "command") as subsubsubkey:
                    winreg.SetValue(subsubsubkey, "", winreg.REG_SZ, abs_exepath)

    # *计算机/HKEY_CURRENT_USER/Software/Classes/{PROG_ID}/shell/open/command  # same as HKEY_CLASSES_ROOT/{PROG_ID}/shell/open/command
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{PROG_ID}") as key:
        winreg.SetValue(key, "", winreg.REG_SZ, Description)
        with winreg.CreateKey(key, "shell") as subkey:
            with winreg.CreateKey(subkey, "open") as subsubkey:
                with winreg.CreateKey(subsubkey, "command") as subsubsubkey:
                    winreg.SetValue(subsubsubkey, "", winreg.REG_SZ, abs_exepath)

    # ApplicationAssociationToasts 是一个 Windows 注册表项，它的作用是存储用户对文件关联的选择和偏好。
    # 计算机/HKEY_CURRENT_USER/Software/Microsoft/Windows/CurrentVersion/ApplicationAssociationToasts下创建特定value:
    # {PROG_ID}_{EXTENSION} = 0|(REG_DWORD):int
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Microsoft\\Windows\\CurrentVersion\\ApplicationAssociationToasts") as key:
        winreg.SetValueEx(key, f"{PROG_ID}_{EXTENSION}", 0, winreg.REG_DWORD, 0)

    # 计算机/HKEY_CURRENT_USER/Software/Microsoft/Windows/CurrentVersion/Explorer/FileExts/{EXTENSION}/OpenWithProgids
    # {EXTENSION}下创建 默认value = |(REG_SZ):str  # 空的
    # {EXTENSION}/OpenWithProgids下创建特定value: {PROG_ID} = |(REG_NONE):?  # 空的
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\{EXTENSION}") as key:
        winreg.SetValue(key, "", winreg.REG_SZ, "")
        with winreg.CreateKey(key, "OpenWithProgids") as subkey:
            ...

    # 创建一个 REG_NONE 类型的项
    subprocess.run(
        ['reg', 'add', f'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\{EXTENSION}\\OpenWithProgids', '/v', PROG_ID,
         '/t', 'REG_NONE', '/d', '', '/f'])

    print(f"Success to assoc {EXTENSION} to {abs_exepath}")


def _cmd_unassoc():
    """
    取消关联
    :return:
    """
    parser = argparse.ArgumentParser("Files3.CMDUnAssoc")
    parser.add_argument('ftype', help="Instance File's custom ftype(like .xxx)", type=str)
    try:
        args = parser.parse_args()
        _try = args.ftype  # try to get ftype
    except Exception as err:
        print(f"Failed to parse arguments. -For: {err}\n\n{_cmd_assoc_doc_}")
        return

    # check extension(whether start with .)
    if not args.ftype.startswith("."):
        print(f"Failed to parse arguments. -For: {args.ftype} is not start with '.'")
        return

    PROG_ID = f"Files3.{args.ftype[1:]}_File"
    EXTENSION = args.ftype

    # 检查admin权限
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Failed to unassoc. -For: Please run this program as administrator.(Modify registry need admin permission)")
        return

    # HKEY_CLASSES_ROOT/{EXTENSION}/OpenWithProgids
    # {EXTENSION}下创建 默认value = {PROG_ID}|(REG_SZ):str
    # {EXTENSION}/OpenWithProgids下创建 默认value  = {BACKEND_PROG_ID}|(REG_SZ):str  # 可选(这里暂选空)
    try:
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, EXTENSION)
    except Exception as err:
        print(f"Failed to unassoc {EXTENSION} to {PROG_ID}. -For: {err}")
        return

    # *计算机/HKEY_CURRENT_USER/Software/Classes/{EXTENSION}/OpenWithProgids  # same as HKEY_CLASSES_ROOT/{EXTENSION}/OpenWithProgids
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{EXTENSION}")
    except Exception as err:
        print(f"Failed to unassoc {EXTENSION} to {PROG_ID}. -For: {err}")
        return

    # HKEY_CLASSES_ROOT下尝试删除PROG_ID
    try:
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, PROG_ID)
    except Exception as err:
        print(f"Failed to unassoc {EXTENSION} to {PROG_ID}. -For: {err}")
        return

    # *计算机/HKEY_CURRENT_USER/Software/Classes/{PROG_ID}/shell/open/command  # same as HKEY_CLASSES_ROOT/{PROG_ID}/shell/open/command
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{PROG_ID}")
    except Exception as err:
        print(f"Failed to unassoc {EXTENSION} to {PROG_ID}. -For: {err}")
        return

    # ApplicationAssociationToasts 是一个 Windows 注册表项，它的作用是存储用户对文件关联的选择和偏好。
    # 计算机/HKEY_CURRENT_USER/Software/Microsoft/Windows/CurrentVersion/ApplicationAssociationToasts中移除特定value:
    # {PROG_ID}_{EXTENSION}
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Microsoft\\Windows\\CurrentVersion\\ApplicationAssociationToasts") as key:
            winreg.DeleteValue(key, f"{PROG_ID}_{EXTENSION}")
    except Exception as err:
        print(f"Failed to unassoc {EXTENSION} to {PROG_ID}. -For: {err}")
        return

    # 计算机/HKEY_CURRENT_USER/Software/Microsoft/Windows/CurrentVersion/Explorer/FileExts下尝试删除EXTENSION
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\{EXTENSION}")
    except Exception as err:
        print(f"Failed to unassoc {EXTENSION} to {PROG_ID}. -For: {err}")
        return

    print(f"Success to unassoc {EXTENSION} to {PROG_ID}")


if __name__ == '__main__':
    sys.argv = ['f3test', "a", '-t', ".inst"]
    _cmd_show()
