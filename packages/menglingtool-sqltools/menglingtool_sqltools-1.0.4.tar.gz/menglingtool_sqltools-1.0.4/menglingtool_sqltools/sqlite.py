import os
import sqlite3
from .__sqltool__.action import Action, SqlData
from .tools import decrypt
from .__sqltool__.alter import Alter


class Sqlite(Action, Alter):
    def __init__(self, dbfilepath, if_new=True, ifencryp=False):
        self._dbfilepath = dbfilepath
        self._if_new = if_new
        self._ifencryp = ifencryp
        class_map = {'varchar': 'text',
                     'text': 'text',
                     'bool': 'integer',
                     'int': 'integer',
                     'float': 'real'
                     }
        super().__init__(self._db_func, placeholder='?', class_map=class_map)

    # 打开数据库连接
    def _db_func(self):
        if not self._if_new and not os.path.exists(self._dbfilepath):
            raise ValueError(f'没有 {self._dbfilepath} 文件!')
        db = sqlite3.connect(self._dbfilepath)
        return db

    def getTablestr(self, table, **kwargs):
        if '.' in table:
            t1, t2 = table.split('.')
            return f'"{t1}"."{t2}"'
        else:
            return f'"{table}"'

    def getLiestr(self, lie, **kwargs):
        if lie in {'*', '1', 'count(1)'}:
            return lie
        else:
            return f'"{lie}"'

    # 判断表是否存在
    def ifExist(self, table):
        b = self.run(f"SELECT 1 FROM sqlite_master WHERE type='table' AND name='{table}'")
        return b and len(self._cursor.fetchall()) > 0
