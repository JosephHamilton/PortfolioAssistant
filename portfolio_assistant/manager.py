from __future__ import print_function

import os.path
import pickle
import re

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from portfolio_assistant.assistant import Portfolio

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
my_portfolio = Portfolio()


def main():
    """
    Main method for program.  Runs every night to check for new stocks purchased
    or sold and adds the expected earnings date.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API to get order execution messages
    results = service.users().messages().list(userId='me', q='subject:order').execute()
    messages = results.get('messages', [])

    if not messages:
        print('No Messages Found')
    else:
        for message in messages:
            snippet = service.users().messages().get(userId='me', id=message['id'], format='minimal').execute()[
                'snippet']
            if "share" in snippet:
                scrape_shares_order(snippet)
            elif "contract" in snippet:
                scrape_options_order(snippet)

    my_portfolio.update_expected_earnings()
    my_portfolio.print()


def scrape_shares_order(string):
    """
    Gather details about shares purchased from brokerage emails and add to my portfolio.
    :param string: body of email given as string
    """

    # Using regex to scrape email
    p = re.compile("to (.*) (.*) shares? of (.*) was executed at an average price of (.*) on")
    order_info = p.findall(string)[0]
    order_type = order_info[0]
    num_shares = order_info[1]
    symbol = order_info[2]
    price_per_share = order_info[3][1:]

    if order_type == "buy":
        my_portfolio.add_position(symbol, int(num_shares), float(price_per_share))
    elif order_type == "sell":
        my_portfolio.sell_position(symbol, int(num_shares), float(price_per_share))


def scrape_options_order(string):
    """
    Gather details about options contracts purchased from brokerage emails
    :param string: body of email given as string
    """

    # Using regex to scrape email
    p = re.compile("to (.*) (.*) contracts? of (.*) (.*) (.*) (.*) executed at an average price of (.*) for")
    order_info = p.findall(string)[0]
    order_type = order_info[0]
    num_contracts = order_info[1]
    symbol = order_info[2]
    strike_price = order_info[3][1:]
    contract_type = order_info[4]
    exp_date = order_info[5]
    price_per_contract = order_info[6][1:]

    if order_type == "buy":
        # print("Buying contract")
        # my_portfolio.add_position(symbol, int(num_shares), float(price_per_share))
        pass
    elif order_type == "sell":
        # print("Selling contract")
        # my_portfolio.sell_position(symbol, int(num_shares), float(price_per_share))
        pass


if __name__ == '__main__':
    main()
