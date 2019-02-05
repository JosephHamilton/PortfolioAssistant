#!/usr/bin/python3

# TODO: Add difference between stocks and options contracts


class Position:
    """
    Positions object that holds all the information about a stock position.
    """

    def __init__(self, symbol, numShares, averageCost, expectedEarnings):
        """
        Create a new position with all given information
        :param symbol: stock symbol
        :param numShares: number of shares in position
        :param averageCost: average cost of the position
        :param expectedEarnings: expected date for earnings report
        """
        self.symbol = symbol.upper()
        self.numShares = numShares
        self.averageCost = averageCost
        self.totalInvestment = numShares * averageCost
        self.expectedEarningsDate = expectedEarnings

    def buy_shares(self, quantity, cost):
        """
        Buy more shares of the current position
        :param quantity: number of shares being purchased
        :param cost: cost per share
        """
        self.numShares += quantity
        self.averageCost = (self.totalInvestment + (quantity * cost)) / self.numShares
        self.totalInvestment = self.averageCost * self.numShares

    def sell_shares(self, quantity, price):
        """
        Sell shares of the current position
        :param quantity: number of shares sold
        :param price: price of shares sold
        """
        self.numShares -= quantity
        self.totalInvestment -= price * quantity

    def print(self):
        """
        Helper method to cleanly display positions information
        """
        print("Symbol: {}\n"
              "Number of Shares: {}\n"
              "Average Cost: ${:,.2f}\n"
              "Total Investment: ${:,.2f}\n"
              "Expected Earnings Report: {}\n".format(self.symbol, self.numShares, self.averageCost,
                                                      self.totalInvestment, self.expectedEarningsDate))
