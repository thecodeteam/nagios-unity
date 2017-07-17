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

_log = logging.getLogger(__name__)


class Options(object):
    def __init__(self, options):
        _log.debug(options)
        self.data = options

    @property
    def cacert(self):
        if self.data.get('--cacert'):
            return self.data.get('<CACERT>')
        # Returns False to avoid ssl check
        return False

    @property
    def verbose(self):
        return self.data.get('--verbose')

    @property
    def command(self):
        command = self.data.get('<OBJECT>', None)
        if command:
            return command
        return None

    @property
    def host(self):
        return self.data.get('<HOST>', '')

    @property
    def username(self):
        return self.data.get('<USERNAME>', '')

    @property
    def password(self):
        return self.data.get('<PASSWORD>', '')
