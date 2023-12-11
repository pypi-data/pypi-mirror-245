# -*- coding: utf-8 -*-
import pandas


class read_excel:
    def __init__(self, file):
        self.filename = file
        self.table = self.read_table()

    def read_table(self) -> pandas.DataFrame:
        table = pandas.read_excel(self.filename)
        i, j = 0, 0
        while "科目代码" not in table.iloc[i].tolist():
            i += 1
        while "科目代码" != table.iloc[i, j]:
            j += 1
        return pandas.read_excel(self.filename, header=i + 1, index_col=j, na_filter="")
