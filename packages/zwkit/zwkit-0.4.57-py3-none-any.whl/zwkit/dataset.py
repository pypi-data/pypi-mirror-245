from . import ddbkit


class dataset_model:
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def get_factor_daily_data(self, end_date, start_date, columns: list):
        s = ddbkit.connect(self.address, self.port)
        start_date = start_date.replace('-', '.')
        end_date = end_date.replace('-', '.')
        # 将list转换成str
        cols = '`' + '`'.join(columns)
        s.run("use data::barra_date_data")
        s.run("use data::dh_kit")
        s.run("data = barra_date_data::get_data_by_date(%s,%s,%s)" % (end_date, start_date, cols))
        result = s.run("select *,year(trade_date) as year,monthOfYear(trade_date) as month from data order by symbol,trade_date asc")
        ddbkit.close_ddb(s)
        return result

    def get_data_returns_by_shift(self, end_date, start_date, shift, symbol_list):
        s = ddbkit.connect(self.address, self.port)
        s.run("use data::data_kit")
        symbol_list = '`' + '`'.join(symbol_list)
        start_date = start_date.replace('-', '.')
        end_date = end_date.replace('-', '.')
        data = s.run("data_kit::get_returns_by_symbol(%s,%s,%s,%s)" % (symbol_list, start_date, end_date, shift))
        ddbkit.close_ddb(s)
        return data
