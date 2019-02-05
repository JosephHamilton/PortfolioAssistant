#!/usr/bin/python3

from DBHandler import DBHandler
from DataGatherer import DataGatherer
from Positions import Position


class Portfolio:
    """
    Portfolio keeps track of all positions currently being held.
    """

    def __init__(self):
        """
        Create a new db handler object and data gatherer object
        """
        self.db = DBHandler()
        self.scraper = DataGatherer()

    def __del__(self):
        """
        Deconstructor of class to close database connection
        """
        del self.db

    def add_position(self, symbol, shares, cost):
        """
        If I already have a position in the stock update the information, otherwise
        add a new position for the stock
        :param symbol: symbol of stock
        :param shares: number of shares in position
        :param cost: cost per share of stock
        """
        current_positions = self.db.current_positions()

        if symbol.upper() in current_positions:
            # Update positions
            pos = self.db.retrieve_position(symbol.upper())
            pos.buy_shares(shares, cost)
            self.db.update_position(pos)

        else:
            exp_earnings = self.scraper.get_expected_earnings(symbol)
            position = Position(symbol, shares, cost, exp_earnings)

            self.db.add_position(position)

    def close_positions(self, symbol):
        """
        Close the positions for the symbol given
        :param symbol: symbol of stock
        """
        # Retrieve information on my position from the database
        pos = self.db.retrieve_position(symbol.upper())

        if pos is not None:
            pos.numShares = 0
            self.db.update_position(pos)

    def sell_position(self, symbol, shares, price):
        """
        Sell some shares of the positions but don't close completely
        :param symbol: symbol of stock
        :param shares: number of shares sold
        :param price: price of shares sold
        """
        current_positions = self.db.current_positions()

        if symbol.upper() in current_positions:
            # Sell shares
            pos = self.db.retrieve_position(symbol.upper())
            pos.sell_shares(shares, price)

            self.db.update_position(pos)

        else:
            print("No shares of stock owned")

    def update_expected_earnings(self):
        """
        Check expected earnings for all positions currently being held
        """
        positions = self.db.db_to_array()

        for position in positions:
            position.expectedEarningsDate = self.scraper.get_expected_earnings(position.symbol)
            self.db.update_position(position)

    def print(self):
        """ Helper method to print portfolio information
        """
        test_positions = self.db.db_to_array()

        for pos in test_positions:
            pos.print()
