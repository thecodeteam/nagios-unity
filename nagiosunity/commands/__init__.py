from nagiosunity.commands import battery, sas_port, system, sp, pool, lcc, \
    memory_module, power_supply, ssc, ssd, lun
from nagiosunity.commands import disk
from nagiosunity.commands import dae
from nagiosunity.commands import ethernet_port
from nagiosunity.commands import fan
from nagiosunity.commands import fc_port
from nagiosunity.commands import io_module

COMMANDS = [battery.Battery,
            disk.Disk,
            ethernet_port.EthernetPort,
            fc_port.FcPort,
            sas_port.SasPort,
            system.System,
            sp.StorageProcessor,
            pool.Pool,
            dae.Dae,
            io_module.IoModule,
            lcc.Lcc,
            memory_module.MemoryModule,
            fan.Fan,
            power_supply.PowerSupply,
            battery.Battery,
            ssc.Ssc,
            ssd.Ssd,
            lun.Lun]

commands_dict = {cmd.name: cmd for cmd in COMMANDS}
