import logging
from nagiosunity.lib import unity
from nagiosunity.lib import utils

_log = logging.getLogger(__name__)


class Dae(unity.UnityWrapper):
    name = 'dae'

    def __init__(self, options, **kwargs):
        super(Dae, self).__init__(options)
        self.options = options
        self.kwargs = kwargs
        self._dae = None

    @property
    def dae(self):
        return self._dae if self._dae else (self.unity.get_dae() + self.unity.get_dpe())

    def check(self):
        ok, warning, critical, unknown = utils.get_all_status(self.dae)
        code = max(ok + warning + critical + unknown, key=lambda i: i[0])
        code = code[0]
        status_mark = utils.get_status_mark("SP", code)
        first_line = "Total DAEs #{}, Failed DAE(ID): {}".format(
            len(ok + warning + critical + unknown), [c[1] for c in critical])
        # Status line
        print(status_mark + first_line + "|")
        # Performance detail
        for d in self.dae:
            print("{}: Power(curr/avg/max)={}/{}/{} watts, "
                  "Temperature(curr/avg/max)={}/{}/{} degrees , "
                  "Speed(curr/max)={}/{} GB".format(
                d.name,
                d.current_power, d.avg_power, d.max_power,
                d.current_temperature, d.avg_temperature, d.max_temperature,
                utils.byte_to_GB(d.current_speed), utils.byte_to_GB(d.max_speed)
            ))
        return code
