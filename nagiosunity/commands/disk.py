from __future__ import division
import logging
from nagiosunity.lib import unity
from nagiosunity.lib import utils

_log = logging.getLogger(__name__)


class Disk(unity.UnityWrapper):
    name = 'disk'

    def __init__(self, options, **kwargs):
        super(Disk, self).__init__(options)
        self.options = options
        self.kwargs = kwargs
        self._disks = None
        self._disk_groups = None

    @property
    def disks(self):
        return self._disks if self._disks else self.unity.get_disk()

    @property
    def disk_groups(self):
        return self._disk_groups if self._disk_groups else self.unity.get_disk_group()

    def check(self):
        all_status = ok, warning, critical, unknown = utils.get_all_status(self.disks)
        code = max(ok+ warning+ critical+ unknown, key=lambda i: i[0])
        code = code[0]
        status_mark = utils.get_status_mark("DISK", code)
        first_line = "Total Disks #{}, Failed Disks: {}, Hot spares: {}, " \
                     "Unbounded: {}".format(
            len(ok +warning+ critical+ unknown),
            [c[1] for c in critical], self.get_hot_spares(), self.get_unbounded_disks())
        # Status line
        print(status_mark + first_line + "|")

        # Failed details
        utils.print_if_failure(all_status[code], self.disks)
        return code

    def get_unbounded_disks(self):
        total = 0
        for group in self.disk_groups:
            total += group.unconfigured_disks
        return total

    def get_hot_spares(self):
        total = 0
        for group in self.disk_groups:
            if group.unconfigured_disks != group.total_disks:
                total += group.min_hot_spare_candidates
        return total
