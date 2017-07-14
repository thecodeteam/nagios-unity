# coding=utf-8
# Copyright (c) 2017 Dell Inc. or its subsidiaries.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from nagiosunity.cli import opt

import unittest


class OptionTest(unittest.TestCase):
    def test_option(self):
        my_opt = opt.Options({
            '<HOST>': '192.168.1.30',
            '<USERNAME>': 'admin',
            '<PASSWORD>': 'password',
            '<OBJECT>': 'disk',
            '--verbose': True,
            '<verbose>': True,
            '--warning': True,
            '<warning>': 123,
            '--critical': True,
            '<critical>': 124})
        self.assertEqual("192.168.1.30", my_opt.host)
        self.assertEqual('admin', my_opt.username)
        self.assertEqual('password', my_opt.password)
        self.assertEqual("disk", my_opt.command)
        self.assertEqual(True, my_opt.verbose)
        self.assertEqual(123, my_opt.warning)
        self.assertEqual(124, my_opt.critical)
