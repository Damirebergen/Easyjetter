#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `easyjetter` package."""


import unittest
from unittest import mock
from easyjetter.utils import check_prices

from selenium import webdriver

class TestWebRequester(unittest.TestCase):
    """Tests for `easyjetter` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_testing(self):
        """Test testing."""
        assert 0 == 0

    # def test_001_driver_setup(self):
    # 	webrequester = check_prices.WebRequester('http://www.nu.nl')

    @mock.patch('easyjetter.utils.check_prices.webdriver')
    def test_002_driver_setup_mocked(self,mock_webdriver):
    	"""Test get is called once in selenium"""
    	webrequester = check_prices.WebRequester(' ')
    	webrequester.driver.get.assert_called_once()

    @mock.patch('easyjetter.utils.check_prices.webdriver')
    def test_003_driver_get_correct_vars(self, mock_webdriver):
    	"""Test get is called correctly in selenium"""
    	webrequester = check_prices.WebRequester('abc')
    	webrequester.driver.get.assert_called_with('abc')

    @mock.patch('easyjetter.utils.check_prices.webdriver')
    def test_004_fill_box(self,mock_webdriver):
        webrequester = check_prices.WebRequester('abc')
        webrequester.fill_box('destination', 'AMS')
        webrequester.fill_box
