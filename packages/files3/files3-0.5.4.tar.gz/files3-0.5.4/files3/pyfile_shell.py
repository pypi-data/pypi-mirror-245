import os
import re
import inspect
from files3._ipackage import *
from files3._pfbool import *
from files3.basic_files import pyfile_basic_files
from files3.standard_files import pyfile_files

function = type(lambda: ...)


class pyfile_shell_base(object):
    info: InfoPackage = None
    backend: pyfile_files = pyfile_files()
    _ready = False

    def __init__(self, path, type=".inst", backend_type=pyfile_files):
        self.info = InfoPackage(path, type)
        self.backend = backend_type()
        assert hasattr(self.backend, "_pflevel"), "backend must be one of pyfile.?files. not " + str(self.backend)

        self._ready = True

    def retype(self, new_type: str, sources=()) -> {"find": [], "keep": []}:
        """
        修改工作目录下的现有一些文件的后缀到新的后缀
        Modify the suffix of some existing files in the working directory to a new suffix
        :param new_type:带.      contain.
        :param sources: (type1, type2...)
        :return: {"find":[], "keep":[]}
            find: 所有满足sources后缀的文件名(带原始后缀)      All file names that meet the sources suffix (with the original suffix)
            keep: 由于名称重复而未能成功retype的文件名(带原始后缀)      Failed to retype file successfully due to duplicate name(with the original suffix)
        """
        find, keep = [], []
        assert '.' == new_type[0], "type must contain '.'"
        # assert self.backend._pflevel >= 1, "For using this function, pyfile_files is needy or more advanced pyfile_files. (Basic_files is not accept.)"
        for fname in os.path.listdir(self.info.path):
            _path = os.path.join(self.info.path, fname)
            if os.path.isfile(_path):
                _base, _type = os.path.splitext(fname)
                if _type in sources:
                    if os.path.exists(os.path.join(self.info.path, _base + new_type)):
                        keep += [fname]
                    else:
                        find += [fname]
        return {"find": find, "keep": keep}


class pyfile_shell_basic_magic(object):  # assert _pflevel == 0
    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        if self.has(key):
            self.modify(key, value)
        else:
            self.new(key, value)

    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        if self._ready == True:
            self.__setitem__(key, value)
        else:
            super(pyfile_shell_basic_magic, self).__setattr__(key, value)

    def __delitem__(self, key):
        self.delete(key)

    def __delattr__(self, item):
        self.delete(item)

    def __contains__(self, item):
        return self.has(item)


class pyfile_shell_magic(object):  # assert _pflevel >= 1
    def _shell_magic_filter_(self, item, type=True, listes=[]):
        """
        标准筛选支持:（sysfunc .protected.）
        1.str
        2.... or slice[:](仅限全选)
        3.re.Pattern 对每个key(type == False)或是fname(type == True)
        4.func(name, type)->bool 将返回True的结果对应的item选中
        5.[] or ()  各个条件间相并
        :param item:
        :param type: whether suffix or not. If False, only select self.info.type
        :param listes: 递归用，用户勿传     Recursive use, users do not pass
        :return: [] of '$name + $type'
        """
        _end = self.info.type if type else ""
        # 第一轮筛选 -- 简单筛选
        if isinstance(item, slice) or item is ...:
            return self.list(with_type=type)
        elif isinstance(item, str):
            return [item + _end]

        _return = []
        # 第二轮筛选 -- advanced筛选
        if not listes:
            listes = os.listdir()
        if isinstance(item, function):
            for fname in listes:
                _key, _type = os.path.splitext(fname)
                if type or self.info.type == _type:
                    try:
                        _value = item(_key)
                    except Exception as err:
                        print(f"Bad filter function: {item}. Cause error: {err}\n\nPlease check your function(fname)->bool and it's code.")
                    if bool(_value) == True:
                        _return += [(_key + _end) if not type else fname]

        elif isinstance(item, re.Pattern):
            for fname in listes:
                _key, _type = os.path.splitext(fname)
                if type or self.info.type == _type:
                    if item.match(_key if not type else fname):
                        _return += [(_key + _end) if not type else fname]
        elif isinstance(item, (tuple, list)):
            for _item in item:
                _return += self._shell_magic_filter_(_item, type, listes)
        else:
            raise Exception("Unkown item - " + str(item))
        return list(set(_return))

    def __getitem__(self, item):
        _return = []
        for key in self._shell_magic_filter_(item, type=False):
            _return += [self.get(key)]
        return PfFalse if not _return else (_return[0] if len(_return) == 1 else _return)

    def __setitem__(self, key, value):
        for key in self._shell_magic_filter_(key, type=False):
            self.set(key, value)

    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        if self._ready == True:
            self.__setitem__(key, value)
        else:
            super(pyfile_shell_magic, self).__setattr__(key, value)

    def __delitem__(self, key):
        for key in self._shell_magic_filter_(key, type=False):
            self.delete(key)

    def __delattr__(self, item):
        self.delete(item)

    def __len__(self):
        return len(self.list())

    def __contains__(self, item):
        _return = True
        for key in self._shell_magic_filter_(item, type=False):
            _return *= self.has(item)
        return bool(_return)

    def __iter__(self):
        return iter(self.list())


