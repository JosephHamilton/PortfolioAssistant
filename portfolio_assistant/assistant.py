import portfolio_assistant.helpers


class Position:
    def __init__(self, symbol, num_shares=0, average_cost=0, expected_earnings=None):
        """
        Stores all necessary information for the current stock position
        TODO: Add difference between stocks and options contracts

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


class Portfolio:
    def __init__(self):
        """
        Connect to the portfolio database
        """
        self.conn = sqlite3.connect('testPortfolio.db', check_same_thread=False)

        self.c = self.conn.cursor()

        # Check if the table exists; create the table if it does not exist
        self.c.execute('''CREATE TABLE IF NOT EXISTS positions
                     (symbol TEXT, shares INTEGER, avgCost REAL, totalInvestment REAL, expectedEarnings TEXT)''')

    def add_position(self, new_position):
        """
        Add new position to the database

        Parameters
        ----------
        new_position : Position
            New position being added
        """

        current_position = self.retrieve_position(new_position.symbol)

        if current_position is None:
            self.c.execute("INSERT INTO positions VALUES (?, ?, ?, ?, ?)", (
                str(new_position.symbol), int(new_position.numShares), float(new_position.averageCost), float(new_position.totalInvestment),
                new_position.expectedEarningsDate))
        else:
            # Update position in database with new information
            current_position += new_position
            self.c.execute(
                "UPDATE positions SET shares=?, avgCost=?, totalInvestment=?, expectedEarnings=? WHERE symbol=?", (
                    int(current_position.numShares), float(current_position.averageCost), float(current_position.totalInvestment), current_position.expectedEarningsDate,
                    str(current_position.symbol)))

        self.conn.commit()

    def sell_position(self, new_position):
        """
        Sell position

        Parameters
        ----------
        new_position : Position
            New position being added
        """

        current_position = self.retrieve_position(new_position.symbol)

        if current_position is None:
            # Position was not found
            return None
        else:
            # Update position in database with new information
            current_position -= new_position

            if current_position.numShares > 0:
                self.c.execute(
                    "UPDATE positions SET shares=?, avgCost=?, totalInvestment=?, expectedEarnings=? WHERE symbol=?", (
                        int(current_position.numShares), float(current_position.averageCost),
                        float(current_position.totalInvestment), current_position.expectedEarningsDate,
                        str(current_position.symbol)))
            else:
                self.c.execute("DELETE FROM positions WHERE symbol=?", (current_position.symbol,))

        self.conn.commit()

    def update_position(self, position):
        """
        Update number of shares for a given symbol

        Parameters
        ----------
        position : Position
            Stock position being updated
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
        Retrieve information from database on the symbol given

        Parameters
        ----------
        sym : str
            Symbol of desired position

        Returns
        -------
        Position
            Position information for given symbol if found, none if no position held
        """

        self.c.execute('SELECT * FROM positions WHERE symbol=?', (sym,))
        row = self.c.fetchone()

        if row is None:
            return None
        else:
            return Position(row[0], row[1], row[2], row[4])

    def current_positions(self):
        """
        Finds symbols of all positions in database currently being held

        Returns
        -------
        list
            List of symbols for current positions
        """

        current_positions = []

        for row in self.c.execute('SELECT symbol FROM positions ORDER BY symbol'):
            current_positions.append(row[0])

        return current_positions

    def db_to_list(self):
        """
        Return all information in database as a list

        Returns
        -------
        list
            All information for all positions in portfolio database
        """
        # TODO: Change name to db_to_list

        return_positions = []

        for row in self.c.execute('SELECT * FROM positions ORDER BY symbol'):
            pos = Position(row[0], row[1], row[2], row[4])
            return_positions.append(pos)

        return return_positions

    def __del__(self):
        """
        Close the connection to the database
        """

        self.conn.close()
