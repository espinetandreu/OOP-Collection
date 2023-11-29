""" Black-Sholes Model """

import numpy as np
from scipy.stats import norm


class European_Option:
    def __init__(self, strike_price, stock_price, expiration_time,
                 risk_free_rate, volatility):
        self.strike_price = strike_price
        self.stock_price = stock_price
        self.expiration_time = expiration_time
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility


class BlackSholesModel:
    def __init__(self, option, time):
        self.option = option
        self.time = time
        self.thau = self.get_thau()
        self.call_value = self.get_call_value()
        self.put_value = self.get_put_value()
        self.call_greeks = self.get_call_greeks()

    def get_thau(self):
        thau = self.option.expiration_time - self.time
        return thau

    def get_d_parameters(self):
        d1 = 1/(self.option.volatility*np.sqrt(self.thau))*(np.log(self.option.stock_price/ \
             self.option.strike_price)+(self.option.risk_free_rate+(self.option.volatility**2/ \
             2))*self.thau)
        d2 = d1 - self.option.volatility*self.thau
        return d1, d2

    def get_call_value(self):
        d1, d2 = self.get_d_parameters()
        call_value = norm.cdf(d1)*self.option.stock_price - \
                    norm.cdf(d2)*self.option.strike_price* \
                    np.exp(-self.option.risk_free_rate*self.thau)
        return call_value

    def get_put_value(self):
        put_value = self.call_value + self.option.strike_price*\
                    np.exp(-self.option.risk_free_rate*self.thau) \
                    - self.option.stock_price
        return put_value

    def get_call_greeks(self):
        call_greeks = {}
        d1, d2 = self.get_d_parameters()
        call_greeks["Delta"] = norm.cdf(d1)
        # I should do also the other greeks...
        return call_greeks


strike_price = 202
stock_price = 200
expiration_time = 2 # in years
risk_free_rate = 0.02 # %annualized
volatility = 0.2
time = 1 # when is the option priced

option = European_Option(strike_price, stock_price, expiration_time, 
                         risk_free_rate, volatility)
bsm = BlackSholesModel(option, time)

print(bsm.call_value, bsm.put_value, bsm.call_greeks)