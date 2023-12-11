# -*- coding: utf-8 -*-
from __future__ import annotations

_date = "19990218"

import pandas
import numpy
import datetime
import pyecharts
from pyecharts import options
import requests
import chinese_calendar
from typing import (
    Dict
)


def Trade_Date(start, end):
    Calendar = chinese_calendar.get_workdays(
        pandas.to_datetime(start).date(), 
        pandas.to_datetime(end).date()
    )
    for date in Calendar.copy():
        if datetime.datetime.weekday(date) > 4:
            Calendar.remove(date)
    Calendar.sort()
    for date in Calendar.copy():
        if date + datetime.timedelta(days=1) in Calendar:
            Calendar.remove(date)
    return Calendar


class RiskIndex:
    def __init__(self, df: pandas.DataFrame, **kwargs):
        self.Table = df.copy().sort_index(ascending=True)

        try:
            self.Table.index = [pandas.to_datetime(x).date() for x in self.Table.index]
        except:
            raise TypeError("输入表格的index不是标准的时间格式")

        self.Table.index = [pandas.to_datetime(x).date() for x in self.Table.index]
        self.Table = self.Table[
            (self.Table.index >= pandas.to_datetime(kwargs.get("start", _date)).date())
            &
            (self.Table.index <= pandas.to_datetime(kwargs.get("end", "22180218")).date())
            ].rename_axis("日期", axis=0)
        self.date = max(self.Table.index)

    def Unified_NV(self, **kwargs):
        start = pandas.to_datetime(kwargs.get("start", _date)).date()
        table = self.Table[self.Table.index >= start]
        start_date = (table > 0).sort_index(ascending=True).idxmax()
        Initial_NV = {x: table[x][y] for x, y in start_date.to_dict().items()}
        return table / Initial_NV

    def Correlation(self, **kwargs):
        start = pandas.to_datetime(kwargs.get("start", _date)).date()
        table = self.Table[self.Table.index >= start]
        return table.pct_change().corr(method="spearman")

    def Annual_Return(self, **kwargs) -> pandas.Series:
        start = pandas.to_datetime(kwargs.get("start", _date)).date()
        table = self.Table[self.Table.index >= start]
        return numpy.exp(numpy.log(table.pct_change() + 1).mean() * 365 / 7) - 1

    def Annual_Volatility(self, **kwargs) -> pandas.Series:
        start = pandas.to_datetime(kwargs.get("start", _date)).date()
        table = self.Table[self.Table.index >= start]
        return numpy.log(table.pct_change() + 1).std() * (365 / 7) ** 0.5

    def Annual_Downward_Volatility(self, **kwargs) -> pandas.Series:
        start = pandas.to_datetime(kwargs.get("start", _date)).date()
        table = self.Table[self.Table.index >= start]
        pct_change = table.pct_change().where(table.pct_change() < 0)
        return numpy.log(pct_change + 1).std() * (365 / 7) ** 0.5

    def Max_Return(self, **kwargs):
        start = pandas.to_datetime(kwargs.get("start", _date)).date()
        table = self.Table[self.Table.index >= start]
        return table.pct_change().where(table.pct_change() > 0, 0).max()

    def Max_Loss(self, **kwargs):
        start = pandas.to_datetime(kwargs.get("start", _date)).date()
        table = self.Table[self.Table.index >= start]
        return table.pct_change().where(table.pct_change() < 0, 0).min()

    def Maximum_Drawdown(self, **kwargs) -> pandas.Series:
        start = pandas.to_datetime(kwargs.get("start", _date)).date()
        table = self.Table[self.Table.index >= start]
        return - pandas.DataFrame(
            {date: table.loc[date] / table[table.index <= date].max() - 1 for date in table.index}
        ).T.min()

    def No_New_High_Period(self, **kwargs) -> pandas.Series:
        start = pandas.to_datetime(kwargs.get("start", _date)).date()
        table = self.Table[self.Table.index >= start]
        return pandas.DataFrame(
            {date: date - table[table.index <= date].idxmax() for date in table.index}
        ).T.max()

    def Drawdown_Recover_Period(self, **kwargs) -> pandas.Series:
        start = pandas.to_datetime(kwargs.get("start", _date)).date()
        table = self.Table[self.Table.index >= start]
        delta = - pandas.DataFrame(
            {date: table.loc[date] / table[table.index <= date].max() - 1 for date in table.index}
        ).T
        return delta

    def Sharpe_Ratio(self, **kwargs) -> pandas.Series:
        start = pandas.to_datetime(kwargs.get("start", _date)).date()
        return self.Annual_Return(start=start) / self.Annual_Volatility(start=start)

    def Sortino_Ratio(self, **kwargs) -> pandas.Series:
        start = pandas.to_datetime(kwargs.get("start", _date)).date()
        return self.Annual_Return(start=start) / self.Annual_Downward_Volatility(start=start)

    def Calmar_Ratio(self, **kwargs) -> pandas.Series:
        start = pandas.to_datetime(kwargs.get("start", _date)).date()
        return self.Annual_Return(start=start) / self.Maximum_Drawdown(start=start)

    def Start_Date(self) -> pandas.Series:
        return (self.Table > 0).sort_index(ascending=True).idxmax()

    def End_Date(self) -> pandas.Series:
        return (self.Table > 0).sort_index(ascending=False).idxmax()

    def Latest_NV(self) -> pandas.Series:
        return pandas.Series({x: self.Table[x][y] for x, y in self.End_Date().to_dict().items()})

    def Return_YTM(self, delta=0):
        if self.Table.index.min() <= pandas.to_datetime("%s1231" % (self.date.year - delta)).date():
            start = max(
                self.Table[
                    self.Table.index <= pandas.to_datetime("%s1231" % (self.date.year - delta - 1)).date()
                    ].index.tolist() +
                [self.Table.index.min()]
            )
            table = self.Table[
                (self.Table.index >= start)
                &
                (self.Table.index <= pandas.to_datetime("%s1231" % (self.date.year - delta)).date())
                ]
            return numpy.exp(numpy.log(table.pct_change() + 1).mean() * 52) - 1
        else:
            return pandas.Series({x: float("nan") for x in self.Table.columns})

    def Return_Period(self, weeks=1):
        table = self.Table.tail(weeks + 1)
        return numpy.exp(numpy.log(table.pct_change() + 1).sum()) - 1

    def Success(self, **kwargs):
        start = pandas.to_datetime(kwargs.get("start", _date)).date()
        table = self.Table[self.Table.index >= start]
        return (table.pct_change() > 0).sum() / (table > 0).sum()

    def DD_Last(self, **kwargs):
        start = pandas.to_datetime(kwargs.get("start", _date)).date()
        Shorted_Table = self.Table[self.Table.index >= start]
        Shorted_Table: pandas.DataFrame = Shorted_Table / Shorted_Table.iloc[0]
        Length = pandas.Series(index=Shorted_Table.columns,
                               dtype=int)
        for name in Shorted_Table.columns:
            tt = pandas.DataFrame(index=Shorted_Table.index, columns=['时长', '回撤'])
            for date in Shorted_Table.index:
                shorted = Shorted_Table[Shorted_Table.index <= date][name]
                Day = shorted[shorted == shorted.max()].index.max()
                dd = list(shorted)[-1] / shorted.max() - 1
                tt.loc[date] = [(date - Day).days if str(Day) != 'nan' else 0, -dd if dd < 0 else 0]
            Length[name] = list(tt[tt['回撤'] == tt['回撤'].max()]['时长'])[0]
        return Length

    def Index_Table(self):
        table = pandas.DataFrame(index=self.Table.columns).rename_axis("产品名称", axis=0)
        table["最新净值"] = self.Latest_NV()
        table["净值日期"] = self.End_Date()
        table["统计起始日"] = self.Start_Date()
        table['近一周涨幅'] = self.Return_Period(1)
        table['近两周涨幅'] = self.Return_Period(2)
        table['近一月涨幅'] = self.Return_Period(4)
        table['近三月涨幅'] = self.Return_Period(13)
        table['近半年涨幅'] = self.Return_Period(26)
        table["%s年年化收益" % (self.date.year - 0)] = self.Return_YTM(0)
        table["%s年年化收益" % (self.date.year - 1)] = self.Return_YTM(1)
        table["%s年年化收益" % (self.date.year - 2)] = self.Return_YTM(2)
        table["近半年年化收益率"] = self.Annual_Return(start=self.date - datetime.timedelta(days=182))
        table["近半年年化波动率"] = self.Annual_Volatility(start=self.date - datetime.timedelta(days=182))
        table["近半年最大回撤"] = self.Maximum_Drawdown(start=self.date - datetime.timedelta(days=182))
        table["近半年夏普率"] = self.Sharpe_Ratio(start=self.date - datetime.timedelta(days=182))
        table["近半年索提诺比率"] = self.Sortino_Ratio(start=self.date - datetime.timedelta(days=182))
        table["近半年卡玛比率"] = self.Calmar_Ratio(start=self.date - datetime.timedelta(days=182))
        table["年化收益率"] = self.Annual_Return()
        table["年化波动率"] = self.Annual_Volatility()
        table["最大回撤"] = self.Maximum_Drawdown()
        table["夏普率"] = self.Sharpe_Ratio()
        table["索提诺比率"] = self.Sortino_Ratio()
        table["卡玛比率"] = self.Calmar_Ratio()
        table["最长不创新高天数"] = self.No_New_High_Period()
        table["胜率"] = self.Success()
        return table

    @staticmethod
    def __pe_line_plot(df: pandas.DataFrame, **kwargs) -> pyecharts.charts.Line:
        Line = pyecharts.charts.Line(
            init_opts=kwargs.get(
                "init_opts", options.InitOpts(
                    width="%spx" % (1920 * 0.8),
                    height="%spx" % (1080 * 0.8)
                )
            )
        )
        Line.add_xaxis(
            xaxis_data=df.index.tolist()
        )
        for col in df.columns:
            Line.add_yaxis(
                series_name=col,
                y_axis=df[col].tolist(),
                label_opts=kwargs.get("label_opts", options.LabelOpts(is_show=False)),
                linestyle_opts=kwargs.get("linestyle_opts", options.LineStyleOpts(width=2)),
            )
        Line.set_global_opts(
            yaxis_opts=kwargs.get(
                "yaxis_opts", options.AxisOpts(
                    is_scale=True, splitline_opts=options.SplitLineOpts(
                        is_show=True
                    )
                )
            ),
            xaxis_opts=kwargs.get(
                "xaxis_opts", options.AxisOpts(
                    is_scale=True, splitline_opts=options.SplitLineOpts(
                        is_show=True
                    )
                )
            ),
            legend_opts=kwargs.get(
                "legend_opts", options.LegendOpts(
                    textstyle_opts=options.TextStyleOpts(
                        font_size=20
                    ),
                    orient="vertical"
                )
            )
        )

    @property
    def nv_plot(self) -> pyecharts.charts.Line:
        return self.__pe_line_plot(self.Table)


