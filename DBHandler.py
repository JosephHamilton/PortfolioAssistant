#!/usr/bin/python3

import sqlite3

from Positions import Position


class DBHandler:
    """
    Handles interactions with the database.
    """

    def __init__(self):
        """
        Connect to the portfolio database.  Check if the positions table exists and
        create the table if one doesn't exist.
        """
        self.conn = sqlite3.connect('testPortfolio.db')

        self.c = self.conn.cursor()

        self.c.execute('''CREATE TABLE IF NOT EXISTS positions
                     (symbol text, shares real, avgCost real, totalInvestment real, expectedEarnings text)''')

    def add_position(self, position):
        """
        Add new position to database
        :param position: new position being added
        """
        self.c.execute("INSERT INTO positions VALUES (?, ?, ?, ?, ?)", (
            position.symbol, position.numShares, position.averageCost, position.totalInvestment,
            position.expectedEarningsDate))
        self.conn.commit()

    def update_position(self, position):
        """
        Update number of shares for a given symbol.
        :param position: stock position being updated
        """
        if position.numShares > 0:
            self.c.execute(
                "UPDATE positions SET shares=?, avgCost=?, totalInvestment=?, expectedEarnings=? WHERE symbol=?", (
                    position.numShares, position.averageCost, position.totalInvestment, position.expectedEarningsDate,
                    position.symbol))
        else:
            self.c.execute("DELETE FROM positions WHERE symbol=?", (position.symbol,))

        self.conn.commit()

    def retrieve_position(self, sym):
        """
        Retrieve information on the symbol given.
        :param sym: symbol of desired position
        :return: position information for given symbol if found, none if no position held
        """
        self.c.execute('SELECT * FROM positions WHERE symbol=?', (sym,))
        row = self.c.fetchone()

        if row is None:
            return None
        else:
            return Position(row[0], row[1], row[2], row[4])

    def current_positions(self):
        """
        Return symbols of current positions.
        :return: list of symbols of current positions
        """
        current_positions = []

        for row in self.c.execute('SELECT symbol FROM positions ORDER BY symbol'):
            current_positions.append(row[0])

        return current_positions

    def db_to_array(self):
        """
        Return all information in database as array.
        :return: all information for all positions in portfolio database
        """
        return_positions = []

        for row in self.c.execute('SELECT * FROM positions ORDER BY symbol'):
            pos = Position(row[0], row[1], row[2], row[4])
            return_positions.append(pos)

        return return_positions

    def __del__(self):
        """
        Close the connection to the database.
        """
        self.conn.close()
