from __future__ import division
import logging
from nagiosunity.lib import unity
from nagiosunity.lib import utils

_log = logging.getLogger(__name__)


class PowerSupply(unity.UnityWrapper):
    name = 'power_supply'

    def __init__(self, options, **kwargs):
        super(PowerSupply, self).__init__(options)
        self.options = options
        self.kwargs = kwargs
        self._supplies = None

    @property
    def power_supplies(self):
        return self._supplies if self._supplies else self.unity.get_power_supply()

    def check(self):
        all_status = ok, warning, critical, unknown = utils.get_all_status(self.power_supplies)
        code = max(ok + warning + critical + unknown, key=lambda i: i[0])
        code = code[0]
        status_mark = utils.get_status_mark("POWER SUPPLY", code)
        first_line = "Total power supplies #{}, Failed supplies: {}".format(
            len(ok + warning + critical + unknown), [c[1] for c in critical])
        # Status line
        print(status_mark + first_line + "|")

        # Failed details
        utils.print_if_failure(all_status[code], self.power_supplies)
        return code
