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

import bitmath

status_dict = {0: "OK", 1: "WARNING", 2: "CRITICAL", 3: "UNKNOWN"}


def byte_to_GiB(size_byte):
    return bitmath.Byte(size_byte).to_GiB().value


def byte_to_GB(size_byte):
    return bitmath.Byte(size_byte).to_GB().value


def get_all_status(unity_objects):
    ok, warning, critical, unknown = [], [], [], []
    for obj in unity_objects:
        status = get_single_status(obj)
        if status == 0:
            ok.append((status, obj.id))
        elif status == 1:
            warning.append((status, obj.id))
        elif status == 2:
            critical.append((status, obj.id))
        else:
            unknown.append((status, obj.id))
    return ok, warning, critical, unknown


def get_single_status(obj):
    if obj.health.value.value[0] in (5, 7):
        # OK status
        return 0
    if obj.health.value.value[0] in (10, 15, 20):
        # Warning status
        return 1
    if obj.health.value.value[0] in (25, 30):
        # Critical status
        return 2
    if obj.health.value.value[0] in (0,):
        # Unknown status
        return 3
    raise ValueError("The object is in Unknown/Unrecoverable state.")


def get_status_mark(obj, mark):
    status = status_dict.get(mark)
    return "{} {}: ".format(obj, status)


def print_if_failure(status_code, items):
    # Avoid printing the error if status code contains (0, xx)
    if not all(map(lambda x: x[0], status_code)):
        return
    ids = [x[1] for x in status_code]
    failed_items = [item for item in items if item.id in ids]
    for failed in failed_items:
        print("{}: Reason={}".format(failed.name, ";".join(
            failed.health.descriptions)))
    return len(failed_items)


def get_by_id(_id, items):
    for item in items:
        if _id == item.id:
            return item
    return None


def format_enum(enum):
    if enum:
        return enum.description
