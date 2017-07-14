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

import unittest

import mock

from nagiosunity.lib import utils
from nagiosunity.tests.lib import fake


class UtilsTest(unittest.TestCase):
    def test_byte_to_GiB(self):
        size_gb = utils.byte_to_GiB(1024 * 1024 * 1024)
        self.assertEqual(1, size_gb)

    def test_byte_to_GB(self):
        size_gb = utils.byte_to_GB(1000 * 1000 * 1000)
        self.assertEqual(1, size_gb)

    def test_get_single_status_ok(self):
        obj = mock.Mock()
        obj.health.value.value = (5, "OK")
        self.assertEqual(0, utils.get_single_status(obj))

    def test_get_single_status_warning(self):
        obj = mock.Mock()
        obj.health.value.value = (10, "WARNING")
        self.assertEqual(1, utils.get_single_status(obj))

    def test_get_single_status_critical(self):
        obj = mock.Mock()
        obj.health.value.value = (25, "CRITICAL")
        self.assertEqual(2, utils.get_single_status(obj))

    def test_get_single_status_unknown(self):
        obj = mock.Mock()
        obj.health.value.value = (0, "Unknown")
        self.assertEqual(3, utils.get_single_status(obj))

    def test_get_single_status_error(self):
        obj = mock.Mock()
        obj.health.value.value = (2, "Unknown")
        self.assertRaises(ValueError, utils.get_single_status, obj)

    def test_get_status_mark(self):
        status = utils.get_status_mark("DISK", 0)
        self.assertEqual("DISK OK: ", status)

    def test_print_if_failure(self):
        items = [fake.FakeUnityObject(_id='sv_2', _code=1),
                 fake.FakeUnityObject(_id='sv_3', _code=1)]
        status_code = [(1, 'sv_1'), (1, 'sv_3')]
        r = utils.print_if_failure(status_code, items)
        self.assertEqual(1, r)

    def test_print_enum(self):
        e = mock.Mock()
        e.description = "hello"
        r = utils.format_enum(e)
        self.assertEqual(r, "hello")
