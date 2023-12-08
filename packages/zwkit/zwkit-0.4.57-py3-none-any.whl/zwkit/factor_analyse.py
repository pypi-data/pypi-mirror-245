import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import stats
import datetime as dt
import pandas as pd


def group_analysis(y, num=10):
    """
    y = ['trade_date','factor','returns']
    :param y:
    :param num:
    :return:
    """
    # 时间序列的因子分层
    result = {}

    data = y.copy()
    data['returns'] = data['returns'].apply(lambda x: x / 100)
    data.sort_values(by=['trade_date', 'ols_factor'], ascending=[True, False], inplace=True)
    for date in data['trade_date'].unique().tolist():
        df = data[data['trade_date'] == date]
        gap = [int(i) for i in list(np.linspace(start=0, stop=len(df), num=num + 1))]
        temp = {}
        for i in range(0, num):
            temp[f'group_{i + 1}'] = df['returns'][gap[i]:gap[i + 1]].mean()
        result[date] = temp

    gap = [int(i) for i in list(np.linspace(start=0, stop=len(data), num=num + 1))]
    factor_mean_list = []
    for i in range(0, num):
        factor_mean = data["returns"][gap[i]:gap[i + 1]].mean() + 1
        factor_mean_list.append(factor_mean)
    value = (
        np.corrcoef(np.array(factor_mean_list).argsort(), (np.arange(0, num)))[0, 1])
    return result, value


def group_analyse_table(y, num):
    factor_data, value = group_analysis(y, num)
    # 将factor_data 按照日期排序
    data = pd.DataFrame(factor_data).T
    group_return = (data + 1).cumprod()
    group_return.plot(figsize=(15, 8), title='分层效应检验')
    plt.show()
    return value, group_return


def ic_analysis(returns):
    rets = returns[['symbol', 'trade_date', 'returns']].pivot(index='trade_date', columns='symbol', values='returns')
    data = returns[['symbol', 'trade_date', 'ols_factor']].pivot(index='trade_date', columns='symbol', values='ols_factor')
    x = data.corrwith(rets, axis=1, method='spearman').dropna(how='all')
    t_stat, p_value = stats.ttest_1samp(x, 0)
    IC = {
        'IC': round(x.mean(), 4),  # ic是因子收益率和股票收益率的相关系数
        'IC std': round(x.std(), 4),  # ic的标准差是因子收益率和股票收益率的相关系数的标准差
        'IR': round(x.mean() / x.std(), 4),  # ir是ic的均值除以ic的标准差
        'IR_ly': round(x[-252:].mean() / x[-252:].std(), 4),  # ir_ly是ic的均值除以ic的标准差，只计算最近252天的数据
        'IC>0': round(len(x[x > 0].dropna()) / len(x), 4),  # ic>0是因子收益率和股票收益率的相关系数大于0的比例
        'ABS_IC>2%': round(len(x[abs(x) > 0.02].dropna()) / len(x), 4),  # abs_ic>2%是因子收益率和股票收益率的相关系数的绝对值大于0.02的比例
        't_stat': round(t_stat, 4),  # t_stat是ic的t检验值，用于检验ic是否显著，如果显著则说明因子收益率和股票收益率的相关系数不为0，结论是因子有效
    }
    return IC


def ic_cumsum(data):
    rets = data[['symbol', 'trade_date', 'returns']].pivot(index='trade_date', columns='symbol', values='returns')
    data = data[['symbol', 'trade_date', 'ols_factor']].pivot(index='trade_date', columns='symbol', values='ols_factor')
    x = data.corrwith(rets, axis=1, method='spearman').dropna(how='all')
    return x.cumsum()


def ic_cumsum_table(data):
    x = ic_cumsum(data)
    x.plot(figsize=(20, 10))
    plt.title('IC Cumsum')
    plt.xlabel('date')
    plt.ylabel('IC')
    plt.legend()
    plt.show()


def ic_month(data):
    data['trade_date'] = data['trade_date'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
    rets = data[['symbol', 'trade_date', 'returns']].pivot(index='trade_date', columns='symbol', values='returns')
    data = data[['symbol', 'trade_date', 'ols_factor']].pivot(index='trade_date', columns='symbol', values='ols_factor')
    x = data.corrwith(rets, axis=1, method='spearman').dropna(how='all')
    return x.resample('M').mean()


def ic_month_table(data):
    x = ic_month(data)
    x.plot(kind="bar", figsize=(20, 10))
    # plt.title('IC Month')
    # plt.xlabel('date')
    # plt.ylabel('IC')
    # plt.legend()
    # plt.show()
