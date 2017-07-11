from __future__ import division
import logging
from nagiosunity.lib import unity
from nagiosunity.lib import utils

_log = logging.getLogger(__name__)


class IoModule(unity.UnityWrapper):
    name = 'io_module'

    def __init__(self, options, **kwargs):
        super(IoModule, self).__init__(options)
        self.options = options
        self.kwargs = kwargs
        self._modules = None

    @property
    def io_modules(self):
        return self._modules if self._modules else self.unity.get_io_module()

    def check(self):
        all_status = ok, warning, critical, unknown = utils.get_all_status(self.io_modules)
        code = max(ok + warning + critical + unknown, key=lambda i: i[0])
        code = code[0]
        status_mark = utils.get_status_mark("IO MODULE", code)
        first_line = "Total io modules #{}, Failed modules: {}".format(
            len(ok + warning + critical + unknown), [c[1] for c in critical])
        # Status line
        print(status_mark + first_line + "|")

        # Failed details
        utils.print_if_failure(all_status[code], self.io_modules)
        return code
