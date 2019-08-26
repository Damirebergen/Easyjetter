# -*- coding: utf-8 -*-

"""Main module."""
from loguru import logger

import utils.enter_flight_details as fly_details
import utils.grab_flight_prices as grab_prices
import utils.process_flight_prices as process_prices

if __name__ == "__main__":
    source = "AMS"
    destination = "LGW"
    logger.info('enter_flight_details')

    wh = fly_details.WebHandler(
        "http://www.easyjet.com/en/", "AMS", "LGW", "2019-12-13", "2019-12-15"
    )
    logger.info('extract prices')
    Prices = grab_prices.WebHandler(driver = wh.driver)
    logger.info("process prices")
    data = process_prices.DataHandler(Prices.flight_prices,"AMS", "LGW")

    logger.info('back in main')

# driver.switch_to.window(driver.window_handles[1])
