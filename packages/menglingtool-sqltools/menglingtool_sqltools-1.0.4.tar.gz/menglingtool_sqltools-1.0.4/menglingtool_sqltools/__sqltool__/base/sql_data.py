from pandas import DataFrame
import json


def _make_func():
    def temp(data):
        if type(data) == str:
            data = data.replace("'", "\\'").strip()
        if type(data) in (tuple, list, dict):
            data = json.dumps(data, ensure_ascii=False)
        return data

    return temp


# 用于操作的集成数据库类型
class SqlData:
    def __init__(self, data: list[dict] or DataFrame):
        df = data if type(data) == DataFrame else DataFrame(data=data)
        df.rename(columns={lie: lie.strip() for lie in df.columns}, inplace=True)
        self._data = df.where(df.notnull(), None).map(_make_func())

    def __bool__(self):
        return len(self._data) > 0

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return self._data

    # 获取
    def getLies(self) -> list:
        return list(self._data.columns)

    def getDf(self) -> DataFrame:
        return self._data

    def getDts(self) -> list[dict]:
        return self._data.to_dict(orient='records')

    def getValues(self, lies: list = None) -> list[tuple]:
        if lies:
            return list(zip(*[self._data[lie].tolist() for lie in lies]))
        else:
            return self._data.to_records(index=False).tolist()

    def getAutoColMap(self, class_map: dict, **colmap) -> dict:
        dt = {}
        # 以首行数据为基准进行自动类型分配
        for lie, value in self._data.iloc[0].to_dict().items():
            if colmap.get(lie):
                dt[lie] = colmap[lie]
                continue
            if type(value) == str:
                if len(lie) < 255:
                    dt[lie] = class_map['varchar']
                else:
                    dt[lie] = class_map['text']
            elif type(value) == bool:
                dt[lie] = class_map['bool']
            elif type(value) == int:
                dt[lie] = class_map['int']
            elif type(value) == float:
                dt[lie] = class_map['float']
            else:
                dt[lie] = class_map['varchar']
        return dt
