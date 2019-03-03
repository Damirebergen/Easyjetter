#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `easyjetter` package."""


import unittest
from unittest import mock
from easyjetter.utils import enter_flight_details

from selenium import webdriver

class TestWebHandler(unittest.TestCase):
    """Tests for `easyjetter` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_testing(self):
        """Test testing."""
        assert 0 == 0

    @mock.patch('easyjetter.utils.enter_flight_details.webdriver')
    def test_001_driver_setup_mocked(self,mock_webdriver):
        """Test get is called once in selenium and with right link"""
        wh = enter_flight_details.WebHandler('htmllink','ABC', 'BCD',"13", "15")
        wh.driver.get.assert_called_once()
        wh.driver.get.assert_called_with('htmllink')

    @mock.patch('easyjetter.utils.enter_flight_details.webdriver')
    def test_002_fill_box(self,mock_webdriver):
        wh = enter_flight_details.WebHandler('htmllink','ABC', 'BCD',"13", "15")
        mock_box = wh.fill_box('destination', 'abc')
        wh.driver.find_element_by_name.assert_called_once()
        wh.driver.find_element_by_name.assert_called_with('destination')
        #check the returned box is called correctly
        mock_box.clear.assert_called_once()
        mock_box.send_keys.assert_called_with('abc')
