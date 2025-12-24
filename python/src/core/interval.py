from math import inf
from typing import ClassVar

class interval:
    empty: ClassVar['interval']
    universe: ClassVar['interval']

    def __init__(self):
        pass
        
    @classmethod
    def from_floats(cls, min: float = inf, max: float = -inf) -> 'interval':
        instance = cls()
        instance.min = min
        instance.max = max
        return instance
    
    @classmethod
    def from_intervals(cls, a: 'interval', b: 'interval') -> 'interval':
        instance = cls()
        instance.min = a.min if a.min < b.min else b.min
        instance.max = a.max if a.max > b.max else b.max
        return instance    


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
        
    def expand(self, delta: float) -> 'interval':
        padding = delta / 2
        return interval.from_floats(self.min - padding, self.max + padding)

# Class constants
interval.empty = interval.from_floats(inf, -inf)
interval.universe = interval.from_floats(-inf, inf)