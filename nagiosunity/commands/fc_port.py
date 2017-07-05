import logging
from nagiosunity.lib import unity
from nagiosunity.lib import utils

_log = logging.getLogger(__name__)


class FcPort(unity.UnityWrapper):
    name = 'fc_port'

    def __init__(self, options, **kwargs):
        super(FcPort, self).__init__(options)
        self.options = options
        self.kwargs = kwargs
        self._fc_ports = None

    @property
    def fc_ports(self):
        return self._fc_ports if self._fc_ports else self.unity.get_fc_port()

    def check(self):
        ok, warning, critical, unknown = utils.get_all_status(self.fc_ports)
        code = max(ok + warning + critical + unknown, key=lambda i: i[0])
        code = code[0]
        status_mark = utils.get_status_mark("FC_PORT", code)
        first_line = "Total fc ports #{}, Failed ports(ID): {}".format(
            len(ok + warning + critical + unknown), [c[1] for c in critical])
        # Status line
        print(status_mark + first_line + "|")
        # Performance detail
        for port in self.fc_ports:
            print("{}: Link status={}, Requested Speed={}, Current Speed={}".format(
                port.name, self.get_link_status(port),
                utils.format_enum(port.requested_speed),
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
