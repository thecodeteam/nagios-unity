import logging

_log = logging.getLogger(__name__)


class Options(object):
    def __init__(self, options):
        _log.debug(options)
        self.data = options

    @property
    def warning(self):
        if self.data.get('--warning'):
            return self.data.get('<warning>')

    @property
    def critical(self):
        if self.data.get('--critical'):
            return self.data.get('<critical>')

    @property
    def verbose(self):
        return self.data.get('--verbose')

    @property
    def command(self):
        command = self.data.get('<OBJECT>', None)
        if command:
            return command
        return None

    @property
    def host(self):
        return self.data.get('<HOST>', '')

    @property
    def username(self):
        return self.data.get('<USERNAME>', '')

    @property
    def password(self):
        return self.data.get('<PASSWORD>', '')

