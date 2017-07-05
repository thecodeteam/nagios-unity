import logging
from nagiosunity.vendor import unity

_log = logging.getLogger(__name__)


class EthernetPort(unity.UnityWrapper):
    name = 'ethernet_port'

    def __init__(self, options, **kwargs):
        super(EthernetPort, self).__init__(options)
        self.options = options
        self.kwargs = kwargs
        self._ethernet_ports = None

    @property
    def ethernet_ports(self):
        return self._ethernet_ports if self._ethernet_ports else self.unity.get_ethernet_port()

    def check(self):
        ok, warning, critical, unknown = unity.get_all_status(self.ethernet_ports)
        code = max(ok + warning + critical + unknown, key=lambda i: i[0])
        status_mark = unity.get_status_mark("ETHERNET_PORT", code[0])
        first_line = "Total #{} ethernet ports, Failed ports #{}".format(
            len(ok + warning + critical + unknown), len(critical))
        # Status line
        print(status_mark + first_line + "|")
        # Performance detail
        for port in self.ethernet_ports:
            print("{}: Link status={}, Requested Speed={}, Current Speed={}".format(
                port.name, "UP" if port.is_link_up else "DOWN",
                unity.format_enum(port.requested_speed),
                unity.format_enum(port.speed)
            ))
        return code
