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

from __future__ import division

from nagiosunity.lib import unity
from nagiosunity.lib import utils
from nagiosunity.commands import battery
from nagiosunity.commands import dae
from nagiosunity.commands import disk
from nagiosunity.commands import dpe
from nagiosunity.commands import ethernet_port
from nagiosunity.commands import fan
from nagiosunity.commands import fc_port
from nagiosunity.commands import io_module
from nagiosunity.commands import lcc
from nagiosunity.commands import memory_module
from nagiosunity.commands import power_supply
from nagiosunity.commands import sas_port
from nagiosunity.commands import sp
from nagiosunity.commands import ssc
from nagiosunity.commands import ssd
from nagiosunity.commands import system

import sys

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO


class ArrayHardware(unity.UnityWrapper):
    name = 'array_hardware'

    def __init__(self, options, **kwargs):
        super(ArrayHardware, self).__init__(options)
        self.options = options
        self.kwargs = kwargs
        self._batteries = None

    @property
    def batteries(self):
        return self._batteries if self._batteries else self.unity.get_battery()

    def check(self):
        code, output = self.combined_output()

        if code == 0:
            print(utils.get_status_mark(
                "HARDWARE", code) + "All hardware work fine.")
        else:
            print(utils.get_status_mark("HARDWARE", code) +
                  "Modules with problems: " +
                  ";".join(map(lambda x: x.split()[0], output[code])) + " | ")
        print('------\n'.join(output[code]).replace("|", ""))
        return code

    def combined_output(self):
        # hold the stdout buffer
        output_dict = {0: [], 1: [], 2: [], 3: []}

        combined_objects = [battery.Battery, dae.Dae, disk.Disk, dpe.Dpe,
                            ethernet_port.EthernetPort, fan.Fan,
                            fc_port.FcPort, io_module.IoModule, lcc.Lcc,
                            memory_module.MemoryModule,
                            power_supply.PowerSupply, sas_port.SasPort,
                            sp.StorageProcessor, ssc.Ssc, ssd.Ssd,
                            system.System]
        errors = []
        for Obj in combined_objects:
            with Capturing() as stringio:
                error_code = Obj(self.options, **self.kwargs).check()
                errors.append(error_code)
                output_dict[error_code].append(stringio.getvalue())

        severity_code = max(errors)
        return severity_code, output_dict


class Capturing(object):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self._stringio

    def __exit__(self, *args):
        sys.stdout = self._stdout
