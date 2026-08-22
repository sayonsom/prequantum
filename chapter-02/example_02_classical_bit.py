class Bit:
    """A mutable classical bit."""

    def __init__(self, value=0):
        if value not in (0, 1):
            raise ValueError("A bit must be 0 or 1.")
        self.value = value

    def read(self):
        return self.value

    def flip(self):
        self.value = 1 - self.value
        return self


bit = Bit(0)
print(bit.read())
print(bit.read())
print(bit.flip().read())
# 0
# 0
# 1
