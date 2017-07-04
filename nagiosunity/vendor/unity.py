import nagiosplugin
import storops


class UnityWrapper(object):
    def __init__(self, options):
        self.options = options

    @property
    def unity(self):
        return storops.UnitySystem(
            self.options.host,
            self.options.username,
            self.options.password)


def get_all_status(unity_objects):
    ok, warning, critical, unknown = [], [], [], []
    for obj in unity_objects:
        status = get_single_status(obj)
        if status == 0:
            ok.append((status, obj.id))
        elif status == 1:
            warning.append((status, obj.id))
        elif status == 2:
            critical.append((status, obj.id))
        else:
            unknown.append((status, obj.id))
    if unknown:
        raise nagiosplugin.CheckError("%d disk(s) are in Unknown/Unrecoverable state." % len(unknown))
    if critical:
        return 2, critical
    if warning:
        return 1, warning
    else:
        return 0, ok


def get_single_status(obj):
    if obj.health.value.value[0] in (5, 7):
        # OK status
        return 0
    if obj.health.value.value[0] in (10, 15, 20):
        # Warning status
        return 1
    if obj.health.value.value[0] in (25, 30):
        # Critical status
        return 2
    if obj.health.value.value[0] in (0,):
        # Unknown status
        return 3
    raise nagiosplugin.CheckError("The disk is in Unknown/Unrecoverable state.")
