import traceback
from pandas import DataFrame, isna


class Body:
    def __init__(self, db_func, placeholder, class_map: dict):
        self._db_func = db_func
        self._db = db_func()
        self._cursor = self._db.cursor()

        self.placeholder = placeholder
        self.class_map = class_map

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def commit(self):
        self._db.commit()

    def close(self):
        try:
            self._cursor.close()
            self._db.close()
        except:
            # traceback.print_exc()
            pass

    # 刷新连接
    def refresh(self):
        self.close()
        self._db = self._db_func()
        self._cursor = self._db.cursor()

    # 事务回滚
    def rollback(self):
        self._db.rollback()

    # 使用sql操作
    def run(self, sql):
        # print(sql)
        return self._cursor.execute(sql)

    # 获取结果
    def getResult(self, data_class='dts'):
        # 获取数据
        lies = [lc[0] for lc in self._cursor.description] if self._cursor.description else []
        result = list()
        for row in self._cursor.fetchall():
            result.append({lie: data for lie, data in zip(lies, row)})
        # 处理返回格式
        if data_class == 'ls':
            result = [list(dt.values()) for dt in result]
        elif data_class == 'df':
            result = DataFrame(data=result)
        return lies, result

    # 判断表是否存在
    def ifExist(self, table, def_schema):
        ls = table.split('.')
        if len(ls) == 1:
            schema = def_schema
        else:
            schema, table = ls
        self.run(f"SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table}' and table_schema='{schema}'")
        return len(self._cursor.fetchall()) > 0

    def in_run(self, sql, lies, *datas, if_error_one=True):
        try:
            self._cursor.executemany(sql, datas)
        except Exception as e:
            self.rollback()
            if if_error_one:
                print("\033[0;31m", '批量插入出错,执行单条插入', "\033[0m")
                for i, data in enumerate(datas):
                    try:
                        self._cursor.executemany(sql, [data])
                    except:
                        print("\033[0;32m", sql, "\033[0m")
                        traceback.print_exc()
                        print("\033[0;31m", f'具体数据出错-index{i}', "\033[0m")
                        [print("\033[0;31m", lie, ':', v, "\033[0m") for lie, v in zip(lies, data)]
                        self.rollback()
                        break
            raise e

    def getTablestr(self, table, **kwargs) -> str:
        raise TypeError('需要实现方法-getTablestr')

    def getLiestr(self, lie, **kwargs) -> str:
        raise TypeError('需要实现方法-getLiestr')

    def getLiestrs(self, lies, **kwargs) -> list:
        if type(lies) == str: lies = [lies]
        return [self.getLiestr(lie, **kwargs) for lie in lies]

