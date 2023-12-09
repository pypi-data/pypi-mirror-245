# from pymssql import connect as sst_connect
from .__sqltool__.action import Action, SqlData
from .tools import decrypt
from .__sqltool__.alter import Alter
import pyodbc


class Sqlserver(Action, Alter):
    def __init__(self, dbname, user, pwd,
                 host='127.0.0.1', port: int = 1433,
                 charset='UTF8',  # cp936
                 ifencryp=True):
        self._dbname = dbname
        self._user = user
        self._pwd = pwd
        self._host = host
        self._port = port
        self._charset = charset
        self._ifencryp = ifencryp
        class_map = {'varchar': 'nvarchar(255)',
                     'text': 'ntext',
                     'bool': 'bit',
                     'int': 'int',
                     'float': 'float'
                     }
        super().__init__(self._db_func, placeholder='?', class_map=class_map)

    def _db_func(self):
        db = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self._host};DATABASE={self._dbname};UID={self._user};PWD={decrypt(self._user, self._pwd) if self._ifencryp else self._pwd}')  # DRIVER={SQL Server};
        # db = sst_connect(host=self.host, port=self.port,
        #                      user=self.user, password=self.passwd,
        #                      database=self.dbname, charset=self.charset)
        return db

    def getTablestr(self, table, **kwargs):
        if '.' in table:
            t1, t2 = table.split('.')
            return f'[{t1}].[{t2}]'
        else:
            return f'[{table}]'

    def getLiestr(self, lie, **kwargs):
        if lie in {'*', '1', 'count(1)', 'top 1 1'}:
            return lie
        else:
            return f"[{lie}]"

    def deleteTable(self, table):
        # DROP TABLE table_name
        sql = '''
            If Exists (select * from sysobjects where id = object_id('{table}') and OBJECTPROPERTY(id, 'IsUserTable') = 1)
                DROP TABLE {table} 
        '''.format(table=self.getTablestr(table))
        return self.run(sql)

    # 判断表是否存在
    def ifExist(self, table):
        return Action.ifExist(self, table, def_schema='dbo')
