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

"""
Unity plugin for Nagios.

Usage:
    nagios-unity -H <HOST> -u <USERNAME> -p <PASSWORD> [--cacert <CACERT>]  \
<OBJECT>
    nagios-unity -h | --help
    nagios-unity --version

Arguments:
    OBJECT  One of below values:
        battery, dae, disk, dpe,
        ethernet_port fan, fc_port,
        io_module, lcc, lun, memory_module,
        pool, power_supply, sas_port,
        sp, ssc, ssd, system, array_hardware

Options:
    -h --help                         Show this screen.
    -V --version                      Show version.
    -C --cacert <CACERT>              Unity CA certificates.
    -H --host <HOST>                  Unity IP address.
    -u --username <USERNAME>          Unity User login.
    -p --password <PASSWORD>          Unity password.
    -v --verbose                      show verbose logs.

Examples:
  nagios-unity -H 10.245.101.39 -u admin -p Password123! ssc

"""

from docopt import docopt

import functools
import nagiosunity
from nagiosunity.lib import utils
from nagiosunity.cli import opt
from nagiosunity import commands
import requests
import urllib3
import sys

urllib3.disable_warnings()


def wrap_connection_error(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.ConnectionError:
            code = 1  # set to warning status
            status_mark = utils.get_status_mark(sys.argv[-1:][0], code)
            first_line = ("ConnectionError occurred, "
                          "the array is offline or unreachable.")
            print(status_mark + first_line + " | ")
            return code

    return inner


@wrap_connection_error
def main():
    """Main cli entry point for distributing cli commands."""
    options = docopt(__doc__, version=nagiosunity.__version__)
    cli_opt = opt.Options(options)

    if cli_opt.command in commands.commands_dict.keys():
        command = commands.commands_dict.get(cli_opt.command)
        return command(cli_opt).check()
    else:
        raise ValueError("Invalid object specified: '%s', "
                         "use 'nagios-unity --help' for details."
                         % cli_opt.command)
