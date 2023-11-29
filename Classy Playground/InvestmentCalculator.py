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