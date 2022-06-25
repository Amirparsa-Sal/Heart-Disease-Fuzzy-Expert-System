from abc import abstractmethod, ABC
from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np

class FuzzySetSection(ABC):
    '''This is a class to define a section in a fuzzyset. this section can be a line or a constant value.'''

    @abstractmethod
    def range(self) -> Tuple:
        '''Returns the range of the section.'''
        pass
    
    @abstractmethod
    def get_value(self, x: float) -> Tuple:
        '''Returns the value of the section at x.'''
        pass

class Line(FuzzySetSection):
    '''This is a class to define a line in a fuzzyset.'''
    def __init__(self, start_pos: Tuple, end_pos: Tuple) -> None:
        # put start_pos and end_pos in order
        if start_pos[0] < end_pos[0]:
            self.start_pos = start_pos
            self.end_pos = end_pos
        else:
            self.start_pos = end_pos
            self.end_pos = start_pos
        # find the line parameters
        self.m, self.b = self.__find_line_paramaters(self.start_pos[0], self.start_pos[1], self.end_pos[0], self.end_pos[1])

    def get_value(self, x: float) -> Tuple:
        return self.m * x + self.b
    
    def range(self) -> Tuple:
        return self.start_pos[0], self.end_pos[0]
    
    def __find_line_paramaters(self, x1: int, y1: int, x2: int, y2: int) -> Tuple:
        weights = np.array([[x1, 1], [x2, 1]])
        out = np.array([y1, y2])
        result = np.linalg.solve(weights, out)
        return result[0], result[1]

class ConstantValue:
    '''This is a class to define a constant value in a fuzzyset.'''
    def __init__(self, start_x: float, end_x: float, value: float) -> None:
        self.start_x = start_x
        self.end_x = end_x
        self.value = value
    
    def get_value(self, x: float) -> float:
        return self.value
    
    def range(self) -> Tuple:
        return self.start_x, self.end_x

class FuzzySet:
    '''This is a class to define a fuzzyset.'''
    def __init__(self, name:str, range: Tuple) -> None:
        self.name = name
        self.range = range
        self.sections = []

    def add(self, section: FuzzySetSection) -> None:
        '''Adds a section to the fuzzyset.'''
        # Check if the section has an intersection with other sections
        for s in self.sections:
            if self.__has_interception(s.range(), section.range()):
                raise ValueError('Interception between sections')
        self.sections.append(section)
    
    def get_value(self, x: float) -> float:
        '''Returns the value of the fuzzyset at x.'''
        # raise error if x is not in the range
        if x < self.range[0] or x > self.range[1]:
            return ValueError('x out of range')
        # find the section that contains x to get the value
        for section in self.sections:
            if section.range()[0] <= x <= section.range()[1]:
                return section.get_value(x)
        return 0
    
    def plot(self) -> None:
        '''Plots the fuzzyset.'''
        x = np.linspace(self.range[0], self.range[1], 100)
        y = [self.get_value(_x) for _x in x]
        plt.plot(x, y)
        plt.show()

    def __has_interception(self, range1: Tuple, range2: Tuple) -> bool:
        if range2[0] < range1[1] < range2[1] or range1[0] < range2[1] < range1[1]:
            return True
        return False

# Define age fuzzysets
AGE_RANGE = (0, 100)

age_young = FuzzySet(name='age_young', range=AGE_RANGE)
age_young.add(ConstantValue(start_x=AGE_RANGE[0], end_x=29, value=1))
age_young.add(Line((29, 1), (38, 0)))

age_mild = FuzzySet(name='age_mild', range=AGE_RANGE)
age_mild.add(Line((33, 0), (38, 1)))
age_mild.add(Line((38, 1), (45, 0)))


age_old = FuzzySet(name='age_old', range=AGE_RANGE)
age_old.add(Line((40, 0), (48, 1)))
age_old.add(Line((48, 1), (58, 0)))


age_veryold = FuzzySet(name='age_veryold', range=AGE_RANGE)
age_veryold.add(Line((52, 0), (60, 1)))
age_veryold.add(ConstantValue(start_x=60, end_x=AGE_RANGE[1], value=1))
