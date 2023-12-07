# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
import numpy as np
import pandas as pd
import xlwings

from WindPy import w
w.start()  # 默认命令超时时间为120秒，如需设置超时时间可以加入waitTime参数，例如waitTime=60,即设置命令超时时间为60秒
w.isconnected()  # 判断WindPy是否已经登录成功

import warnings
warnings.filterwarnings("ignore")


def get_overseas_date(start_date, end_date):
    calendar_df = HBDB().read_cal(start_date, end_date)
    calendar_df = calendar_df.rename(columns={'jyrq': 'CALENDAR_DATE', 'sfjj': 'IS_OPEN', 'sfzm': 'IS_WEEK_END', 'sfym': 'IS_MONTH_END'})
    calendar_df['CALENDAR_DATE'] = calendar_df['CALENDAR_DATE'].astype(str)
    calendar_df = calendar_df.sort_values('CALENDAR_DATE')
    calendar_df['IS_OPEN'] = calendar_df['IS_OPEN'].astype(int).replace({0: 1, 1: 0})
    calendar_df['YEAR_MONTH'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[:6])
    calendar_df['MONTH'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:6])
    calendar_df['MONTH_DAY'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:])
    calendar_df = calendar_df[(calendar_df['CALENDAR_DATE'] >= start_date) & (calendar_df['CALENDAR_DATE'] <= end_date)]

    # start_date_hyphen = datetime.strptime(start_date, '%Y%m%d').strftime('%Y-%m-%d')
    # end_date_hyphen = datetime.strptime(end_date, '%Y%m%d').strftime('%Y-%m-%d')
    # trade_df = w.wsd("SPX.GI", "close", start_date_hyphen, end_date_hyphen, usedf=True)[1].reset_index()
    # trade_df['index'] = trade_df['index'].apply(lambda x: x.strftime('%Y%m%d'))
    # trade_df = trade_df[['index']].rename(columns={'index': 'TRADE_DATE'})
    # trade_df.to_hdf('{0}trade_df.hdf'.format(data_path), key='table', mode='w')
    trade_df = pd.read_hdf('{0}trade_df.hdf'.format(data_path), key='table')
    return calendar_df, trade_df


def df_add_info(df, info):
    df = df.T
    df.index.name = 'INDEX'
    df = df.reset_index()
    df['TYPE'] = info
    df = df.set_index(['TYPE', 'INDEX']).T
    return df


def cal_drawdown(ser):
    df = pd.DataFrame(ser)
    col = df.columns[0]
    print(col)
    df.columns = ['NAV']
    df = df.sort_index()
    df['IDX'] = range(len(df))
    df['HIGHEST'] = df['NAV'].cummax()
    df['DRAWDOWN'] = (df['NAV'] - df['HIGHEST']) / df['HIGHEST']
    return df['DRAWDOWN']


def cal_annual_ret(idxs, col, daily_df, q):
    part_df = daily_df.iloc[list(map(int, idxs))].copy(deep=True)
    annual_ret = (part_df[col].iloc[-1] / part_df[col].iloc[0]) ** (float(q) / len(part_df)) - 1 if part_df[col].iloc[0] != 0 else np.nan
    return annual_ret


def cal_annual_vol(idxs, col, daily_df, q):
    part_df = daily_df.iloc[list(map(int, idxs))].copy(deep=True)
    annual_vol = np.std(part_df[col].pct_change().dropna(), ddof=1) * np.sqrt(q)
    return annual_vol


def cal_max_drawdown(idxs, col, daily_df, q):
    part_df = daily_df.iloc[list(map(int, idxs))].copy(deep=True)
    part_df['HIGHEST'] = part_df[col].cummax()
    part_df['DRAWDOWN'] = (part_df[col] - part_df['HIGHEST']) / part_df['HIGHEST']
    max_drawdown = min(part_df['DRAWDOWN'])
    return max_drawdown


