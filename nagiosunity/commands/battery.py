import logging
import nagiosplugin
from nagiosunity.vendor import unity

_log = logging.getLogger(__name__)


class Battery(unity.UnityWrapper,
              nagiosplugin.Resource):
    name = 'battery'

    def __init__(self, options, **kwargs):
        super(Battery, self).__init__(options)
        self.options = options
        self.kwargs = kwargs
        self._batteries = None

    @property
    def batteries(self):
        return self._batteries if self._batteries else self.unity.get_battery()

    def probe(self):
        self._batteries = self.batteries
        all_status = unity.get_all_status(self.batteries)
        if all_status[0] == 0:
            self.ok = all_status[1]

        if all_status[0] == 1:
            self.warning = all_status[1]

        if all_status[0] == 2:
            self.critical = all_status[1]

        return [nagiosplugin.Metric('battery [%s]' % s[1], s[0], context='battery') for s in all_status[1]]

    @staticmethod
    def get_check_instance(options, **kwargs):
        check = nagiosplugin.Check(
            Battery(options),
            nagiosplugin.ScalarContext(
                options.command, warning="@1:1", critical="@2:2"),
            BatterySummary()
        )
        return check


class BatterySummary(nagiosplugin.Summary):
    def ok(self, results):
        return "All batteries are in OK state."

    def warning(self, results):
        return "%d batteries are in Warning state." % len(results['battery'].resource.warning)

    def critical(self, results):
        return "%d batteries are in Critical state." % len(results['battery'].resource.critical)

    def verbose(self, results):
        super(BatterySummary, self).verbose(results)
        if results:
            return "Total: %d batteries, " % len(results[0].resource.batteries)
