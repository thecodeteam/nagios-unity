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


class IoModule(unity.UnityWrapper):
    name = 'io_module'

    def __init__(self, options, **kwargs):
        super(IoModule, self).__init__(options)
        self.options = options
        self.kwargs = kwargs
        self._modules = None

    @property
    def io_modules(self):
        return self._modules if self._modules else self.unity.get_io_module()

    def check(self):
        all_status = ok, warning, critical, unknown = utils.get_all_status(
            self.io_modules)
        code = utils.max_if_not_empty(ok + warning + critical + unknown,
                                      key=lambda i: i[0])
        code = code[0]
        status_mark = utils.get_status_mark("IO MODULE", code)
        first_line = "Total io modules #{}, Failed modules: {}".format(
            len(ok + warning + critical + unknown), [c[1] for c in critical])
        # Status line
        print(status_mark + first_line + " | ")

        # Failed details
        utils.print_if_failure(all_status[code], self.io_modules)
        return code
