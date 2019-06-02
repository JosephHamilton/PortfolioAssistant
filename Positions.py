#!/usr/bin/python3

# TODO: Add difference between stocks and options contracts


class Position:
    def __init__(self, symbol, numShares, averageCost, expectedEarnings):
        """
        Stores all necessary information for the current stock position
        
        Parameters
        ----------
        symbol : str
            Stock symbol
        numShares : int
            Number of shares purchased
        averageCost : float
            Average cost per share
        expectedEarnings : datetime
            Date of expected earnings
        """

        self.symbol = symbol.upper()
        self.numShares = numShares
        self.averageCost = averageCost
        self.totalInvestment = numShares * averageCost
        self.expectedEarningsDate = expectedEarnings

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
        self.totalInvestment -= price * quantity

    def print(self):
        """
        Helper method to print out the position
        """
        # TODO: Change to __repr__ or some magic method
        print("Symbol: {}\n"
              "Number of Shares: {}\n"
              "Average Cost: ${:,.2f}\n"
              "Total Investment: ${:,.2f}\n"
              "Expected Earnings Report: {}\n".format(self.symbol, self.numShares, self.averageCost,
                                                      self.totalInvestment, self.expectedEarningsDate))
