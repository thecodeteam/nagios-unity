import logging
from nagiosunity.lib import unity
from nagiosunity.lib import utils

_log = logging.getLogger(__name__)


class SasPort(unity.UnityWrapper):
    name = 'sas_port'

    def __init__(self, options, **kwargs):
        super(SasPort, self).__init__(options)
        self.options = options
        self.kwargs = kwargs
        self._sas_ports = None

    @property
    def sas_ports(self):
        if not self._sas_ports:
            self._sas_ports = self.unity.get_sas_port()
        return self._sas_ports

    def check(self):
        all_status = ok, warning, critical, unknown = utils.get_all_status(self.sas_ports)
        code = max(ok + warning + critical + unknown, key=lambda i: i[0])
        code = code[0]
        status_mark = utils.get_status_mark("SAS_PORT", code)
        first_line = "Total SAS ports #{}, Failed ports(ID): {}".format(
            len(ok + warning + critical + unknown), [c[1] for c in critical])
        # Status line
        print(status_mark + first_line + "|")

        # Failed details
        utils.print_if_failure(all_status[code], self.sas_ports)
        # Performance detail
        for port in self.sas_ports:
            print("{}: Link status={}, Current Speed={}".format(
                port.name, self.get_link_status(port),
                utils.format_enum(port.current_speed)
            ))
        return code

    def get_link_status(self, port):
        if utils.get_single_status(port) == 0:
            if " link is down" in ''.join(port.health.descriptions):
                return "DOWN"
            else:
                return "UP"
        return "DOWN"
