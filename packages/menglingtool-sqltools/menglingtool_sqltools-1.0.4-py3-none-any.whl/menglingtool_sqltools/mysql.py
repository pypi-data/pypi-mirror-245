from pymysql import connect as myt_connect
from .__sqltool__.action import Action, SqlData
from .tools import decrypt
from .__sqltool__.alter import Alter


class Mysql(Action, Alter):
    def __init__(self, dbname, user, pwd,
                 host='127.0.0.1', port: int = 3306,
                 charset='utf8mb4',
                 ifencryp=True):
        self._dbname = dbname
        self._user = user
        self._pwd = pwd
        self._host = host
        self._port = port
        self._charset = charset
        self._ifencryp = ifencryp
        class_map = {'varchar': 'varchar(255)',
                     'text': 'text',
                     'bool': 'blob',
                     'int': 'int',
                     'float': 'float'
                     }
        super().__init__(self._db_func, placeholder='%s', class_map=class_map)

    def _db_func(self):
        db = myt_connect(host=self._host, port=self._port,
                         user=self._user, passwd=decrypt(self._user, self._pwd) if self._ifencryp else self._pwd,
                         database=self._dbname, charset=self._charset)
        return db

    def run(self, sql):
        # 设置重连
        self._db.ping(reconnect=True)
        return Action.run(self, sql)

    def in_run(self, sql, *datas, if_error_one=True):
        # 设置重连
        self._db.ping(reconnect=True)
        return Action.in_run(self, sql, *datas, if_error_one=if_error_one)

    def commit(self):
        # 设置重连
        self._db.ping(reconnect=True)
        return Action.commit(self)

    def getTablestr(self, table, **kwargs):
        return '`%s`' % table

    def getLiestr(self, lie, **kwargs):
        if lie in {'*', '1', 'count(1)'}:
            return lie
        else:
            return f"`{lie.replace('%', '%%')}`"

    def ifExist(self, table):
        b = self.run(f'show tables like "{table}"')
        return b and len(self._cursor.fetchall()) > 0
