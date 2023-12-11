import pandas
import datetime


class read_GZB:
    __Substitute = pandas.DataFrame()

    def __init__(self, filename, Code):
        self.Code = Code
        self.Filename = filename
        self.Table = pandas.read_excel(self.Filename, engine="xlrd")
        self.Table = self._Extract()

    def _Extract(self):
        for ind in range(len(self.Table.index)):
            if "科目代码" in self.Table.iloc[ind].tolist():
                break
        for col in range(len(self.Table.columns)):
            if "科目代码" == self.Table.iloc[ind, col]:
                break
        result = pandas.read_excel(self.Filename, header=ind + 1, index_col=col, thousands=",")
        result.index = [str(x) for x in result.index]
        result: pandas.DataFrame = result.loc[[x for x in result.index if not (
                x == "科目代码" or x.__contains__("制  表：") or x.__contains__("打  印："))]]
        result.index = result.index.astype(str)
        result = result.loc[[x for x in result.index if x != "nan"]]
        result["科目名称"] = [self.__Substitute["新名称"][x] if x in self.__Substitute.index else x for x in result["科目名称"]]
        result["科目名称"] = ["".join(x.split(" ")) if isinstance(x, str) else x for x in result["科目名称"]]
        result["数量"] = result["数量"].astype(float) if len(result) else result["数量"]
        result["成本-本币"] = result["成本-本币" if "成本-本币" in result.columns else "成本"].astype(float)
        result["市值-本币"] = result["市值-本币" if "市值-本币" in result.columns else "市值"].astype(float)
        result = result.fillna("").replace({" ": ""})
        return result

    @staticmethod
    def _Change_Name(name):
        part = name[-4:]
        ind: int
        for ind in range(len(part)):
            if 48 <= ord(part[ind]) < 58 or 65 <= ord(part[ind]) < 91:
                break
        if len(part) == ind + 1 and not (48 <= ord(part[ind]) < 58 or 65 <= ord(part[ind]) < 91):
            ind += 1
        output: str = name[:-4] + part[:ind]
        if output.find("(") > 0:
            output = output[: output.find("(")]
        if output.find("（") > 0:
            output = output[: output.find("（")]
        return output

    def Get_Funds(self):
        Funds: pandas.DataFrame = self.Table[self.Table["停牌信息"] != ""].replace({"": float("nan")})
        Funds['科目名称'] = [self._Change_Name(x) for x in Funds["科目名称"]]
        Funds["数量"] = Funds["数量"].astype(float)
        Funds["成本-本币"] = Funds["成本-本币" if "成本-本币" in Funds.columns else "成本"].astype(float)
        Funds["市值-本币"] = Funds["市值-本币" if "市值-本币" in Funds.columns else "市值"].astype(float)
        result = pandas.DataFrame(index=list(set(Funds["科目名称"])))
        result["数量"] = Funds.groupby("科目名称")["数量"].sum()
        result["规模"] = Funds.groupby("科目名称")["市值-本币"].sum()
        result["成本"] = Funds.groupby("科目名称")["成本-本币"].sum()
        result["单位成本"] = result["成本"] / result["数量"]
        return result

    def Get_Date(self):
        """
        
        Returns
        -------
        datetime.date
            选定估值表的日期

        """
        name = self.Filename.split("/")[-1]
        name = name.split(".")[0]
        date = "".join([x for x in name[-12:] if 48 <= ord(x) < 58])
        if not date:
            date = "".join([x for x in name.replace(self.Code, "")[:12] if 48 <= ord(x) < 58])
        return pandas.to_datetime(date[:8]).date()

    def Get_Dividend(self):
        # result = self.Table.loc[[x for x in self.Table.index if len(x) > 10 and
        #                         (x[:10] == "1203.03.02" or str(self.Table.loc[x, "科目名称"]).__contains__("红利"))]]
        """
        获取当日分红品种及分红金额

        Returns
        -------
        pandas.Series
            分红品种与金额
        """
        Funds = self.Get_Funds()
        result = self.Table.loc[[x for x in self.Table.index if len(x) > 10 and x[:4] == "1203"]]
        result['科目名称'] = [self._Change_Name(x) for x in result["科目名称"]]
        result = result.loc[[x for x in result.index if result.loc[x, "科目名称"] in Funds.index.values]]
        result["科目名称"] = [self._Change_Name(x) for x in result["科目名称"]]
        return result.groupby("科目名称")["市值-本币"].sum()
