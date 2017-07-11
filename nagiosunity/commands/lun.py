from __future__ import division
import logging
from nagiosunity.lib import unity
from nagiosunity.lib import utils

_log = logging.getLogger(__name__)


class Lun(unity.UnityWrapper):
    name = 'lun'

    def __init__(self, options, **kwargs):
        super(Lun, self).__init__(options)
        self.options = options
        self.kwargs = kwargs
        self._luns = None

    @property
    def luns(self):
        return self._luns if self._luns else self.unity.get_lun()

    def check(self):
        all_status = ok, warning, critical, unknown = utils.get_all_status(self.luns)
        code = max(ok + warning + critical + unknown, key=lambda i: i[0])
        code = code[0]
        status_mark = utils.get_status_mark("LUN", code)
        first_line = "Total LUNs #{}, Failed LUNs: {}".format(
            len(ok + warning + critical + unknown), [c[1] for c in critical])
        # Status line
        print(status_mark + first_line + "|")

        # Failed details
        utils.print_if_failure(all_status[code], self.luns)
        return code

