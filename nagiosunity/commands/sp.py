import logging
from nagiosunity.lib import unity
from nagiosunity.lib import utils

_log = logging.getLogger(__name__)


class StorageProcessor(unity.UnityWrapper):
    name = 'sp'

    def __init__(self, options, **kwargs):
        super(StorageProcessor, self).__init__(options)
        self.options = options
        self.kwargs = kwargs
        self._sp = None

    @property
    def sp(self):
        return self._sp if self._sp else self.unity.get_sp()

    def check(self):
        all_status = ok, warning, critical, unknown = utils.get_all_status(self.sp)
        code = max(ok + warning + critical + unknown, key=lambda i: i[0])
        code = code[0]
        status_mark = utils.get_status_mark("SP", code)
        first_line = "Total SPs #{}, Failed SP(ID): {}".format(
            len(ok + warning + critical + unknown), [c[1] for c in critical])
        # Status line
        print(status_mark + first_line + "|")
        # Failed details
        utils.print_if_failure(all_status[code], self.sp)
        # Performance detail
        for p in self.sp:
            print("{}: Rescue Mode={}, Bios Firmware Revision={}, "
                  "Post Firmware Revision={}, Needs Replacement={}".format(
                p.name,
                p.is_rescue_mode,
                p.bios_firmware_revision,
                p.post_firmware_revision,
                p.needs_replacement
            ))
        return code
