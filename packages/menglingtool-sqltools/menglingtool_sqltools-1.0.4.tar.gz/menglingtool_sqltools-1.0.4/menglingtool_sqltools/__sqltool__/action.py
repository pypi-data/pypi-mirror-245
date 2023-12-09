from .base.body import Body, traceback
from .base.sql_data import SqlData


class Action(Body):
    def createTable(self, table, lies: list,
                    colmap: dict = None,
                    key: list or str = None,
                    hz: str = None):
        colmap = colmap if colmap else {}
        assert lies, "数量有误！"
        if key:
            if type(key) == str:
                key = [key]
                key = f" ,PRIMARY KEY({','.join(self.getLiestrs(key))})"
        else:
            key = ''
        # 默认类型为短字符串类型
        liestr = ",\n".join(f'{self.getLiestr(lie)} {colmap.get(lie, self.class_map["varchar"])}' for lie in lies)
        sql = '''
            Create Table If Not Exists {table}
            ({lies} {key}){hz}
        '''.format(table=self.getTablestr(table), lies=liestr, key=key, hz=hz if hz else '')
        return self.run(sql)

    # 删除表
    def deleteTable(self, table):
        # DROP TABLE table_name
        sql = '''DROP TABLE IF EXISTS {table} 
        '''.format(table=self.getTablestr(table))
        return self.run(sql)

    def _auto_add_lie(self, lies, table, dataclass, other):
        have_lies = self.select('*', table, where='1=0', ifgetlies=True)[0]
        not_liest = set(lies) - set(have_lies)
        for lie in self.getLiestrs(not_liest):
            self.run(f'ALTER TABLE {self.getTablestr(table)} ADD {lie} {other};')
            # return self.run(';'.join(sqls))

    # 插入
    def insert(self, table: str, sql_data: SqlData,
               lies=None,
               in_hz='',
               auto_lie_class=None,
               if_error_one=True):
        assert sql_data, "数量不能为0！"
        lies = [lie.strip() for lie in lies] if lies else sql_data.getLies()
        datas = sql_data.getValues(lies)
        # 插入语句
        sql = '''INSERT INTO {table}({liestr})
                VALUES ({cstr}) {in_hz}
        '''.format(table=self.getTablestr(table), liestr=','.join(self.getLiestrs(lies)),
                   cstr=','.join([self.placeholder] * len(lies)), in_hz=in_hz)
        if auto_lie_class:
            try:
                return self._cursor.executemany(sql, datas)
            except Exception as e:
                self._auto_add_lie(lies, table, auto_lie_class, other='')
                return self.in_run(sql, lies, *datas, if_error_one=if_error_one)
        else:
            return self.in_run(sql, lies, *datas, if_error_one=if_error_one)

    def create_insert(self, table, dts: list,
                      colmap: dict = None,
                      key: list or str = None,
                      hz: str = None,
                      in_hz='',
                      auto_lie_class=None):
        colmap = colmap if colmap else {}
        sdata = SqlData(dts)
        self.createTable(table, sdata.getLies(), sdata.getAutoColMap(self.class_map, **colmap), key=key, hz=hz)
        self.insert(table, sdata, in_hz=in_hz, auto_lie_class=auto_lie_class)

    # 修改
    def update(self, table, dt: dict, where: str, **kwargs):
        assert dt, "数量有误！"
        sdata = SqlData([dt])
        lies = sdata.getLies()
        setv = ','.join([f"{lie}={self.placeholder}" for lie in self.getLiestrs(lies)])
        sql = '''UPDATE {table}
                SET {setv}
                WHERE {where}
        '''.format(table=self.getTablestr(table, **kwargs), setv=setv, where=where)
        # print(sql)
        return self.in_run(sql, lies, *sdata.getValues(lies), **kwargs)

    # 删除
    def delete(self, table, where: str):
        # 表名
        sql = '''DELETE FROM {table}
            WHERE {where}
        '''.format(table=self.getTablestr(table), where=where)
        return self.run(sql)

    def select(self, lies, table, where=None, other='',
               data_class='dts',
               ifgetlies=False,
               ifget_one_lie=False,
               if_original_table=False,
               if_original_lies=False) -> list or (list, list):
        assert not (if_original_lies and type(lies) == str), '开启原始列时,输入列必须为列表格式!'
        sql = '''select {lies}
                   from {table}
                   where {where}
                   {other}
           '''.format(lies=','.join(lies if if_original_lies else self.getLiestrs(lies)),
                      table=table if if_original_table else self.getTablestr(table),
                      where=where if where else '1=1',
                      other=other)
        self.run(sql)
        # 获取数据
        lies, result = self.getResult(data_class='ls' if ifget_one_lie else data_class)
        if ifget_one_lie:
            result = [d[0] for d in result]
        if ifgetlies:
            return lies, result
        else:
            return result

    # 判断是否可以查询到
    def ifGet(self, table, where=None, if_error=True):
        try:
            if len(self.select('1', table, where=where, data_class='ls', other='limit 1')) > 0:
                return True
            else:
                return False
        except:
            if if_error:
                traceback.print_exc()
            return False

    # 获取数量
    def getNum(self, table, where=None):
        num = self.select('count(1)', table, where=where, data_class='ls')[0][0]
        return num
