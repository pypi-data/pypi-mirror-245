from psycopg2 import connect as pgt_connect
from .__sqltool__.action import Action, SqlData
from .tools import decrypt
from .__sqltool__.alter import Alter


class Pgsql(Action, Alter):
    def __init__(self, dbname, user, pwd,
                 host='127.0.0.1', port: int = 5432,
                 charset='UTF8',
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
                     'bool': 'bool',
                     'int': 'int8',
                     'float': 'float8'
                     }
        super().__init__(self._db_func, placeholder='%s', class_map=class_map)

    def _db_func(self):
        db = pgt_connect(host=self._host, port=self._port,
                         user=self._user, password=decrypt(self._user, self._pwd) if self._ifencryp else self._pwd,
                         database=self._dbname)
        db.set_client_encoding(self._charset)
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

    # 创建物化视图
    def createMaterializedView(self, view_name, run_sql):
        self.run(f'create materialized view "{view_name}" as {run_sql}')

    # 创建唯一约束
    pass

    # 刷新物化视图
    def refreshMaterializedView(self, view_name, if_lock=True):
        # 使用CONCURRENTLY的物化索引必须具有 unique 约束,否则会报错
        self.run(f'REFRESH MATERIALIZED VIEW {"" if if_lock else "CONCURRENTLY"} "{view_name}"')

    # 删除物化视图
    def deleteMaterializedView(self, view_name):
        self.run(f'drop materialized view if exists {view_name}')

    def createTable(self, table, lies: list,
                    colmap: dict = None,
                    key: list or str = None,
                    hz: str = None,
                    parentable_valuetxt: tuple = None):
        if parentable_valuetxt:
            parent_table, valuetxt = parentable_valuetxt
            return self.createTable_child(table, parent_table, valuetxt)
        else:
            return Action.createTable(self, table, lies, hz=hz, colmap=colmap, key=key)

    def createTable_copy(self, table, copy_table):
        # 子表与父表结构保持一致
        sql = f'CREATE TABLE If Not Exists {self.getTablestr(table)} (LIKE {self.getTablestr(copy_table)} including all)'
        return self.run(sql)

    def createTable_parent(self, table, lies: list, key_lie: str, columnclassdict: dict = None, colmap: dict = None,
                           key=None, map_class='list', **kwargs):  # range
        # 分区父表
        return Action.createTable(self, table, lies, hz=f"PARTITION BY {map_class} (\"{key_lie}\")",
                                  colmap=colmap, key=key, **kwargs)

    def createTable_child(self, table, parent_table, valuetxt):
        # 分区子表
        sql = f'CREATE TABLE If Not Exists {self.getTablestr(table)} PARTITION of {self.getTablestr(parent_table)} FOR values {valuetxt}'  # in ('123') from ('123') to ('125')
        return self.run(sql)

    # 解除子表分区关系
    def detachPartition(self, parentable, childtable):
        sql = f"ALTER TABLE {self.getTablestr(parentable)} detach PARTITION {self.getTablestr(childtable)}"
        return self.run(sql)

    # 绑定子表分区关系
    def attachPartition(self, parentable, childtable, valuetxt):
        sql = f"ALTER TABLE {self.getTablestr(parentable)} attach PARTITION {self.getTablestr(childtable)} FOR VALUES {valuetxt}"
        return self.run(sql)

    # 判断表是否存在
    def ifExist(self, table):
        return Action.ifExist(self, table, def_schema='public')
