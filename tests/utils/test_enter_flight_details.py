#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `easyjetter` package."""


import unittest
from unittest import mock
from easyjetter.utils import enter_flight_details

import selenium

class TestWebHandler(unittest.TestCase):
    """Tests for `easyjetter` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_testing(self):
        """Test testing."""
        self.assertEqual(0, 0)

    @mock.patch("selenium.webdriver.Chrome")
    def test_001_driver_setup_mocked(self, mock_webdriver):
        """Test get is called once in selenium and with right link"""
        wh = enter_flight_details.WebHandler("htmllink", "ABC", "BCD", "13", "15")
        wh.driver.get.assert_called_once_with("htmllink")

    @mock.patch("selenium.webdriver.Chrome")
    def test_002_fill_box(self, mock_webdriver):
        """Test that the textbox filler calls selenium as intended"""
        wh = enter_flight_details.WebHandler("htmllink", "ABC", "BCD", "13", "15")
        mock_box = wh.fill_box("destination", "abc")
        wh.driver.find_element_by_name.assert_called_once_with("destination")
        # check the returned box is called correctly
        # mock_box.clear.assert_called_once()
        mock_box.send_keys.assert_called_once_with("abc")

    @mock.patch("selenium.webdriver.Chrome")
    def test_003_click_submit_button(self, mock_webdriver):
        """Test that the submit button calls selenium as intended"""
        wh = enter_flight_details.WebHandler("http", "ABC", "BCD", "13", "15")
        response = wh.click_submit_button()
        # is the buton looked for with the default?
        # wh.driver.find_element_by_class_name.assert_called_once()
        wh.driver.find_element_by_class_name.assert_called_once_with("search-submit")
        response.click.assert_called_once()

    @mock.patch("selenium.webdriver.Chrome")
    def test_004_find_correct_calendar(self, mock_webdriver):
        wh = enter_flight_details.WebHandler("http", "ABC", "BCD", "13", "15")
        # setup responses
        cor_atr = {"get_attribute.return_value": "A"}
        correct = mock.Mock(**cor_atr)
        bad_atr = {"get_attribute.return_value": "B"}
        bad = mock.Mock(**bad_atr)
        # let the driver return the above mocks so we can test the atribute calling
        wh.driver.find_elements_by_class_name.return_value = [bad, correct]
        # find the calendar
        response = wh.find_correct_calendar("A")
        # assert the output
        bad.get_attribute.assert_called_once_with("data-tab")
        correct.get_attribute.assert_called_once_with("data-tab")
        self.assertEqual(response, correct)
        # test that it raises an error when the correct calendar cannot be found
        wh.driver.find_elements_by_class_name.return_value = [bad, bad]
        self.assertRaises(AttributeError, wh.find_correct_calendar, "A")

    def test_005_find_correct_date(self):
        pass
