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

from ddt import ddt, data, unpack

from nagiosunity import commands
from nagiosunity.tests import utils

result_dict = {'battery': 0, 'dae': 0, 'disk': 0, 'dpe': 0, 'ethernet_port': 2,
               'fan': 0, 'fc_port': 1, 'io_module': 0, 'lcc': 0, 'lun': 0,
               'memory_module': 0, 'pool': 0, 'power_supply': 0, 'sas_port': 0,
               'sp': 0, 'ssc': 0, 'ssd': 0, 'system': 0}


@ddt
class CommandsTest(unittest.TestCase):
    @unpack
    @data(*commands.commands_dict.items())
    @utils.patch_unity
    def test_check(self, name, command):
        if name not in result_dict:
            return self.skipTest(
                "Please specify the expected result in result_dict.")
        c = command(options={})
        r = c.check()
        self.assertEqual(result_dict[name], r,
                         "Assert failed for {}".format(name))
