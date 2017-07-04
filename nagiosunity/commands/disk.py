import logging
import nagiosplugin
from nagiosunity.vendor import unity

_log = logging.getLogger(__name__)


class Disk(unity.UnityWrapper,
           nagiosplugin.Resource):
    name = 'disk'

    def __init__(self, options, **kwargs):
        super(Disk, self).__init__(options)
        self.options = options
        self.kwargs = kwargs
        self._disks = None

    @property
    def disks(self):
        return self._disks if self._disks else self.unity.get_disk()

    def probe(self):
        self._disks = self.disks
        all_status = unity.get_all_status(self.disks)
        if all_status[0] == 0:
            self.ok = all_status[1]

        if all_status[0] == 1:
            self.warning = all_status[1]

        if all_status[0] == 2:
            self.critical = all_status[1]

        return [nagiosplugin.Metric('disk [%s]' % s[1], s[0], context='disk') for s in all_status[1]]

    @staticmethod
    def get_check_instance(options, **kwargs):
        check = nagiosplugin.Check(
            Disk(options),
            nagiosplugin.ScalarContext(
                options.command, warning="@1:1", critical="@2:2"),
            DiskSummary()
        )
        return check


class DiskSummary(nagiosplugin.Summary):
    def ok(self, results):
        return "All disks are in OK state."

    def warning(self, results):
        return "%d disks are in Warning state." % len(results['disk'].resource.warning)

    def critical(self, results):
        return "%d disks are in Critical state." % len(results['disk'].resource.critical)

    def verbose(self, results):
        super(DiskSummary, self).verbose(results)
        if results:
            return "Total: %d disks, " % len(results[0].resource.disks)
