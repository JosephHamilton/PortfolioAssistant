#!/usr/bin/python3

# TODO: Add difference between stocks and options contracts


class Position:
    def __init__(self, symbol, num_shares=0, average_cost=0, expected_earnings=None):
        """
        Stores all necessary information for the current stock position

        Parameters
        ----------
        symbol : str
            Stock symbol
        num_shares : int
            Number of shares purchased
        average_cost : float
            Average cost per share
        expected_earnings : datetime
            Date of expected earnings
        """

        self.symbol = symbol.upper()
        self.numShares = num_shares
        self.averageCost = average_cost
        self.totalInvestment = num_shares * average_cost
        self.expectedEarningsDate = expected_earnings

    def __repr__(self):
        return f'{self.symbol}(num_shares={self.numShares}, average_cost={self.averageCost}, ' \
               f'expected_earnings={self.expectedEarningsDate})'

    def __add__(self, other):
        if not isinstance(other, Position):
            raise TypeError('Other object is not of type Position')

        self.numShares += other.numShares
        self.averageCost = (self.totalInvestment + float(other.numShares * other.averageCost)) / self.numShares
        self.totalInvestment = self.averageCost * self.numShares
        return self

    def __sub__(self, other):
        if not isinstance(other, Position):
            raise TypeError('Other object is not of type Position')

        self.numShares -= other.numShares
        self.totalInvestment = self.averageCost * self.numShares
        return self

    def buy_shares(self, quantity, cost):
        """
        Buy more shares of the stock

        Parameters
        ----------
        quantity : int
            Number of shares to purchase
        cost : float
            Cost per share
        """

        self.numShares += quantity
        self.averageCost = (self.totalInvestment + (quantity * cost)) / self.numShares
        self.totalInvestment = self.averageCost * self.numShares

    def sell_shares(self, quantity, price):
        """
        Sell shares of the position

        Parameters
        ----------
        quantity : int
            Number of shares to sell
        price : float
            Price per share sold
        """

        self.numShares -= quantity
        self.totalInvestment = self.averageCost * quantity
