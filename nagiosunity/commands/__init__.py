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

from nagiosunity.commands import battery, sas_port, system, sp, pool, lcc, \
    memory_module, power_supply, ssc, ssd, lun, dpe
from nagiosunity.commands import disk
from nagiosunity.commands import dae
from nagiosunity.commands import ethernet_port
from nagiosunity.commands import fan
from nagiosunity.commands import fc_port
from nagiosunity.commands import io_module

COMMANDS = [battery.Battery,
            disk.Disk,
            ethernet_port.EthernetPort,
            fc_port.FcPort,
            sas_port.SasPort,
            system.System,
            sp.StorageProcessor,
            pool.Pool,
            dae.Dae,
            dpe.Dpe,
            io_module.IoModule,
            lcc.Lcc,
            memory_module.MemoryModule,
            fan.Fan,
            power_supply.PowerSupply,
            battery.Battery,
            ssc.Ssc,
            ssd.Ssd,
            lun.Lun]

commands_dict = {cmd.name: cmd for cmd in COMMANDS}
