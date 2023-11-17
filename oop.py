
"""  OBJECT ORIENTED PROGRAMMING PRACTICE """


'''  Word Frequency Counter  '''

class WordFrequencyCounter:
    def __init__(self):
        self.frequencies = {}

    def count(self, text):
        tokens = text.split()
        for token in tokens:
            if token not in self.frequencies:
                self.frequencies[token] = 1
            else:
                self.frequencies[token] += 1

    def query_frequency(self, word):
        if word in self.frequencies:
            return self.frequencies[word]

wfc = WordFrequencyCounter()
wfc.count("Hello world")
print(wfc.query_frequency('world'))



'''  Investment Portfolio Calculator  '''

from datetime import datetime as dt

class PortfolioCalculator:
    def __init__(self):
        self.investments = []
        self.date_format = "%Y-%m-%d"
        
        
    def add_investment_atributes(self, list_of_investments):
        for investment in list_of_investments:
            self.investments.append(investment)
        
    def day_difference(self, day1, day2):
        day1 = dt.strptime(day1, self.date_format)
        day2 = dt.strptime(day2, self.date_format)
        delta = day2 - day1
        return delta.days
    
    def calculate_value(self, annual_interest_rate, date):
        daily_interest_rate = annual_interest_rate/365
        value = 0
        for i in range(len(self.investments)):
            days = self.day_difference(self.investments[i][0], date)
            value += self.investments[i][1]*(1+daily_interest_rate)**days
        return round(value,2)


list_of_investments = [
    ("2023-01-01", 1000.0),  # (Date, Amount)
    ("2023-03-15", 500.0),
    ("2023-06-30", 750.0),
]
annual_interest_rate = 0.05

pc = PortfolioCalculator()
pc.add_investment_atributes(list_of_investments)
print(pc.calculate_value(annual_interest_rate, "2023-08-30"))



''' Moving Average Crossover Strategy '''

from connectors import devo
from datetime import datetime as dt


class MovingAverageCrossover:
    
    def __init__(self):
        self.trade_signals = []
    
    
    def download_data(self, initial_date, end_date):
        df = devo.read_sql(f"""SELECT time_period, obs_value
                            FROM crp_other_pub.fx
                            WHERE time_period >= '{initial_date}'
                            AND time_period <= '{end_date}'
                            AND series_key = 'FX.B.USD.EUR.BL.FX.USDEUR.HST'
                            """)
        return df
    
    
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
df = mac.download_data("2023-01-01","2023-10-10")
df = mac.moving_average(df, 20)
df = mac.moving_average(df, 50)
df = mac.crossovers(df)
print(mac.trade_signals)



''' Minimum Spanning Tree (MST) for Portfolio Diversification 

Description CHAT_GPT: The Minimum Spanning Tree (MST) algorithm can be applied in 
quantitative finance to optimize portfolio diversification. The idea is to 
construct a minimum spanning tree from a correlation or covariance matrix of 
assets. This tree represents an efficient way to diversify a portfolio, 
ensuring that the selected assets are minimally correlated with each other.


'''

class Node:
    
    def __init__(self, node_name):
        self._node_name = node_name
        self._neighbors = []


    def add_neighbor(self, node_name, neighbour_node_name, edge_value):
        self._neighbors.append((node_name, neighbour_node_name, edge_value))


    def get_neighbors(self):
        return self._neighbors



class Graph:
    
    def __init__(self, node_names):
        self._nodes = {}
        self._node_names = node_names


    def create_graph(self, correlation_matrix):
        for i, row in enumerate(correlation_matrix):
            node = Node(self._node_names[i])
            for j, edge_value in enumerate(row):
                if i != j:
                    node.add_neighbor(self._node_names[i], self._node_names[j], edge_value)
            self._nodes[self._node_names[i]] = node


    def get_node(self, node_name: str) -> Node:
        return self._nodes.get(node_name)


    def get_nodes(self):
        return self._nodes
    
    
    def get_nodes_names(self):
        return self._node_names
    