class pyfile_shell_basic(pyfile_shell_base, pyfile_shell_basic_magic):
    def __init__(self, path="", type=".inst"):
        pyfile_shell_base.__init__(self, path, type, pyfile_basic_files)

    def has(self, key: str) -> PfBool:
        """
        增删改查之番外-事先确认。成功返回PfTrue，如果目标文件不存在，则返回PfFalse
        Has a pyfile file exists. Returns True successfully, or False if the target file doesnot exists

        :param info:     InfoPackage inst
        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        """
        return self.backend.has(self.info, key)

    def get(self, key: str) -> object:
        """
        增删改查之'查'。成功返回读取到的pyobject，如果目标文件不存在，则返回PfFalse
        Find data files. The read pyobject is returned successfully. If the target file does not exist, false is returned

        :param info:     InfoPackage inst
        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        """
        return self.backend.get(self.info, key)

    def new(self, key: str, pyobject: object) -> PfBool:
        """
        增删改查之'增'。成功返回PfTrue，如果目标文件已存在，则返回PfFalse
        Add a new pyfile file. Returns True successfully, or False if the target file already exists

        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        :param pyobject: python对象   python object
        """
        return self.backend.new(self.info, key, pyobject)

    def delete(self, key: str) -> PfBool:
        """
        增删改查之'删'。成功或目标文件不存在则返回PfTrue，如果目标文件存在而无法删除，则返回PfFalse
        Delete pyfile file. Returns True if the target file is successful or does not exist. Returns False if the target file exists and cannot be deleted

        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        """
        return self.backend.delete(self.info, key)

    def modify(self, key: str, pyobject: object) -> PfBool:
        """
        增删改查之'改'。成功返回PfTrue，如果目标文件不存在，则返回PfFalse
        Modify existing data files. Returns True successfully, or False if the target file does not exist

        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        :param pyobject: python对象   python object
        """
        return self.backend.modify(self.info, key, pyobject)


class pyfile_shell(pyfile_shell_base, pyfile_shell_magic):
    def __init__(self, path="", type=".inst"):
        pyfile_shell_base.__init__(self, path, type, pyfile_files)

    def has(self, key: str) -> PfBool:
        """
        增删改查之番外-事先确认。成功返回PfTrue，如果目标文件不存在，则返回PfFalse
        Has a pyfile file exists. Returns True successfully, or False if the target file doesnot exists

        :param info:     InfoPackage inst
        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        """
        return self.backend.has(self.info, key)

    def set(self, key: str, pyobject: object) -> PfBool:
        """
        存储python对象到目标文件夹下。成功返回PfTrue，如果目标文件被锁定或占用，则返回PfFalse
        Storing Python objects to pyfile under specific path in InfoPackage. Returns True successfully. If the target file is locked or occupied, returns False

        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        :param pyobject: python对象   python object
        """
        return self.backend.set(self.info, key, pyobject)

    def get(self, key: str) -> object:
        """
        增删改查之'查'。成功返回读取到的pyobject，如果目标文件不存在，则返回PfFalse
        Find data files. The read pyobject is returned successfully. If the target file does not exist, false is returned

        :param info:     InfoPackage inst
        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        """
        return self.backend.get(self.info, key)

    def delete(self, key: str) -> PfBool:
        """
        增删改查之'删'。成功或目标文件不存在则返回PfTrue，如果目标文件存在而无法删除，则返回PfFalse
        Delete pyfile file. Returns True if the target file is successful or does not exist. Returns False if the target file exists and cannot be deleted

        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        """
        return self.backend.delete(self.info, key)

    def list(self, with_type=False) -> list:
        """
        列举目标文件夹下所有info.type类型的文件的key。返回一个列表结果
        List all info of keys (In the target folder The key of a file of type). Returns a list result

        :param with_type:     whether with suffix or not
        """
        return self.backend.list(self.info, with_type)
