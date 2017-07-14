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
import logging
from nagiosunity.lib import unity
from nagiosunity.lib import utils

_log = logging.getLogger(__name__)


class Ssd(unity.UnityWrapper):
    name = 'ssd'

    def __init__(self, options, **kwargs):
        super(Ssd, self).__init__(options)
        self.options = options
        self.kwargs = kwargs
        self._ssds = None

    @property
    def ssds(self):
        return self._ssds if self._ssds else self.unity.get_ssd()

    def check(self):
        code = 0
        all_status = ok, warning, critical, unknown = utils.get_all_status(
            self.ssds)
        if len(self.ssds):
            code = max(ok + warning + critical + unknown, key=lambda i: i[0])
            code = code[0]
        status_mark = utils.get_status_mark("SSD", code)
        first_line = "Total SSDs #{}, Failed SSDs: {}".format(
            len(ok + warning + critical + unknown), [c[1] for c in critical])
        # Status line
        print(status_mark + first_line + " | ")

        # Failed details
        utils.print_if_failure(all_status[code], self.ssds)
        return code