class MinimumSpanningTree:
    
    def __init__(self, graph):
        self._graph = graph
        self._forest = []
        self._included_nodes = []


    def minimum_cost_neighbor(self, neighbors):
      abs_min_cost = min(abs(neighbor[2]) for neighbor in neighbors)
      for neighbor in neighbors:
          if abs(neighbor[2]) == abs_min_cost:
              min_cost_neighbor = neighbor
              return min_cost_neighbor
    
    
    def calculate_cost(self):
        node_names = graph.get_nodes_names()
        self._included_nodes.append("E")
        while len(self._included_nodes) < len(node_names):
            tree_neighbors = []
            for included_node_name in self._included_nodes:
                included_node = graph.get_node(included_node_name)
                node_neighbors = included_node.get_neighbors()
                tree_neighbors.extend(node_neighbors)
            while len(tree_neighbors)>0:
                min_cost_neighbor = self.minimum_cost_neighbor(tree_neighbors)
                if not min_cost_neighbor[1] in self._included_nodes:
                    self._included_nodes.append(min_cost_neighbor[1])
                    self._forest.append(min_cost_neighbor)
                    break
                tree_neighbors.remove(min_cost_neighbor)
     
        
    def get_forest(self):
        return self._forest
    
    

class PortfolioDiversification:
    
    def __init__(self, forest, total_investment):
        self._forest = forest
        self._weights = {}
        self._investment_alocation = {}
        self._total_investment = total_investment
        
        
    def allocate_invesments(self):
        for edge in self._forest:
            asset1, asset2, weight = edge[0],edge[1], edge[2]
            if asset1 in self._weights:
                self._weights[asset1] += abs(1/weight)
            else:
                self._weights[asset1] = abs(1/weight)
            if asset2 in self._weights:
                self._weights[asset2] += abs(1/weight)
            else:
                self._weights[asset2] = abs(1/weight)
        total_weight = sum(self._weights.values())
        self._investment_alocation = {asset: self._total_investment * weight / total_weight 
                              for asset, weight in self._weights.items()}
        
    def get_investment_allocation(self):
        return self._investment_alocation
    
    
    def get_asset_weights(self):
        return self._weights



# Example
correlation_matrix = [
    [1.0, 0.6, -0.2, 0.1, 0.4],
    [0.6, 1.0, 0.3, -0.1, 0.7],
    [-0.2, 0.3, 1.0, 0.4, -0.2],
    [0.1, -0.1, 0.4, 1.0, 0.5],
    [0.4, 0.7, -0.2, 0.5, 1.0]
]

node_names = ['A', 'B', 'C', 'D', 'E']

total_investment = 10000


graph = Graph(node_names)
graph.create_graph(correlation_matrix)

mst = MinimumSpanningTree(graph)
mst.calculate_cost()
forest = mst.get_forest()

pd = PortfolioDiversification(forest, total_investment)
pd.allocate_invesments()
investment_allocation = pd.get_investment_allocation()
asset_weights = pd.get_asset_weights()


print(f"Forest: {forest}")
print(f"Asset weights: {asset_weights}")
print(f"Investment allocation: {investment_allocation}")




""" Black-Sholes Model

The Black-Scholes Model provides formulas to calculate the prices of European
call and put options. It has paved the way for a better understanding of 
financial derivatives and has been instrumental in the development of various 
option trading strategies and risk management techniques.
"""

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
        #Hauria de fer les altre pero fa mandra...
        return call_greeks
        
    
strike_price = 202
stock_price = 200
expiration_time = 2 # in years
risk_free_rate = 0.02 # %annualized
volatility = 0.2

option = European_Option(strike_price, stock_price, expiration_time, 
                         risk_free_rate, volatility)

time = 1 # when is the option priced

bsm = BlackSholesModel(option, time)
print(bsm.call_value, bsm.put_value, bsm.call_greeks)
"Outut: 16.8713 14.8714 {'Delta': 0.5597}"



'''
binomial tree, Monte-Carlo
'''