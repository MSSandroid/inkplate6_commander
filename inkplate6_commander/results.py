from parse import parse


class Result():
    def __init__(self):
        self.val = None

    def parse(self, bin_string):
        raise NotImplementedError()

    def __str__(self):
        return f'{type(self).__name__}={self.val}'

    def __repr__(self):
        return str(self)


class EchoResult(Result):
    def parse(self, bin_string):
        self.val = True if bin_string.decode() == "OK\r\n" else False


class DrawBitmapResult(Result):
    def parse(self, bin_string):
        v = int(parse("#H({})*\r\n", bin_string.decode()).fixed[0])
        if v == 1:
            self.val = 'Image loaded succesfully'
        elif v == 0:
            self.val = 'Image load failed'
        elif v == -1:
            self.val = 'SD Card Init Error'


class GetDisplayModeResult(Result):
    def parse(self, bin_string):
        self.val = int(parse("#J({})*\r\n", bin_string.decode()).fixed[0])


class ReadTemperatureResult(Result):
    def parse(self, bin_string):
        self.val = int(parse("#N({})*\r\n", bin_string.decode()).fixed[0])


class ReadTouchpadResult(Result):
    def __init__(self, pad):
        super().__init__()
        self.pad = pad

    def parse(self, bin_string):
        self.val = bool(parse("#O({})*\r\n", bin_string.decode()).fixed[0])

    def __str__(self):
        return f'{type(self).__name__}(pad={self.pad})={self.val}'


class ReadBatteryResult(Result):
    def parse(self, bin_string):
        self.val = float(parse("#P({})*\r\n", bin_string.decode()).fixed[0])


class GetPanelStateResult(Result):
    def parse(self, bin_string):
        self.val = bool(parse("#R({})*\r\n", bin_string.decode()).fixed[0])
