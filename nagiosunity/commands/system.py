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

import logging
from nagiosunity.lib import unity
from nagiosunity.lib import utils

_log = logging.getLogger(__name__)


class System(unity.UnityWrapper):
    name = 'system'

    def __init__(self, options, **kwargs):
        super(System, self).__init__(options)
        self.options = options
        self.kwargs = kwargs
        self._licenses = None

    @property
    def licenses(self):
        if not self._licenses:
            self._licenses = self.unity.get_license()
        return self._licenses

    def check(self):
        code = 0
        status_mark = utils.get_status_mark("SYSTEM", code)
        first_line = "Name: {}, MODEL: {}, VERSION: {}".format(
            self.unity.name, self.unity.model, self.unity.system_version)
        # Status line
        print(status_mark + first_line + " | ")

        # Performance detail
        for license in self.licenses:
            print("{}: Status={}, Reason={}".format(
                license.name, self.__class__.get_license_status(license),
                (None if not license.feature.reason
                 else license.feature.reason.description)
            ))
        return code

    @staticmethod
    def get_license_status(license):
        if license.feature:
            return license.feature.state.name
