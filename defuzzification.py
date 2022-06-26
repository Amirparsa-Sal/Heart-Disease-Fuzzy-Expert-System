from dataclasses import dataclass
from abc import abstractmethod, ABC
from typing import List
from fuzzification import FuzzySet

@dataclass
class FuzzySetDefuzData:
    fuzzy_set: FuzzySet
    cut_value: float

class DefuzzificationMethod(ABC):
    '''An abstract class to represent a defuzzification method.'''

    @abstractmethod
    def defuzzify(self, data: List[FuzzySetDefuzData]) -> float:
        '''Defuzzify the data.'''
        pass
    
class CenterOfMassDefuz(DefuzzificationMethod):
    '''A class to calculate the center of mass of the output fuzzysets.'''

    def __init__(self, stride, range) -> None:
        super().__init__()
        self.stride = stride
        self.range = range

    def defuzzify(self, data: List[FuzzySetDefuzData]) -> float:
        '''Defuzzify the data.'''
        total_area = 0
        for i in [self.range[0] + i * self.stride for i in range(int((self.range[1] - self.range[0]) / self.stride) + 1)]:
            max_value = float('-inf')
            for fuzzy_set_data in data:
                value = fuzzy_set_data.fuzzy_set.get_cut_value(i, fuzzy_set_data.cut_value)
                max_value = max(max_value, value)
            total_area += max_value * self.stride
        return total_area