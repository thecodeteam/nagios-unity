"""
Unity plugin for Nagios.

Usage:
    nagios-unity [-v] -H <HOST> -u <USERNAME> -p <PASSWORD> <OBJECT> [-w <warning>] [-c <critical>]
    nagios-unity -h | --help
    nagios-unity --version

Arguments:
    OBJECT  One of below values:
        battery, dae, disk, dpe,
        ethernet_port fan, fc_port,
        io_module, lcc, memory_module,
        pool, power_supply, sas_port,
        sp, ssc, ssd, system

Options:
    -h --help                         Show this screen.
    -V --version                      Show version.
    -H --host                         Unity IP address.
    -u --username                     Unity User login.
    -p --password                     Unity password.
    -w --warning                      warning threshold.
    -c --critical                     critical threshold.
    -v --verbose                      show verbose logs.

Examples:
  nagios-unity disk -w :5 -c 10:

"""

from docopt import docopt

import nagiosunity
from nagiosunity.cli import opt
from nagiosunity import commands

try:
    urllib3 = __import__('urllib3')
except ImportError:
    urllib3 = None
if urllib3:
    urllib3.disable_warnings()


def main():
    """Main cli entry point for distributing cli commands."""
    options = docopt(__doc__, version=nagiosunity.__version__)
    cli_opt = opt.Options(options)

    if cli_opt.command in commands.commands_dict.keys():
        command = commands.commands_dict.get(cli_opt.command)
        return command(cli_opt).check()
    else:
        raise ValueError("Invalid object specified: %s, "
                         "use 'nagios-unity --help' for details." % cli_opt.command)
