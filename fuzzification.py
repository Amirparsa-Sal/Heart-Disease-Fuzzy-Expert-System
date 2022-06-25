from abc import abstractmethod, ABC
from typing import Tuple

class FuzzySetSection(ABC):
    
    @abstractmethod
    def range(self) -> Tuple:
        pass
    
    @abstractmethod
    def get_value(self, x: float) -> Tuple:
        pass

class Line(FuzzySetSection):
    def __init__(self, start_pos: Tuple, end_pos: Tuple) -> None:
        if start_pos[0] < end_pos[0]:
            self.start_pos = start_pos
            self.end_pos = end_pos
        else:
            self.start_pos = end_pos
            self.end_pos = start_pos
        self.m, self.b = self.find_line_paramaters(self.start_pos[0], self.start_pos[1], self.end_pos[0], self.end_pos[1])

    def find_line_paramaters(self, x1: int, y1: int, x2: int, y2: int) -> Tuple:
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        return m, b

    def get_value(self, x: float) -> Tuple:
        return self.m * x + self.b
    
    def range(self) -> Tuple:
        return self.start_pos[0], self.end_pos[0]

class ConstantValue:
    def __init__(self, start_x: float, end_x: float, value: float) -> None:
        self.start_x = start_x
        self.end_x = end_x
        self.value = value
    
    def get_value(self, x: float) -> float:
        return self.value
    
    def range(self) -> Tuple:
        return self.start_x, self.end_x

class FuzzySet:

    def __init__(self, name:str, range: Tuple) -> None:
        self.name = name
        self.range = range
        self.sections = []

    def add(self, section: FuzzySetSection) -> None:
        for s in self.sections:
            if self.__has_interception(s.range(), section.range()):
                raise ValueError('Interception between sections')
        self.sections.append(section)
    
    def get_value(self, x: float) -> float:
        if x < self.range[0] or x > self.range[1]:
            return ValueError('x out of range')

        for section in self.sections:
            if section.range()[0] <= x <= section.range()[1]:
                return section.get_value(x)
        return 0
    
    def __has_interception(self, range1: Tuple, range2: Tuple) -> bool:
        if range2[0] < range1[1] < range2[1] or range1[0] < range2[1] < range1[1]:
            return True
        return False

# Define age fuzzysets
AGE_RANGE = (0, 100)

age_young = FuzzySet(name='age_young', range=AGE_RANGE)
age_young.add(ConstantValue(start_x=0, end_x=29, value=1))
age_young.add(Line((29, 1), (38, 0)))

age_mild = FuzzySet(name='age_mild', range=AGE_RANGE)
age_mild.add(Line((33, 0), (38, 1)))
age_mild.add(Line((38, 1), (45, 0)))

age_old = FuzzySet(name='age_old', range=AGE_RANGE)
age_old.add(Line((40, 0), (48, 1)))
age_old.add(Line((48, 1), (58, 0)))


age_veryold = FuzzySet(name='age_veryold', range=AGE_RANGE)
age_veryold.add(Line((52, 0), (60, 1)))