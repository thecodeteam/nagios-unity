from nagiosunity.commands import battery
from nagiosunity.commands import disk
from nagiosunity.commands import dpe
from nagiosunity.commands import dae
from nagiosunity.commands import ethernet_port
from nagiosunity.commands import fan
from nagiosunity.commands import fc_port
from nagiosunity.commands import io_module


COMMANDS = [battery.Battery, disk.Disk, ethernet_port.EthernetPort]

commands_dict = {cmd.name: cmd for cmd in COMMANDS}