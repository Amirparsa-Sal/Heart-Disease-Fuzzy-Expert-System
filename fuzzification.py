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

# Define Blood pressure fuzzysets
BP_RANGE = (0, 350)

blood_pressure_low = FuzzySet(name='bloodPressure_low', range=BP_RANGE)
blood_pressure_low.add(ConstantValue(start_x=BP_RANGE[0], end_x=111, value=1))
blood_pressure_low.add(Line((111, 1), (134, 0)))

blood_pressure_medium = FuzzySet(name='bloodPressure_medium', range=BP_RANGE)
blood_pressure_medium.add(Line((127, 0), (139, 1)))
blood_pressure_medium.add(Line((139, 1), (153, 0)))

blood_pressure_high = FuzzySet(name='bloodPressure_high', range=BP_RANGE)
blood_pressure_high.add(Line((153, 0), (157, 1)))
blood_pressure_high.add(Line((157, 1), (172, 0)))

blood_pressure_veryhigh = FuzzySet(name='bloodPressure_veryhigh', range=BP_RANGE)
blood_pressure_veryhigh.add(Line((154, 0), (171, 1)))
blood_pressure_veryhigh.add(ConstantValue(start_x=171, end_x=BP_RANGE[1], value=1))

# Define Blood sugar fuzzysets
BS_RANGE = (0, 200)

blood_sugar_veryhigh = FuzzySet(name='bloodSugar_veryhigh', range=BS_RANGE)
blood_sugar_veryhigh.add(Line((105, 0), (120, 1)))
blood_sugar_veryhigh.add(ConstantValue(start_x=120, end_x=BP_RANGE[1], value=1))

# Define cholesterol fuzzysets
CH_RANGE = (0, 600)

cholesterol_low = FuzzySet(name='cholesterol_low', range=CH_RANGE)
cholesterol_low.add(ConstantValue(start_x=CH_RANGE[0], end_x=151, value=1))
cholesterol_low.add(Line((151, 1), (197, 0)))

cholesterol_medium = FuzzySet(name='cholesterol_medium', range=CH_RANGE)
cholesterol_medium.add(Line((188, 0), (215, 1)))
cholesterol_medium.add(Line((215, 1), (250, 0)))

cholesterol_high = FuzzySet(name='cholesterol_high', range=CH_RANGE)
cholesterol_high.add(Line((217, 0), (263, 1)))
cholesterol_high.add(Line((263, 1), (307, 0)))

cholesterol_veryhigh = FuzzySet(name='cholesterol_veryhigh', range=CH_RANGE)
cholesterol_veryhigh.add(Line((281, 0), (347, 1)))
cholesterol_veryhigh.add(ConstantValue(start_x=347, end_x=CH_RANGE[1], value=1))

# Define heartrate fuzzysets
HR_RANGE = (0, 600)

heartrate_low = FuzzySet(name='heartRate_low', range=HR_RANGE)
heartrate_low.add(ConstantValue(start_x=HR_RANGE[0], end_x=100, value=1))
heartrate_low.add(Line((100, 1), (141, 0)))

heartrate_medium = FuzzySet(name='heartRate_medium', range=HR_RANGE)
heartrate_medium.add(Line((111, 0), (152, 1)))
heartrate_medium.add(Line((152, 1), (194, 0)))

heartrate_high = FuzzySet(name='heartRate_high', range=HR_RANGE)
heartrate_high.add(Line((152, 0), (210, 1)))
heartrate_high.add(ConstantValue(start_x=210, end_x=HR_RANGE[1], value=1))

# Define ecg fuzzysets
ECG_RANGE = (-0.5, 2.5)

ecg_normal = FuzzySet(name='ECG_normal', range=ECG_RANGE)
ecg_normal.add(ConstantValue(start_x=ECG_RANGE[0], end_x=0, value=1))
ecg_normal.add(Line((0, 1), (0.4, 0)))

ecg_abnormal = FuzzySet(name='ECG_abnormal', range=ECG_RANGE)
ecg_abnormal.add(Line((0.2, 0), (1, 1)))
ecg_abnormal.add(Line((1, 1), (1.8, 0)))

ecg_hypertrophy = FuzzySet(name='ECG_hypertrophy', range=ECG_RANGE)
ecg_hypertrophy.add(Line((1.4, 0), (1.9, 1)))
ecg_hypertrophy.add(ConstantValue(start_x=1.9, end_x=ECG_RANGE[1], value=1))

# Define old peak fuzzysets
OP_RANGE = (0, 10)

oldpeak_low = FuzzySet(name='oldPeak_low', range=OP_RANGE)
oldpeak_low.add(ConstantValue(start_x=OP_RANGE[0], end_x=1, value=1))
oldpeak_low.add(Line((1, 1), (2, 0)))

oldpeak_risk = FuzzySet(name='oldPeak_risk', range=OP_RANGE)
oldpeak_risk.add(Line((1.5, 0), (2.8, 1)))
oldpeak_risk.add(Line((2.8, 1), (4.2, 0)))

oldpeak_terrible = FuzzySet(name='oldPeak_terrible', range=OP_RANGE)
oldpeak_terrible.add(Line((2.5, 0), (4, 1)))
oldpeak_terrible.add(ConstantValue(start_x=4, end_x=OP_RANGE[1], value=1))

