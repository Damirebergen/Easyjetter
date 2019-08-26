# -*- coding: utf-8 -*-

"""Check the price of a flight on easyjet site."""
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
from loguru import logger

class WebHandler:
    def __init__(self, driver=None):
        """ Handles all the actions needed to get the desired info off of the price page
        Args:
               driver (class): selenium driver to use.
        Returns:
            None
        """
        # if we dont get a driver (browser), start a new one.
        if driver == None:
            raise ChildProcessError('Needs to be given a driver on the prices page')
        else:
            self.driver = driver

        # seperate the departure and return flights
        flight_prices_direction = {}
        for direction, flightfunnel in zip(
            ["depart", "retour"],
            self.driver.find_elements_by_class_name("funnel-flight"),
        ):
            logger.info("next funnel")
            flight_prices_direction[direction] = self.flight_funnel_processor(
                flightfunnel
            )
        logger.trace(flight_prices_direction)
        self.flight_prices = flight_prices_direction

    def flight_funnel_processor(
        self, flight_funnel, flight_funnel_target="flight-grid-flight-body"
    ):
        # css class names:
        time_class = "full-time"
        seat_class = "data-lowest-fare-seats-available"
        price_class = "price-container"

        # output
        direction_list = []

        # find all the flight boxes to get info from
        for flight_box in flight_funnel.find_elements_by_class_name(
            flight_funnel_target
        ):
            # depart time is always first
            depart_time = flight_box.find_elements_by_class_name(time_class)[
                0
            ].get_attribute("innerHTML")
            # seccond appearence is arrival time
            arrival_time = flight_box.find_elements_by_class_name(time_class)[
                1
            ].get_attribute("innerHTML")
            # price can be found in an hidden span of a div with class price container
            price = (
                flight_box.find_element_by_class_name(price_class)
                .find_element_by_class_name("access-hidden")
                .get_attribute("innerHTML")
            )
            # we can also find the available seats for the given price
            seats_at_price = flight_box.find_element_by_class_name(
                "flight-grid-flight-fare"
            ).get_attribute(seat_class)

            logger.debug(
                "\t{} for {} for {} seat remaining ".format(
                    depart_time, price, seats_at_price
                )
            )
            # add as a tuple to the directionlist
            direction_list.append((depart_time, arrival_time, price, seats_at_price))
        return direction_list


if __name__ == "__main__":
    pass
