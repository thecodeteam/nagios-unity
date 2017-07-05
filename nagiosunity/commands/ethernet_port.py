import logging
import nagiosplugin
from nagiosunity.vendor import unity

_log = logging.getLogger(__name__)


class EthernetPort(unity.UnityWrapper,
                   nagiosplugin.Resource):
    name = 'ethernet_port'

    def __init__(self, options, **kwargs):
        super(EthernetPort, self).__init__(options)
        self.options = options
        self.kwargs = kwargs
        self._ethernet_ports = None

    @property
    def ethernet_ports(self):
        return self._ethernet_ports if self._ethernet_ports else self.unity.get_ethernet_port()

    def probe(self):
        self._ethernet_ports = self.ethernet_ports
        all_status = unity.get_all_status(self.ethernet_ports)
        return [nagiosplugin.Metric('ethernet_port %s' % item[1], item[0], context='ethernet_port')
                for item in (all_status[0] + all_status[1] + all_status[2] + all_status[3])]

    @staticmethod
    def get_check_instance(options, **kwargs):
        check = nagiosplugin.Check(
            EthernetPort(options),
            nagiosplugin.ScalarContext(
                options.command, warning="@1:1", critical="@2:2"),
            EthernetPortSummary()
        )
        return check


class EthernetPortSummary(nagiosplugin.Summary):
    def ok(self, results):
        super(EthernetPortSummary, self).ok(results)

        return "All ethernet_ports are in OK state."

    def problem(self, results):
        super(EthernetPortSummary, self).problem(results)
        return "%d ethernet_ports are in Warning state." % len(
            results[0].resource.warning)

    def _format(self, result):
        first_line = "Total: #{0}, {1} of OK, {2} of failed, " \
                     "{3} of hot spares, {4} of unbound disks, " \
                     "ID of failed disks: {5}".format(
            len(result.resource.ethernet_ports),
            len())
        return first_line

    def verbose(self, results):
        super(EthernetPortSummary, self).verbose(results)
        if results:
            return "Total: %d ethernet_ports, " % len(results[0].resource.ethernet_ports)
