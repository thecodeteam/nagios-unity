from __future__ import division
import logging
from nagiosunity.lib import unity
from nagiosunity.lib import utils

_log = logging.getLogger(__name__)


class Lcc(unity.UnityWrapper):
    name = 'lcc'

    def __init__(self, options, **kwargs):
        super(Lcc, self).__init__(options)
        self.options = options
        self.kwargs = kwargs
        self._lccs = None

    @property
    def lccs(self):
        return self._lccs if self._lccs else self.unity.get_lcc()

    def check(self):
        all_status = ok, warning, critical, unknown = utils.get_all_status(self.lccs)
        code = max(ok + warning + critical + unknown, key=lambda i: i[0])
        code = code[0]
        status_mark = utils.get_status_mark("LCC", code)
        first_line = "Total LCCs #{}, Failed LCCs: {}".format(
            len(ok + warning + critical + unknown), [c[1] for c in critical])
        # Status line
        print(status_mark + first_line + "|")

        # Failed details
        utils.print_if_failure(all_status[code], self.lccs)
        return code
