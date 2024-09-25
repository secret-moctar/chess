class Move:
    def __init__(self, start,  end, cap):
        self.start = start
        self.end = end
        self.is_capture = cap

    def __eq__(self, other):
        if isinstance(other, Move):
            return other == self
        return self.end == other
