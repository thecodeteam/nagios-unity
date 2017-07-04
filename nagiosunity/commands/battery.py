
class Battery(object):
    name = 'battery'

    def __init__(self, options, **kwargs):
        self.options = options
        self.kwargs = kwargs

    def __str__(self):
        return "Unity Battery: %d" % id(self)

    def check(self):
        print("all params: %s ", self.kwargs)