class OverseasOverview:
    def __init__(self, start_date, end_date, data_path):
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_hyphen = datetime.strptime(self.start_date, '%Y%m%d').strftime('%Y-%m-%d')
        self.end_date_hyphen = datetime.strptime(self.end_date, '%Y%m%d').strftime('%Y-%m-%d')
        self.data_path = data_path

        self.index_list = ['881001.WI', 'HSI.HI', 'HSTECH.HI',
                           'SPX Index', 'INDU Index', 'CCMP Index',
                           'SXXP Index', 'SX5E Index', 'UKX Index', 'CAC Index', 'DAX Index',
                           'TPX Index', 'NKY Index', 'KOSPI Index', 'VN30 Index', 'SENSEX Index',
                           'MXEF Index', 'M1WO Index']
        self.index_name_dict = {'881001.WI': '万得全A指数', 'HSI.HI': '恒生指数', 'HSTECH.HI': '恒生科技指数',
                                'SPX Index': '标普500指数', 'INDU Index': '道琼斯工业平均指数', 'CCMP Index': '纳斯达克综合指数',
                                'SXXP Index': '欧洲斯托克600指数', 'SX5E Index': '欧洲斯托克50指数', 'UKX Index': '英国富时100指数', 'CAC Index': '法国CAC40指数', 'DAX Index': '德国DAX30指数',
                                'TPX Index': '日本东证指数', 'NKY Index': '日经225指数', 'KOSPI Index': '韩国综合指数', 'VN30 Index': '越南VN30指数', 'SENSEX Index': '印度孟买30指数',
                                'MXEF Index': 'MSCI新兴市场指数', 'M1WO Index': 'MSCI全球指数'}

        self.calendar_df, self.trade_df = get_overseas_date(self.start_date, self.end_date)
        self.date_1w = self.trade_df[self.trade_df['TRADE_DATE'] < self.end_date]['TRADE_DATE'].iloc[-5]
        self.date_1m = self.trade_df[self.trade_df['TRADE_DATE'] < self.end_date]['TRADE_DATE'].iloc[-20 * 1]
        self.date_3m = self.trade_df[self.trade_df['TRADE_DATE'] < self.end_date]['TRADE_DATE'].iloc[-20 * 3]
        self.date_6m = self.trade_df[self.trade_df['TRADE_DATE'] < self.end_date]['TRADE_DATE'].iloc[-20 * 6]
        self.date_1y = self.trade_df[self.trade_df['TRADE_DATE'] < self.end_date]['TRADE_DATE'].iloc[-250]
        self.date_2023 = self.trade_df[self.trade_df['TRADE_DATE'] < '20230101']['TRADE_DATE'].iloc[-1]
        self.date_2022 = self.trade_df[self.trade_df['TRADE_DATE'] < '20220101']['TRADE_DATE'].iloc[-1]
        self.date_2021 = self.trade_df[self.trade_df['TRADE_DATE'] < '20210101']['TRADE_DATE'].iloc[-1]
        self.date_2015 = self.trade_df[self.trade_df['TRADE_DATE'] < '20150101']['TRADE_DATE'].iloc[-1]

        self.load()

    def load(self):
        # self.overseas_index_daily_k = HBDB().get_overseas_index_daily_k_given_indexs(self.index_list)
        # self.overseas_index_daily_k.to_hdf('{0}overseas_index_daily_k.hdf'.format(self.data_path), key='table', mode='w')
        self.overseas_index_daily_k = pd.read_hdf('{0}overseas_index_daily_k.hdf'.format(self.data_path), key='table')

        # self.overseas_index_finance = HBDB().get_overseas_index_finance_given_indexs(self.index_list)
        # self.overseas_index_finance.to_hdf('{0}overseas_index_finance.hdf'.format(self.data_path), key='table', mode='w')
        self.overseas_index_finance = pd.read_hdf('{0}overseas_index_finance.hdf'.format(self.data_path), key='table')

        # self.overseas_index_best = HBDB().get_overseas_index_best_given_indexs(self.index_list)
        # self.overseas_index_best.to_hdf('{0}overseas_index_best.hdf'.format(self.data_path), key='table', mode='w')
        self.overseas_index_best = pd.read_hdf('{0}overseas_index_best.hdf'.format(self.data_path), key='table')

    def index(self):
        index_w = w.wsd(",".join(self.index_list[:3]), "close", self.start_date_hyphen, self.end_date_hyphen, usedf=True)[1].reset_index()
        index_w['index'] = index_w['index'].apply(lambda x: x.strftime('%Y%m%d'))
        index_w = index_w.set_index('index').sort_index()
        index = self.overseas_index_daily_k[['bzzsdm', 'jyrq', 'px_last']]
        index['jyrq'] = index['jyrq'].astype(str)
        index = index.pivot(index='jyrq', columns='bzzsdm', values='px_last').sort_index()
        index = pd.concat([index_w, index], axis=1)
        index = index[index.index.isin(self.trade_df['TRADE_DATE'].unique().tolist())].sort_index().fillna(method='ffill')
        index = index[self.index_list].rename(columns=self.index_name_dict)
        index = index[(index.index >= self.start_date) & (index.index <= self.end_date)]

        close = index.copy(deep=True)
        close = df_add_info(close, '收盘点位')

        close_nav = index.dropna()
        close_nav = close_nav / close_nav.iloc[0]
        close_nav = df_add_info(close_nav, '收盘点位（最大同期归一化）')

        close_ytd = index[index.index >= '20221230']
        close_ytd = close_ytd / close_ytd.iloc[0]
        close_ytd = df_add_info(close_ytd, '收盘点位（今年以来归一化）')

        ret_1w = index.pct_change(5)
        ret_1w = df_add_info(ret_1w, '近一周')

        ret_1m = index.pct_change(20 * 1)
        ret_1m = df_add_info(ret_1m, '近一月')

        ret_3m = index.pct_change(20 * 3)
        ret_3m = df_add_info(ret_3m, '近三月')

        ret_6m = index.pct_change(20 * 6)
        ret_6m = df_add_info(ret_6m, '近六月')

        ret_1y = index.pct_change(250)
        ret_1y = df_add_info(ret_1y, '近一年')

        index_2023 = index[index.index >= self.date_2023]
        ret_2023 = index_2023 / index_2023.iloc[0] - 1
        ret_2023 = df_add_info(ret_2023, '2023年以来')

        index_2022 = index[index.index >= self.date_2022]
        ret_2022 = index_2022 / index_2022.iloc[0] - 1
        ret_2022 = df_add_info(ret_2022, '2022年以来')

        index_2021 = index[index.index >= self.date_2021]
        ret_2021 = index_2021 / index_2021.iloc[0] - 1
        ret_2021 = df_add_info(ret_2021, '2021年以来')

        index_2015 = index[index.index >= self.date_2015]
        ret_2015 = index_2015 / index_2015.iloc[0] - 1
        ret_2015 = df_add_info(ret_2015, '2015年以来')

        drawdown = index.copy(deep=True)
        drawdown = drawdown.apply(lambda x: cal_drawdown(x))
        drawdown = df_add_info(drawdown, '回撤')

        ret_risk = index.copy(deep=True)
        ret_risk['IDX'] = range(len(ret_risk))
        annual_ret_1y, annual_ret_3y, annual_ret_5y, annual_ret_10y, \
        annual_vol_1y, annual_vol_3y, annual_vol_5y, annual_vol_10y, \
        max_drawdown_1y, max_drawdown_3y, max_drawdown_5y, max_drawdown_10y = \
        index.copy(deep=True), index.copy(deep=True), index.copy(deep=True), index.copy(deep=True), \
        index.copy(deep=True), index.copy(deep=True), index.copy(deep=True), index.copy(deep=True), \
        index.copy(deep=True), index.copy(deep=True), index.copy(deep=True), index.copy(deep=True)
        for col in list(ret_risk.columns)[:-1]:
            print(col)
            annual_ret_1y[col] = ret_risk['IDX'].rolling(250 * 1).apply(lambda x: cal_annual_ret(x, col, ret_risk, 250))
            annual_ret_3y[col] = ret_risk['IDX'].rolling(250 * 3).apply(lambda x: cal_annual_ret(x, col, ret_risk, 250))
            annual_ret_5y[col] = ret_risk['IDX'].rolling(250 * 5).apply(lambda x: cal_annual_ret(x, col, ret_risk, 250))
            annual_ret_10y[col] = ret_risk['IDX'].rolling(250 * 10).apply(lambda x: cal_annual_ret(x, col, ret_risk, 250))
            annual_vol_1y[col] = ret_risk['IDX'].rolling(250 * 1).apply(lambda x: cal_annual_vol(x, col, ret_risk, 250))
            annual_vol_3y[col] = ret_risk['IDX'].rolling(250 * 3).apply(lambda x: cal_annual_vol(x, col, ret_risk, 250))
            annual_vol_5y[col] = ret_risk['IDX'].rolling(250 * 5).apply(lambda x: cal_annual_vol(x, col, ret_risk, 250))
            annual_vol_10y[col] = ret_risk['IDX'].rolling(250 * 10).apply(lambda x: cal_annual_vol(x, col, ret_risk, 250))
            max_drawdown_1y[col] = ret_risk['IDX'].rolling(250 * 1).apply(lambda x: cal_max_drawdown(x, col, ret_risk, 250))
            max_drawdown_3y[col] = ret_risk['IDX'].rolling(250 * 3).apply(lambda x: cal_max_drawdown(x, col, ret_risk, 250))
            max_drawdown_5y[col] = ret_risk['IDX'].rolling(250 * 5).apply(lambda x: cal_max_drawdown(x, col, ret_risk, 250))
            max_drawdown_10y[col] = ret_risk['IDX'].rolling(250 * 10).apply(lambda x: cal_max_drawdown(x, col, ret_risk, 250))
        sharpe_ratio_1y = (annual_ret_1y - 0.015) / annual_vol_1y
        sharpe_ratio_3y = (annual_ret_3y - 0.015) / annual_vol_3y
        sharpe_ratio_5y = (annual_ret_5y - 0.015) / annual_vol_5y
        sharpe_ratio_10y = (annual_ret_10y - 0.015) / annual_vol_10y
        annual_ret_1y = df_add_info(annual_ret_1y, '年化收益率（近一年）')
        annual_ret_3y = df_add_info(annual_ret_3y, '年化收益率（近三年）')
        annual_ret_5y = df_add_info(annual_ret_5y, '年化收益率（近五年）')
        annual_ret_10y = df_add_info(annual_ret_10y, '年化收益率（近十年）')
        annual_vol_1y = df_add_info(annual_vol_1y, '年化波动率（近一年）')
        annual_vol_3y = df_add_info(annual_vol_3y, '年化波动率（近三年）')
        annual_vol_5y = df_add_info(annual_vol_5y, '年化波动率（近五年）')
        annual_vol_10y = df_add_info(annual_vol_10y, '年化波动率（近十年）')
        sharpe_ratio_1y = df_add_info(sharpe_ratio_1y, '夏普比率（近一年）')
        sharpe_ratio_3y = df_add_info(sharpe_ratio_3y, '夏普比率（近三年）')
        sharpe_ratio_5y = df_add_info(sharpe_ratio_5y, '夏普比率（近五年）')
        sharpe_ratio_10y = df_add_info(sharpe_ratio_10y, '夏普比率（近十年）')
        max_drawdown_1y = df_add_info(max_drawdown_1y, '最大回撤（近一年）')
        max_drawdown_3y = df_add_info(max_drawdown_3y, '最大回撤（近三年）')
        max_drawdown_5y = df_add_info(max_drawdown_5y, '最大回撤（近五年）')
        max_drawdown_10y = df_add_info(max_drawdown_10y, '最大回撤（近十年）')

        index = pd.concat([close, close_nav, close_ytd, ret_1w, ret_1m, ret_3m, ret_6m, ret_1y, ret_2023, ret_2022, ret_2021, ret_2015, drawdown,
                           annual_ret_1y, annual_vol_1y, sharpe_ratio_1y, max_drawdown_1y,
                           annual_ret_3y, annual_vol_3y, sharpe_ratio_3y, max_drawdown_3y,
                           annual_ret_5y, annual_vol_5y, sharpe_ratio_5y, max_drawdown_5y,
                           annual_ret_10y, annual_vol_10y, sharpe_ratio_10y, max_drawdown_10y], axis=1)
        index.index = map(lambda x: datetime.strptime(x, '%Y%m%d').date(), index.index)
        return index

    def turnover(self):
        mv_w = w.wsd(",".join(self.index_list[:3]), "mkt_cap_ard", self.start_date_hyphen, self.end_date_hyphen, usedf=True)[1].reset_index()
        mv_w['index'] = mv_w['index'].apply(lambda x: x.strftime('%Y%m%d'))
        mv_w = mv_w.set_index('index').sort_index()
        free_mv_w = w.wsd(",".join(self.index_list[:3]), "mkt_freeshares", self.start_date_hyphen, self.end_date_hyphen, usedf=True)[1].reset_index()
        free_mv_w['index'] = free_mv_w['index'].apply(lambda x: x.strftime('%Y%m%d'))
        free_mv_w = free_mv_w.set_index('index').sort_index()
        turnover_volume_w = w.wsd(",".join(self.index_list[:3]), "volume", self.start_date_hyphen, self.end_date_hyphen, usedf=True)[1].reset_index()
        turnover_volume_w['index'] = turnover_volume_w['index'].apply(lambda x: x.strftime('%Y%m%d'))
        turnover_volume_w = turnover_volume_w.set_index('index').sort_index()
        turnover_value_w = w.wsd(",".join(self.index_list[:3]), "amt", self.start_date_hyphen, self.end_date_hyphen, usedf=True)[1].reset_index()
        turnover_value_w['index'] = turnover_value_w['index'].apply(lambda x: x.strftime('%Y%m%d'))
        turnover_value_w = turnover_value_w.set_index('index').sort_index()
        index_w = w.wsd(",".join(self.index_list[:3]), "close", self.start_date_hyphen, self.end_date_hyphen, usedf=True)[1].reset_index()
        index_w['index'] = index_w['index'].apply(lambda x: x.strftime('%Y%m%d'))
        index_w = index_w.set_index('index').sort_index()
        mv = self.overseas_index_daily_k[['bzzsdm', 'jyrq', 'cur_mkt_cap']]
        mv['jyrq'] = mv['jyrq'].astype(str)
        mv = mv.pivot(index='jyrq', columns='bzzsdm', values='cur_mkt_cap').sort_index()
        free_mv = self.overseas_index_daily_k[['bzzsdm', 'jyrq', 'free_float_market_cap']]
        free_mv['jyrq'] = free_mv['jyrq'].astype(str)
        free_mv = free_mv.pivot(index='jyrq', columns='bzzsdm', values='free_float_market_cap').sort_index()
        turnover_volume = self.overseas_index_daily_k[['bzzsdm', 'jyrq', 'px_volume']]
        turnover_volume['jyrq'] = turnover_volume['jyrq'].astype(str)
        turnover_volume = turnover_volume.pivot(index='jyrq', columns='bzzsdm', values='px_volume').sort_index()
        turnover_value = self.overseas_index_daily_k[['bzzsdm', 'jyrq', 'indx_traded_val']]
        turnover_value['jyrq'] = turnover_value['jyrq'].astype(str)
        turnover_value = turnover_value.pivot(index='jyrq', columns='bzzsdm', values='indx_traded_val').sort_index()
        index = self.overseas_index_daily_k[['bzzsdm', 'jyrq', 'px_last']]
        index['jyrq'] = index['jyrq'].astype(str)
        index = index.pivot(index='jyrq', columns='bzzsdm', values='px_last').sort_index()
        mv = pd.concat([mv_w / 10000000000.0, mv / 10000.0], axis=1)
        free_mv = pd.concat([free_mv_w / 10000000000.0, free_mv / 10000.0], axis=1)
        turnover_volume = pd.concat([turnover_volume_w / 10000000000.0, turnover_volume / 10000000.0], axis=1)
        turnover_value = pd.concat([turnover_value_w / 10000000000.0, turnover_value / 10000000.0], axis=1)
        index = pd.concat([index_w, index], axis=1)
        mv = mv[mv.index.isin(self.trade_df['TRADE_DATE'].unique().tolist())].sort_index().fillna(method='ffill')
        free_mv = free_mv[free_mv.index.isin(self.trade_df['TRADE_DATE'].unique().tolist())].sort_index().fillna(method='ffill')
        turnover_volume = turnover_volume[turnover_volume.index.isin(self.trade_df['TRADE_DATE'].unique().tolist())].sort_index().fillna(method='ffill')
        turnover_value = turnover_value[turnover_value.index.isin(self.trade_df['TRADE_DATE'].unique().tolist())].sort_index().fillna(method='ffill')
        index = index[index.index.isin(self.trade_df['TRADE_DATE'].unique().tolist())].sort_index().fillna(method='ffill')
        mv = mv[self.index_list].rename(columns=self.index_name_dict)
        free_mv = free_mv[self.index_list].rename(columns=self.index_name_dict)
        turnover_volume = turnover_volume[self.index_list].rename(columns=self.index_name_dict)
        turnover_value = turnover_value[self.index_list].rename(columns=self.index_name_dict)
        index = index[self.index_list].rename(columns=self.index_name_dict)
        mv = mv[(mv.index >= self.start_date) & (mv.index <= self.end_date)]
        free_mv = free_mv[(free_mv.index >= self.start_date) & (free_mv.index <= self.end_date)]
        turnover_volume = turnover_volume[(turnover_volume.index >= self.start_date) & (turnover_volume.index <= self.end_date)]
        turnover_value = turnover_value[(turnover_value.index >= self.start_date) & (turnover_value.index <= self.end_date)]
        index = index[(index.index >= self.start_date) & (index.index <= self.end_date)]
        turnover_rate = turnover_value / mv
        volatility = index.pct_change().rolling(20).std()

        mv = df_add_info(mv, '总市值（百亿）')
        free_mv = df_add_info(free_mv, '自由流通市值（百亿）')
        turnover_volume = df_add_info(turnover_volume, '成交量（百亿）')
        turnover_value = df_add_info(turnover_value, '成交额（百亿）')
        turnover_rate = df_add_info(turnover_rate, '换手率')
        volatility = df_add_info(volatility, '20日波动率')

        turnover = pd.concat([mv, free_mv, turnover_volume, turnover_value, turnover_rate, volatility], axis=1)
        turnover.index = map(lambda x: datetime.strptime(x, '%Y%m%d').date(), turnover.index)
        return turnover

    def valuation(self):
        pe_ttm_w = w.wsd(",".join(self.index_list[:3]), "pe_ttm", self.start_date_hyphen, self.end_date_hyphen, usedf=True)[1].reset_index()
        pe_ttm_w['index'] = pe_ttm_w['index'].apply(lambda x: x.strftime('%Y%m%d'))
        pe_ttm_w = pe_ttm_w.set_index('index').sort_index()
        pb_lf_w = w.wsd(",".join(self.index_list[:3]), "pb_lf", self.start_date_hyphen, self.end_date_hyphen, usedf=True)[1].reset_index()
        pb_lf_w['index'] = pb_lf_w['index'].apply(lambda x: x.strftime('%Y%m%d'))
        pb_lf_w = pb_lf_w.set_index('index').sort_index()
        div_yield_w = w.wsd(",".join(self.index_list[:3]), "dividendyield2", self.start_date_hyphen, self.end_date_hyphen, usedf=True)[1].reset_index()
        div_yield_w['index'] = div_yield_w['index'].apply(lambda x: x.strftime('%Y%m%d'))
        div_yield_w = div_yield_w.set_index('index').sort_index()
        pe_ttm = self.overseas_index_daily_k[['bzzsdm', 'jyrq', 'pe_ratio']]
        pe_ttm['jyrq'] = pe_ttm['jyrq'].astype(str)
        pe_ttm = pe_ttm.pivot(index='jyrq', columns='bzzsdm', values='pe_ratio').sort_index()
        pb_lf = self.overseas_index_finance[['bzzsdm', 'jyrq', 'px_to_book_ratio']]
        pb_lf['jyrq'] = pb_lf['jyrq'].astype(str)
        pb_lf = pb_lf.pivot(index='jyrq', columns='bzzsdm', values='px_to_book_ratio').sort_index()
        div_yield = self.overseas_index_daily_k[['bzzsdm', 'jyrq', 'eqy_dvd_yld_12m']]
        div_yield['jyrq'] = div_yield['jyrq'].astype(str)
        div_yield = div_yield.pivot(index='jyrq', columns='bzzsdm', values='eqy_dvd_yld_12m').sort_index()
        pe_ttm = pd.concat([pe_ttm_w, pe_ttm], axis=1)
        pb_lf = pd.concat([pb_lf_w, pb_lf], axis=1)
        div_yield = pd.concat([div_yield_w, div_yield], axis=1)
        pe_ttm = pe_ttm[pe_ttm.index.isin(self.trade_df['TRADE_DATE'].unique().tolist())].sort_index().fillna(method='ffill')
        pb_lf = pb_lf[pb_lf.index.isin(self.trade_df['TRADE_DATE'].unique().tolist())].sort_index().fillna(method='ffill')
        div_yield = div_yield[div_yield.index.isin(self.trade_df['TRADE_DATE'].unique().tolist())].sort_index().fillna(method='ffill')
        pe_ttm = pe_ttm[self.index_list].rename(columns=self.index_name_dict)
        pb_lf = pb_lf[self.index_list].rename(columns=self.index_name_dict)
        div_yield = div_yield[self.index_list].rename(columns=self.index_name_dict)
        pe_ttm = pe_ttm[(pe_ttm.index >= self.start_date) & (pe_ttm.index <= self.end_date)]
        pb_lf = pb_lf[(pb_lf.index >= self.start_date) & (pb_lf.index <= self.end_date)]
        div_yield = div_yield[(div_yield.index >= self.start_date) & (div_yield.index <= self.end_date)]





        index_name_dict = {'000300': '沪深300', '000905': '中证500', '000852': '中证1000', '399303': '国证2000', '881001': '万得全A'}
        valuation = HBDB().read_index_daily_k_given_date_and_indexs(self.start_date, index_list)
        valuation = valuation[['zqdm', 'jyrq', 'pe']]
        valuation = valuation.rename(columns={'zqdm': 'INDEX_SYMBOL', 'jyrq': 'TRADE_DATE', 'pe': 'PE（TTM）'})
        valuation['TRADE_DATE'] = valuation['TRADE_DATE'].astype(str)
        valuation = valuation[valuation['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        valuation = valuation[(valuation['TRADE_DATE'] >= self.start_date) & (valuation['TRADE_DATE'] <= self.end_date)]
        valuation = valuation.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='PE（TTM）').sort_index()
        valuation = valuation.replace(0.0, np.nan)
        valuation = valuation[index_list].rename(columns=index_name_dict)
        valuation['IDX'] = range(len(valuation))

        pettm = valuation.copy(deep=True).drop('IDX', axis=1)
        pettm = pettm.T.reset_index()
        pettm['TYPE'] = 'PE（TTM）'
        pettm = pettm.set_index(['TYPE', 'INDEX_SYMBOL']).T

        pettm_relative = valuation.copy(deep=True)
        pettm_relative['沪深300PE（TTM）/中证1000PE（TTM）'] = pettm_relative['沪深300'] / pettm_relative['中证1000']
        pettm_relative = pettm_relative[['沪深300PE（TTM）/中证1000PE（TTM）']]
        pettm_relative = pettm_relative.T.reset_index()
        pettm_relative['TYPE'] = '比值'
        pettm_relative = pettm_relative.set_index(['TYPE', 'INDEX_SYMBOL']).T

        pettm_q1y = valuation.copy(deep=True).drop('IDX', axis=1)
        for col in list(pettm_q1y.columns):
            pettm_q1y[col] = valuation['IDX'].rolling(250 * 1).apply(lambda x: quantile_definition(x, col, valuation))
        pettm_q1y = pettm_q1y.T.reset_index()
        pettm_q1y['TYPE'] = '近一年分位水平'
        pettm_q1y = pettm_q1y.set_index(['TYPE', 'INDEX_SYMBOL']).T

        pettm_q3y = valuation.copy(deep=True).drop('IDX', axis=1)
        for col in list(pettm_q3y.columns):
            pettm_q3y[col] = valuation['IDX'].rolling(250 * 3).apply(lambda x: quantile_definition(x, col, valuation))
        pettm_q3y = pettm_q3y.T.reset_index()
        pettm_q3y['TYPE'] = '近三年分位水平'
        pettm_q3y = pettm_q3y.set_index(['TYPE', 'INDEX_SYMBOL']).T

        pettm_q5y = valuation.copy(deep=True).drop('IDX', axis=1)
        for col in list(pettm_q5y.columns):
            pettm_q5y[col] = valuation['IDX'].rolling(250 * 5).apply(lambda x: quantile_definition(x, col, valuation))
        pettm_q5y = pettm_q5y.T.reset_index()
        pettm_q5y['TYPE'] = '近五年分位水平'
        pettm_q5y = pettm_q5y.set_index(['TYPE', 'INDEX_SYMBOL']).T

        valuation = pd.concat([pettm, pettm_relative, pettm_q1y, pettm_q3y, pettm_q5y], axis=1)
        valuation.index = map(lambda x: datetime.strptime(x, '%Y%m%d').date(), valuation.index)
        return valuation

    def get_all(self):
        # index = self.index()
        turnover = self.turnover()
        # valuation = self.valuation()

        filename = '{0}overseas_overview.xlsx'.format(self.data_path)
        app = xlwings.App(visible=False)
        wookbook = app.books.open(filename)
        sheet_names = [wookbook.sheets[i].name for i in range(len(wookbook.sheets))]
        # index_wooksheet = wookbook.sheets['指数']
        # index_wooksheet.clear()
        # index_wooksheet["A1"].options(pd.DataFrame, header=1, expand='table').value = index
        valuation_wooksheet = wookbook.sheets['成交']
        valuation_wooksheet.clear()
        valuation_wooksheet["A1"].options(pd.DataFrame, header=1, expand='table').value = turnover
        wookbook.save(filename)
        wookbook.close()
        app.quit()
        return


if __name__ == '__main__':
    start_date = '20070101'
    end_date = '20231117'
    data_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/overseas_overview/'
    OverseasOverview(start_date, end_date, data_path).get_all()