from math import inf
from typing import ClassVar

class interval:
    empty: ClassVar['interval']
    universe: ClassVar['interval']

    def __init__(self, min: float = inf, max: float = -inf):
        self.min = min
        self.max = max

    def size(self) -> float:
        return self.max - self.min

    def contains(self, x: float) -> bool:
        return self.min <= x <= self.max

    def surrounds(self, x: float) -> bool:
        return self.min < x < self.max
    
    def clamp(self, x: float) -> float:
        if x < self.min:
            return self.min
        elif x > self.max:
            return self.max
        else:
            return x

# Class constants
interval.empty = interval(inf, -inf)
interval.universe = interval(-inf, inf)