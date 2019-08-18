import pytest
from Position import Position

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
    assert True


def test_sell_shares():
    assert True
