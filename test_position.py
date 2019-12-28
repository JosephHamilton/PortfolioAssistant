import pytest
from portfolio_assistant.portfolio import Position


@pytest.mark.parametrize("test_input, expected",
                    [
                        (Position('AAPL'), 'AAPL(num_shares=0, average_cost=0, expected_earnings=None)'),
                        (Position('AAPL', num_shares=20),
                         'AAPL(num_shares=20, average_cost=0, expected_earnings=None)'),
                        (Position('AAPL', num_shares=60, average_cost=30),
                         'AAPL(num_shares=60, average_cost=30, expected_earnings=None)'),
                        (Position('AAPL', average_cost=2.22),
                         'AAPL(num_shares=0, average_cost=2.22, expected_earnings=None)'),

                    ]
)
def test_repr(test_input, expected):
    assert repr(test_input) == expected


def test_buy_shares():
    position = Position('AAPL', num_shares=60, average_cost=30)

    # Check position has the right information
    assert position.symbol == 'AAPL'
    assert position.numShares == 60
    assert position.averageCost == 30
    assert position.totalInvestment == 1800
    assert position.expectedEarningsDate is None

    # Buy 60 new shares with an average cost of $60
    position.buy_shares(60, 60)

    # Check that position updated properly
    assert position.symbol == 'AAPL'
    assert position.numShares == 120
    assert position.averageCost == 45
    assert position.totalInvestment == 5400
    assert position.expectedEarningsDate is None


def test_sell_shares():
    position = Position('AAPL', num_shares=60, average_cost=30)

    # Check position has the right information
    assert position.symbol == 'AAPL'
    assert position.numShares == 60
    assert position.averageCost == 30
    assert position.totalInvestment == 1800
    assert position.expectedEarningsDate is None

    # Sell 30 shares at an average price of $45
    position.sell_shares(30, 45)

    # Check that position updated properly
    assert position.symbol == 'AAPL'
    assert position.numShares == 30
    assert position.averageCost == 30
    assert position.totalInvestment == 900
    assert position.expectedEarningsDate is None

