''' Moving Average Crossover Strategy '''

#from connectors import devo
from datetime import datetime as dt


class MovingAverageCrossover:
    def __init__(self):
        self.trade_signals = []

    def download_data(self, initial_date, end_date):
        try:
            df = devo.read_sql(f"""SELECT time_period, obs_value
                                FROM crp_other_pub.fx
                                WHERE time_period >= '{initial_date}'
                                AND time_period <= '{end_date}'
                                AND series_key = 'FX.B.USD.EUR.BL.FX.USDEUR.HST'
                                """)
            return df
        except:
            print("\n Note!!! You may not have the same data connection as me. Modify the 'download_data' function. \n")

    def moving_average(self, df, n_days):
        df[f'MA{n_days}'] = df['obs_value'].rolling(n_days).mean()
        return df

    def crossovers(self, df):
        price_list = df.values.tolist()
        previous_price = None
        for price in price_list:
            if not previous_price:
                previous_price = price
            else:
                if (previous_price[2] < previous_price[3] and
                    price[2] > price[3]):
                    self.trade_signals.append([price[0], 'BUY'])
                if (previous_price[2] > previous_price[3] and
                    price[2] < price[3]):
                    self.trade_signals.append([price[0], 'SELL'])
                previous_price = price


mac = MovingAverageCrossover()
df = mac.download_data("2023-01-01", "2023-10-10")
df = mac.moving_average(df, 20)
df = mac.moving_average(df, 50)
df = mac.crossovers(df)

print(mac.trade_signals)