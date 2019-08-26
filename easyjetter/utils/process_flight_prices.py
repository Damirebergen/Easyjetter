"""Check the price of a flight on easyjet site."""

import time
from datetime import datetime, timedelta
import psycopg2


class DataHandler:
    def __init__(self, Prices, depart, arrival):
        """ Handles all the actions needed to get the desired info off of the price page
        Args:
            Prices: dict
               output from grab flight prices
        Returns:
            None
        """
        # depart and return
        # dict with direction as key and flights(list) as value
        for direction, flights in Prices.items():
            if direction == 'depart':
                from_to = '_'.join((depart, arrival))
            elif direction == 'retour':
                from_to = '_'.join((arrival, depart))
            for flight in flights:
                flight_date = self.date_year_guesser(flight[0])
                UUID = '{}_{}'.format(from_to, flight_date)
                
                print((UUID, flight))
                # TODO: 
                # - setup postgress 
                #       - flights table
                #       - flight_price_table
                # - lookup id of UUID in flights table
                #  submit to it in flight_price_table
                #

        # print(self.date_year_guesser(Prices[ "depart"][0][0]))
        # print(self.date_year_guesser("Thursday 12th March, 06:05."))

    def date_year_guesser(self, easyjetdatestring):
        # read the following string format while guessing the year by assuming its in the future
        # Thursday 12th December, 06:05

        # get the current year
        current_year = datetime.today().year
        # and next year
        next_year = current_year + 1
   
        # make guesses as strings
        current_year_guess = '{} {}'.format(current_year, easyjetdatestring)
        next_year_guess = '{} {}'.format(next_year, easyjetdatestring)

        # read stings into datetime elements
        current_year_guess = datetime.strptime(current_year_guess, '%Y %A %dth %B, %H:%M.')
        next_year_guess = datetime.strptime(next_year_guess, '%Y %A %dth %B, %H:%M.')

        #check if current year is in the future
        if current_year_guess - datetime.now() > timedelta(seconds = 0):
            year_guess = current_year_guess
        # else check if next year is in the future
        elif next_year_guess - datetime.now() > timedelta(seconds = 0):
            year_guess = next_year_guess
        # else we dont know whats gooing on
        else:
            raise ValueError('date_year_guesser could not guess the propper year')

        # return as a string in the iso standard format
        return year_guess.isoformat()

if __name__ == "__main__":
    example_dict  = {
    "depart": [
        (
            "Thursday 12th December, 06:05.",
            "Thursday 12th December, 08:35.",
            "£34.99",
            "8",
        ),
        (
            "Thursday 12th December, 08:00.",
            "Thursday 12th December, 10:30.",
            "£34.99",
            "2",
        ),
        (
            "Thursday 12th December, 18:35.",
            "Thursday 12th December, 20:50.",
            "£34.99",
            "8",
        ),
        (
            "Thursday 12th December, 20:05.",
            "Thursday 12th December, 22:25.",
            "£34.99",
            "8",
        ),
        ("Friday 13th December, 06:05.", "Friday 13th December, 08:35.", "£54.99", "6"),
        ("Friday 13th December, 08:00.", "Friday 13th December, 10:30.", "£51.99", "4"),
        ("Friday 13th December, 08:55.", "Friday 13th December, 11:15.", "£51.99", "7"),
    ],
    "retour": [
        (
            "Saturday 14th December, 07:05.",
            "Saturday 14th December, 07:20.",
            "£38.99",
            "4",
        ),
        (
            "Saturday 14th December, 09:10.",
            "Saturday 14th December, 09:25.",
            "£28.99",
            "1",
        ),
        ("Sunday 15th December, 07:05.", "Sunday 15th December, 07:20.", "£31.99", "8"),
        ("Sunday 15th December, 11:50.", "Sunday 15th December, 12:05.", "£55.99", "8"),
    ],
    }

    WebHandler(example_dict, "AMS", "LGW")
