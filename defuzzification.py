from dataclasses import dataclass
from abc import abstractmethod, ABC
from typing import Tuple, List

@dataclass
class FuzzySetDefuzData:
    membership_function: callable
    range: Tuple[float, float]

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
        for i in range(self.range[0], self.range[1], self.stride):
            max_value = float('-inf')
            for fuzzy_set_data in data:
                if fuzzy_set_data.range[0] <= i <= fuzzy_set_data.range[1] and fuzzy_set_data.membership_function(i) > max_value:
                    max_value = fuzzy_set_data.membership_function(i)
            total_area += max_value * self.stride
        return total_area