class NV_Fetch:
    Pairs: Dict[str, Dict[str, str]]
    net_values: Dict[str, pandas.DataFrame]
    index: pandas.DataFrame

    def fetch_data(self, pairs: Dict[str, Dict[str, str]]):
        self.Pairs = pairs
        self.net_values = self._net_values()
        self.index = self._strategy_index()

    def _net_values(self) -> Dict[str, pandas.DataFrame]:
        nvs = {
            stra: [self._net_value_gs(code, name) for name, code in codes.items() if not print(stra, name)]
            for stra, codes in self.Pairs.items()
        }
        table = {stra: pandas.concat(
            [
                x.pivot_table(columns="产品名称", values="复权净值", index="净值日期") for x in nv if len(x) > 0
            ],
            axis=1
        ).sort_index() for stra, nv in nvs.items()}
        table = {y: z.loc[[x for x in Trade_Date(z.index.min(), z.index.max()) if x in z.index]] for y, z in
                 table.items()}
        return table

    @staticmethod
    def _net_value_gs(code, name) -> pandas.DataFrame:
        url = 'https://www.licai.com/api/v1/data/simu/product/deal_return_rate'
        Referer = 'https://www.licai.com/simu/product/' + code
        # for i in range(len(IA_names)):
        headers = {'Referer': Referer,
                   'Cookie': '_ga=GA1.2.268133517.1615011712; '
                             'sessionid=wicmdx17kl8m3dhtnq3ctyjk5icyy41b; '
                             'CNZZDATA1280376908=2001916158-1635562685-%7C1650816538; '
                             'Hm_lvt_c09b6af925ee0121f9617c3f09d2a088=1661094214,1661679343; '
                             'Hm_lvt_4f5f61d55230ff308da1069fd4da34dd=1661094214,1661679343; '
                             'firstEnterUrlInSession=https%3A//www.licai.com/%3Futm_source%3Dfbdsem%26utm_subsource'
                             '%3Dgeshanglicai%26bd_vid%3D8452263011033607138; '
                             'VisitorCapacity=1; '
                             'pageReferrInSession=https%3A//www.licai.com/search%3Fquery%3D%25E6%25BB%25B4%25E6%25B0'
                             '%25B4%25E6%2588%2590%25E6%25B5%25B77%25E5%258F%25B7; '
                             '_gat=1; '
                             'Hm_lpvt_c09b6af925ee0121f9617c3f09d2a088=1661682115; '
                             'Hm_lpvt_4f5f61d55230ff308da1069fd4da34dd=1661682115',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/81.0.4044.138 Safari/537.36'}
        payload_i = {"product_id": code,
                     "index_name": "NH0100.NH",
                     "is_excess_returns": "false"}
        s = requests.session()
        data = s.post(url, json=payload_i, headers=headers).json()
        try:
            result = pandas.DataFrame(data['result']['netvalue']).loc[:, ['trading_date', 'rehabilitation_nv']]
            result['rehabilitation_nv'] = result['rehabilitation_nv'].astype(float)
            result['trading_date'] = [pandas.to_datetime(x).date() for x in result["trading_date"]]
            result = result.rename(columns={'trading_date': '净值日期', 'rehabilitation_nv': '复权净值'})
            result = result.sort_values(by=['净值日期'], ascending=[False])
            result = result.set_index('净值日期')
            result['产品名称'] = [name] * len(result)
            return result
        except:
            return pandas.DataFrame(columns=["复权净值", "产品名称"])

    def _strategy_index(self) -> pandas.DataFrame:
        pct_chg = {x: numpy.log(y.pct_change() + 1) for x, y in self.net_values.items()}
        return pandas.DataFrame({x: numpy.exp(y.T.mean().T.cumsum()).fillna(1) for x, y in pct_chg.items()})


__all__ = ["RiskIndex", "NV_Fetch"]