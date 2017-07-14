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
import functools

from nagiosunity.tests.lib import fake


def patch_unity(test_func):
    @functools.wraps(test_func)
    def patched(*args, **kwargs):
        with mock.patch(target='nagiosunity.lib.unity.UnityWrapper.unity',
                        new=fake.FakeUnity()):
            print(
                "\nOUTPUT({}.{})=======>".format(test_func.__name__, args[1]))

            test_func(*args, **kwargs)

            print("END({}.{})<==========".format(test_func.__name__, args[1]))

    return patched
