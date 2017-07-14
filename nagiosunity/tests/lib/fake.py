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

import mock


class FakeUnity(object):
    def __init__(self):
        pass

    def get_battery(self):
        return [FakeUnityObject('bt_1', 5)]

    def get_dae(self):
        return [FakeUnityObject('dae_1', 7, name='dae 1', current_power=151,
                                avg_power=11, max_power=13,
                                current_temperature=100, avg_temperature=10,
                                max_temperature=133,
                                current_speed=1000 * 1000 * 1000,
                                max_speed=1000 * 1000 * 1000)]

    def get_dpe(self):
        return [FakeUnityObject('dpe_1', 7, name='dpe 1', current_power=151,
                                avg_power=11, max_power=13,
                                current_temperature=100, avg_temperature=10,
                                max_temperature=133,
                                current_speed=1000 * 1000 * 1000,
                                max_speed=1000 * 1000 * 1000)]

    def get_disk(self):
        return [FakeUnityObject('disk_1', 7),
                FakeUnityObject('disk_2', 5),
                FakeUnityObject('disk_3', 7)]

    def get_disk_group(self):
        return [
            FakeUnityObject('dg_1', 7, unconfigured_disks=1, total_disks=10,
                            min_hot_spare_candidates=1),
            FakeUnityObject('dg_2', 5, unconfigured_disks=2, total_disks=2)]

    def get_ethernet_port(self):
        return [
            FakeUnityObject('eth_1', 7, name="Ethernet Port 1",
                            is_link_up=True,
                            requested_speed=FakeEnum(0, "Auto"),
                            speed=FakeEnum(1000, "Auto")),
            FakeUnityObject('eth_2', 7, name="Ethernet Port 2",
                            is_link_up=True,
                            requested_speed=FakeEnum(0, "Auto"),
                            speed=FakeEnum(1000, "Auto")),
            FakeUnityObject('eth_3', 25, name="Ethernet Port 3",
                            is_link_up=False,
                            requested_speed=FakeEnum(0, "Auto"),
                            speed=FakeEnum(1000, "Auto"))
        ]

    def get_fan(self):
        return [
            FakeUnityObject('fan_1', 7, name='Fan 1'),
            FakeUnityObject('fan_2', 7, name='Fan 2'),
            FakeUnityObject('fan_3', 5, name='Fan 3')
        ]

    def get_io_module(self):
        return [
            FakeUnityObject('io_1', 7, name='IO 1'),
            FakeUnityObject('io_2', 7, name='IO 2'),
            FakeUnityObject('io_3', 5, name='IO 3')
        ]

    def get_lcc(self):
        return [
            FakeUnityObject('lcc_1', 7, name='lcc 1')
        ]

    def get_lun(self):
        return [
            FakeUnityObject('sv_1', 7, name='LUN 1'),
            FakeUnityObject('sv_2', 7, name='LUN 2'),
            FakeUnityObject('sv_3', 5, name='LUN 3')
        ]

    def get_fc_port(self):
        return [
            FakeUnityObject('fc_port_1', 7, name="FC Port 1", is_link_up=True,
                            requested_speed=FakeEnum(0, "Auto"),
                            current_speed=FakeEnum(1000, "Auto")),
            FakeUnityObject('fc_port_2', 7, name="FC Port 2", is_link_up=True,
                            requested_speed=FakeEnum(0, "Auto"),
                            current_speed=FakeEnum(1000, "Auto")),
            FakeUnityObject('fc_port_3', 15, name="FC Port 3",
                            is_link_up=False,
                            requested_speed=FakeEnum(0, "Auto"),
                            current_speed=FakeEnum(1000, "Auto"))
        ]

    def get_memory_module(self):
        return [
            FakeUnityObject('spa_mm_3', 7, name='SP A Memory Module 3'),
            FakeUnityObject('spb_mm_4', 5, name='SP B Memory Module 4'),
        ]

    def get_pool(self):
        return [
            FakeUnityObject('pool_1', 7, name='nagios-pool',
                            size_total=2556310847488,
                            size_free=2456721293312)
        ]

    def get_power_supply(self):
        return [
            FakeUnityObject('dpe_ps_a0', 7, name='DPE Power Supply A0'),
            FakeUnityObject('dpe_ps_b0', 7, name='DPE Power Supply B0')
        ]

    def get_sas_port(self):
        return [
            FakeUnityObject('spb_sas1', 7, name='SP B SAS Port 1',
                            current_speed=FakeEnum(3, "3Gbps"))
        ]

    def get_sp(self):
        return [
            FakeUnityObject('spa', 7, name='SP A', is_rescue_mode=False,
                            bios_firmware_revision='50.78',
                            post_firmware_revision='29.80',
                            needs_replacement=False),
            FakeUnityObject('spb', 7, name='SP B', is_rescue_mode=False,
                            bios_firmware_revision='50.78',
                            post_firmware_revision='29.80',
                            needs_replacement=False),

        ]

    def get_ssc(self):
        return [
            FakeUnityObject('', 7, name='')
        ]

    def get_ssd(self):
        return [
            FakeUnityObject('spa_ssd', 7, name='SP A Internal Disk'),
            FakeUnityObject('spb_ssd', 7, name='SP B Internal Disk')
        ]

    def get_license(self):
        return [
            FakeUnityObject('ANTIVIRUS', 7, name='ANTIVIRUS',
                            feature=FakeUnityObject(
                                'ANTIVIRUS', 7,
                                name='ANTIVIRUS',
                                reason=FakeEnum(description=""),
                                state=FakeEnum(2, "FeatureStateEnabled",
                                               "Enabled"))),
            FakeUnityObject('BASE_OE_V4_0', 7, name='BASE_OE_V4_0',
                            feature=FakeUnityObject(
                                'BASE_OE_V4_0', 7,
                                name='BASE_OE_V4_0',
                                reason=FakeEnum(description=""),
                                state=FakeEnum(2, "FeatureStateEnabled",
                                               "Enabled"))
                            )]

    @property
    def name(self):
        return "FNM00150600267"

    @property
    def model(self):
        return "Unity 500"

    @property
    def system_version(self):
        return "4.2.0"


class FakeUnityObject(object):
    def __init__(self, _id=None, _code=None, **kwargs):
        """Initialize the properties for the Unity object.

        :param _id: the id of object
        :param _code: health code for state check
        :param kwargs: dict to populate any other properties
        """
        self._id = _id
        self._code = _code
        self.props = kwargs

    @property
    def id(self):
        return self._id

    @property
    def code(self):
        return self._code

    @property
    def health(self):
        m = mock.Mock()
        m.value.value = (self.code, "status")
        m.descriptions = ["d1", "d2"]
        return m

    def __getattr__(self, item):
        if item in self.props:
            return self.props[item]
        raise AttributeError(
            "'FakeUnityObject' object has no attribute '%s'" % item)


class FakeEnum(object):
    def __init__(self, index=None, description=None, name=None):
        self.index = index
        self.description = description
        self.name = name


class FakeStorops(object):
    pass
