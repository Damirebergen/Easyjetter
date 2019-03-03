# -*- coding: utf-8 -*-

"""Check the price of a flight on easyjet site."""
from selenium import webdriver
import time

class WebHandler:
	def __init__(self, startpage, destination, origin,
				depart_date, return_date, driver=None):
    """handles all the actions needed to get to the price page.
    Args:
        startpage (string): http link of the page to start the driver on.
        destination (string): 3 letter code of the destination airport
        origin (string): 3 letter code of the departure airport
        depart_date (string): YYYY-MM-DD string of the departure date
        return_date (string): YYYY-MM-DD string of the arrival date
        driver (class): selenium driver to use, starts its own when none.
    Returns:
        None
    """
		#if we dont get a driver (browser), start a new one.
		if driver == None:
			self.driver = webdriver.Chrome()
		else:
			self.driver = driver
		# go the the startpage
		self.driver.get(startpage)
		# variables
		self.submit_button_type = "search-submit"
		self.destination = destination
		self.origin = origin
		self.depart_date = depart_date
		self.return_date = return_date

	def fill_fields(self):
    """Use all the self.* variables to fill the boxes on the landing package
	of Easyjet.
    Args: None
    Returns:
        None: Nothing
	TODO:
		check if inputs are sane.
    """
		self.fill_box("destination", self.destination)
		self.fill_box("origin",self.origin)
		print('Set depart date')
		self.set_date(self.depart_date ,Depart=True)
		print('Set return date')
		self.set_date(self.return_date ,Depart=False)
		self.click_submit_button()
		# wait to finish as this can take some time.
		time.sleep(5)

	def fill_box(self,name,message):
    """given the css name of a textbox enter the message into that textbox.
    Args:
        name (string): css class name of the box to enter the message in
        message (string): message to put into html text box
	Returns:
        type: selenium element object
    """
		box = self.driver.find_element_by_name(name)
		# emptybox
		box.clear()
		# send message to box
		box.send_keys(message)
		return box

	def set_date(self, date, Depart=True):
    """ Manager function to perform all the clicks to set a date on the main
	page of easyjet.
    Args:
        date (string): YYYY-MM-DD string of the date that is entered.
				e.q. "2019-03-13".
        Depart (Boolean): are we entering a departure date or a return date.
    Returns:
        type: None
    """
		# set css class names for depart or return
		if Depart:
			class_name = "outbound-date-picker"
			calendar_div = "Date Calendar Outbound"
		else:
			class_name = "return-date-picker"
			calendar_div = "Date Calendar Return"
		# find the correct date button for depart or arrival
		date_box = self.driver.find_element_by_class_name(class_name)
		date_box_button = date_box.find_element_by_class_name( \
											"date-picker-button")
		# click and wait to load
		date_box_button.click()
		time.sleep(2)
		# find the correct calendar
		calendar = self.find_correct_calendar(calendar_div)
		# find the day to click and click it
		correct_date = self.find_correct_date(date, calendar)
		correct_date.find_element_by_class_name("selectable").click()
		time.sleep(1)
		# if we are in depart the drawer doesnt close automaticly.
		# so we find the close button and click it.
		if Depart:
			self.driver.find_element_by_id("close-drawer-link").click()
		time.sleep(1)

	def find_correct_date(self, date, calendar):
    """iterates over all the divs with the css class of day.
	if the data-date attribute matches the selenium element object is
	returned.

    Args:
        date (string): YYYY-MM-DD string of the date that is looked for
				e.q. "2019-03-13".
        calendar (class): selenium object of the calander

    Returns:
        class: selenium object of the div that matched the date

    Raises:        ExceptionName: Why the exception is raised.

    """
		dates = calendar.find_elements_by_class_name("day")
		for day in dates:
			# print(day.get_attribute("data-date"))
			if day.get_attribute("data-date") == date:
				return day
		raise AttributeError ("day not found on page, \
				is the date valid? example 2019-03-13")

	def find_correct_calendar(self, tab_id):
    """iterates over all calanders with the css tag of drawer-tab-contentsself.
	if the attribute data-tab of the tab_id is equal to the data-tab attribute
	it is returned.
    Args:
        tab_id (string): css class name of the calendar tab_id you look for.
    Returns:
        class: selenium element object of the correct calander
    Raises:	AttributeError: the correct calendar has not been found.
    """
		cals = self.driver.find_elements_by_class_name('drawer-tab-content')
		for cal in cals:
			if cal.get_attribute('data-tab') == tab_id:
				print('found calendar')
				return cal
		raise AttributeError('div class not found in the calendars')


	def click_submit_button(self, css_class_name=None):
    """clicks the html object that matches the css_class_name variable,
	has a default for the easyjet submit button on the homepage.
    Args:
        css_class_name (type):  name of the css calss to look for.
		 	Defaults to None.
    Returns:
        type: selenium element object of the submit button
    """
		if css_class_name == None:
			css_class_name = self.submit_button_type
		sub_button = self.driver.find_element_by_class_name(css_class_name)
		sub_button.click()
		return sub_button


if __name__ == '__main__':
	pass
	# example to fly from amsterdam to gatwick on 13 march and terun the 15th:
	# wh = WebHandler('http://www.easyjet.com/en/', "AMS", "LGW", \
	# 				"2019-03-13", "2019-03-15")
