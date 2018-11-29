#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import zoomeye


class ZoomeyeTest(unittest.TestCase):

    def setUp(self):
        self.zm = zoomeye.ZoomEye()

    def test_zoomeye_login_api(self):
        value = 'https://api.zoomeye.org/user/login'
        self.assertEqual(self.zm.zoomeye_login_api, value)

    def test_zoomeye_dork_api(self):
        value = 'https://api.zoomeye.org/{}/search'
        self.assertEqual(self.zm.zoomeye_dork_api, value)

    def test_login(self):
        self.assertEqual(self.zm.login(), self.zm.token)

    def test_dork_search(self):
        value = 'zoomeye invalid dork'
        self.assertEqual(self.zm.dork_search(value), [])

    def test_resources_info(self):
        self.assertEqual(self.zm.resources_info(), None)

    def dearDwon(self):
        del self.zm


if __name__ == '__main__':
    unittest.main()
