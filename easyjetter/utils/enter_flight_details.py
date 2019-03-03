# -*- coding: utf-8 -*-

"""Check the price of a flight on easyjet site."""
from selenium import webdriver
import time

class WebHandler:
	def __init__(self, startpage, destination, origin,
				depart_date, return_date, driver=None):

		#if we dont get a driver, start a new one.
		if driver == None:
			self.driver = webdriver.Chrome()
		else:
			self.driver = driver
		# go the the startpage
		self.driver.get(startpage)
		self.submit_button_type = "search-submit"

	def fill_fields(self):
		self.fill_box("destination", destination)
		self.fill_box("origin",origin)
		print('Set depart date')
		self.set_date(depart_date ,Depart=True)
		print('Set return date')
		self.set_date(return_date ,Depart=False)
		self.click_submit_button()
		# import pdb; pdb.set_trace()

	def fill_box(self,name,message):
		box = self.driver.find_element_by_name(name)
		# emptybox
		box.clear()
		# send message to box
		box.send_keys(message)
		return box

	def set_date(self, date, Depart=True):
		if Depart:
			class_name = "outbound-date-picker"
			calender_div = "Date Calendar Outbound"
		else:
			class_name = "return-date-picker"
			calender_div = "Date Calendar Return"

		date_box = self.driver.find_element_by_class_name(class_name)
		date_box_button = date_box.find_element_by_class_name("date-picker-button")
		date_box_button.click()
		time.sleep(2)
		calender = self.find_correct_calender(calender_div)
		correct_date = self.find_correct_date(date, calender)
		correct_date.find_element_by_class_name("selectable").click()
		time.sleep(1)
		# correct_date.click()
		if Depart:
			self.driver.find_element_by_id("close-drawer-link").click()
		time.sleep(1)

	def find_correct_date(self, date, calender):
		dates = calender.find_elements_by_class_name("day")
		for day in dates:
			# print(day.get_attribute("data-date"))
			if day.get_attribute("data-date") == date:
				return day
		raise AttributeError ("day not found on page, \
				is the date valid? example 2019-03-13")

	def find_correct_calender(self, div):
		cals = self.driver.find_elements_by_class_name('drawer-tab-content')
		for cal in cals:
			if cal.get_attribute('data-tab') == div:
				print('found calender')
				return cal
		raise AttributeError('div class not found in the calendars')

	def click_submit_button(self, css_class_name=None):
		if css_class_name == None:
			css_class_name = self.submit_button_type
		sub_button = self.driver.find_element_by_class_name(css_class_name)
		sub_button.click()
		return sub_button


if __name__ == '__main__':
	wh = WebHandler('http://www.easyjet.com/en/', "AMS", "LGW", "2019-03-13", "2019-03-15")
