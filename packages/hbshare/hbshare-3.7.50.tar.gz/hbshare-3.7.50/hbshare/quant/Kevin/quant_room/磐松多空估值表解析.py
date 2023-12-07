"""
磐松多空估值表解析模块
"""
import os
import pandas as pd


def long_short_holding_extractor():
    data_path = "D:\\估值表基地\\磐松多空对冲"
    filenames = os.listdir(data_path)
    names_xls = [x for x in filenames if x.split('.')[-1] in ['xls', 'xlsx']]
    # 2-5号
    holding_list = []
    for name in names_xls:
        fund_name = name.split('_')[1]
        date = name.split('_')[-2]
        if fund_name in ['磐松多空对冲2号私募证券投资基金']:
            context = "市值占净值%"
            hd = 3
            data = pd.read_excel(
                os.path.join(data_path, name), sheet_name=0, header=hd).dropna(subset=['科目代码'])
            sh = data[data['科目代码'].str.startswith('11021101')]
            sz = data[data['科目代码'].str.startswith('11021201')]
            cyb = data[data['科目代码'].str.startswith('11021501')]
            kcb = data[data['科目代码'].str.startswith('1102D201')]
            long_df = pd.concat([sh, sz, cyb, kcb], axis=0).dropna()
            long_df['direction'] = 'long'
            sh_short = data[data['科目代码'].str.startswith('21010101')]
            kcb_short = data[data['科目代码'].str.startswith('21010201')]
            sz_short = data[data['科目代码'].str.startswith('21013101')]
            cyb_short = data[data['科目代码'].str.startswith('21014101')]
            short_df = pd.concat([sh_short, sz_short, cyb_short, kcb_short], axis=0).dropna()
            short_df['direction'] = 'short'
            holding_df = pd.concat([long_df, short_df], axis=0)
            holding_df['ticker'] = holding_df['科目代码'].apply(lambda x: x[-6:])
            holding_df.rename(columns={"科目名称": "sec_name", context: "weight"}, inplace=True)
            holding_df = holding_df[['ticker', 'sec_name', 'weight', 'direction']]
        elif fund_name in ['磐松多空对冲3号私募证券投资基金', '磐松多空对冲5号私募证券投资基金']:
            data = pd.read_excel(
                os.path.join(data_path, name), sheet_name=0, header=6).dropna(subset=['科目代码'])
            data['科目代码'] = data['科目代码'].map(str)
            sh = data[data['科目代码'].str.endswith('SH')]
            sz = data[data['科目代码'].str.endswith('SZ')]
            holding_df = pd.concat([sh, sz], axis=0).dropna()
            holding_df = holding_df[
                (holding_df['科目代码'].str.startswith('1102')) | (holding_df['科目代码'].str.startswith('2101'))]
            holding_df['ticker'] = holding_df['科目代码'].apply(lambda x: x.split('.')[-1].split(' ')[0])
            holding_df.rename(columns={"科目名称": "sec_name", "市值占比": "weight"}, inplace=True)
            holding_df.loc[holding_df['科目代码'].str.startswith('2'), 'direction'] = 'short'
            holding_df['direction'].fillna('long', inplace=True)
        else:
            holding_df = pd.DataFrame()

        holding_df['fund_name'] = fund_name
        holding_df['trade_date'] = date
        holding_list.append(holding_df)

    inc = ['ticker', 'weight', 'direction', 'fund_name', 'trade_date']
    holding_df_other = pd.concat(holding_list)[inc]

    # 多空对冲1号
    path_inner = os.path.join(data_path, "LONGSHORT")
    filenames = os.listdir(path_inner)
    holding_list_one = []
    for file_name in filenames:
        fund_name = file_name.split('_')[1]
        date = file_name.split('_')[-1].split('.')[0]
        context = "市值占净值%"
        data = pd.read_excel(
            os.path.join(path_inner, file_name), sheet_name=0, header=3).dropna(subset=['科目代码'])
        sh = data[data['科目代码'].str.startswith('11021101')]
        sz = data[data['科目代码'].str.startswith('11021201')]
        cyb = data[data['科目代码'].str.startswith('11021501')]
        kcb = data[data['科目代码'].str.startswith('1102D201')]
        long_df = pd.concat([sh, sz, cyb, kcb], axis=0).dropna()
        long_df['direction'] = 'long'
        sh_short = data[data['科目代码'].str.startswith('21010101')]
        kcb_short = data[data['科目代码'].str.startswith('21010201')]
        sz_short = data[data['科目代码'].str.startswith('21013101')]
        cyb_short = data[data['科目代码'].str.startswith('21014101')]
        short_df = pd.concat([sh_short, sz_short, cyb_short, kcb_short], axis=0).dropna()
        short_df['direction'] = 'short'
        holding_df = pd.concat([long_df, short_df], axis=0)
        holding_df['ticker'] = holding_df['科目代码'].apply(lambda x: x[-6:])
        holding_df.rename(columns={"科目名称": "sec_name", context: "weight"}, inplace=True)
        holding_df = holding_df[['ticker', 'sec_name', 'weight', 'direction']]
        holding_df['fund_name'] = fund_name
        holding_df['trade_date'] = date
        holding_list_one.append(holding_df)

    inc = ['ticker', 'weight', 'direction', 'fund_name', 'trade_date']
    holding_df_1 = pd.concat(holding_list_one)[inc]

    return holding_df_other, holding_df_1



if __name__ == '__main__':
    hd1, hd2 = long_short_holding_extractor()
