#!/usr/bin/python3

import datetime
import re

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


class DataGatherer:
    def get_expected_earnings(self, symbol):
        """
        Search webpage for earnings on given stock symbol

        Parameters
        ----------
        symbol : str
            Symbol of stock we need information on

        Returns
        -------
        datetime
            Date of expected earnings in datetime format if found, None if no
            earnings date is found
        """

        # Webpage format for each stock symbol
        earnings_url = "https://www.nasdaq.com/earnings/report/" + symbol

        earnings_soup = self.get_soup(earnings_url)

        data_string = earnings_soup.find(id="two_column_main_content_reportdata")

        # Find date in string found using regex
        match = re.search(r'\d{2}/\d{2}/\d{4}', data_string.text)

        if match is not None:
            date = datetime.datetime.strptime(match.group(), '%m/%d/%Y').date()
        else:
            return None

        return date

    def get_soup(self, url):
        """
        Grabs source html of for the given webpage

        Parameters
        ----------
        url : str
            Url of webpage we want html for

        Returns
        -------
        soup
            Soup for desired webpage
        """

        try:
            page = requests.get(url, timeout=5)
        except RequestException as e:
            print(e)
            return None

        soup = BeautifulSoup(page.content, 'html.parser')

        return soup
