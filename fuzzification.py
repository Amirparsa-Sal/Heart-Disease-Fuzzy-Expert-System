from abc import abstractmethod, ABC
from typing import Tuple, List
import matplotlib.pyplot as plt
import numpy as np

class FuzzySetSection(ABC):
    '''This is a class to define a section in a fuzzyset. this section can be a line or anything.'''

    @abstractmethod
    def range(self) -> Tuple:
        '''Returns the range of the section.'''
        pass
    
    @abstractmethod
    def get_value(self, x: float) -> float:
        '''Returns the value of the section at x.'''
        pass

class Point(FuzzySetSection):
    '''This is a class to define a point in a fuzzyset. this section can be a point.'''

    def __init__(self, x: float, value: float):
        self.x = x
        self.value = value

    def range(self) -> Tuple:
        return (self.x, self.x)

    def get_value(self, x: float) -> float:
        return self.value

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

    def get_value(self, x: float) -> float:
        return self.m * x + self.b
    
    def range(self) -> Tuple:
        return self.start_pos[0], self.end_pos[0]
    
    def __find_line_paramaters(self, x1: int, y1: int, x2: int, y2: int) -> Tuple:
        weights = np.array([[x1, 1], [x2, 1]])
        out = np.array([y1, y2])
        result = np.linalg.solve(weights, out)
        return result[0], result[1]

def linspace(start: float, end: float, stride: int) -> List:
    '''Returns a list of floats between start and end with stride.'''
    return [start + i * stride for i in range(int((end - start) / stride) + 1)]

class FuzzySet:
    '''This is a class to define a fuzzyset.'''
    def __init__(self, name:str) -> None:
        self.name = name
        self.parameter = None
        self.sections = []
        self.not_continous_points = []

    def add(self, section: FuzzySetSection) -> None:
        '''Adds a section to the fuzzyset.'''
        # Check if the section has an intersection with other sections
        for s in self.sections:
            if self.__has_interception(s.range(), section.range()):
                raise ValueError('Interception between sections')
        if isinstance(section, Point):
            self.not_continous_points.append(section.x)
        self.sections.append(section)
    
    def get_value(self, x: float) -> float:
        '''Returns the value of the fuzzyset at x.'''
        # raise error if x is not in the range and x is assigned to a parameter
        if self.parameter:
            if x < self.parameter.range[0] or x > self.parameter.range[1]:
                return ValueError('x out of range')
        # find the section that contains x to get the value
        for section in self.sections:
            if section.range()[0] <= x <= section.range()[1]:
                return section.get_value(x)
        return 0

    def __has_interception(self, range1: Tuple, range2: Tuple) -> bool:
        if range2[0] < range1[1] < range2[1] or range1[0] < range2[1] < range1[1]:
            return True
        return False

class FuzzyParameter:
    '''This is a class to define a fuzzy parameter.'''

    def __init__(self, name: str, range: Tuple, name_in_rules=None):
        self.name = name
        self.name_in_rules = name_in_rules if name_in_rules else self.name
        self.range = range
        self.sets = dict()
    
    def create_set(self, name: str, points: list) -> None:
        '''Creates a fuzzyset with the given name and points to draw a line.'''
        if name in self.sets:
            raise ValueError('Set already exists')
        our_set = FuzzySet(name)
        for i in range(len(points) - 1):
            our_set.add(Line((points[i][0], points[i][1]), (points[i+1][0], points[i+1][1])))
        self.sets[our_set.name] = our_set
        our_set.parameter = self

    def add_set(self, our_set: FuzzySet) -> None:
        '''Adds a fuzzyset to the parameter.'''
        self.sets[our_set.name] = our_set
        our_set.parameter = self
    
    def plot(self) -> None:
        '''Plots the parameter's fuzzysets.'''
        x = linspace(self.range[0], self.range[1], 0.005)
        for set_name, set in self.sets.items():
            y = [set.get_value(_x) for _x in x]
            plt.plot(x, y, label=f'{self.name}_{set_name}')
        plt.legend(loc='best')
        plt.title(f'{self.name}')
        plt.show()
    
    def get_value(self, x: float) -> dict:
        '''Returns the value of the parameter at x for every fuzzysets.'''
        result = dict()
        for set_name, set in self.sets.items():
            result[set_name] = set.get_value(x)
        return result
    
    def get_value_in_set(self, x: float, set_name: str) -> float:
        '''Returns the value of the parameter at x in the fuzzyset with the given name.'''
        return self.sets[set_name].get_value(x)
    
    def __str__(self) -> str:
        return f'{self.name}: sets: {len(self.sets)}'

def init_fuzzy_parameters() -> List[FuzzyParameter]:
    '''Initializes the fuzzy parameters.'''

    # define chest pain fuzzysets
    CP_RANGE = (1, 4)
    
    chest_typical_anginal = FuzzySet('typical_anginal')
    chest_typical_anginal.add(Point(1, 1))
    
    chest_atypical_anginal = FuzzySet('atypical_anginal')
    chest_atypical_anginal.add(Point(2, 1))

    chest_non_anginal = FuzzySet('non_aginal_pain')
    chest_non_anginal.add(Point(3, 1))

    chest_asymptomatic = FuzzySet('asymptomatic')
    chest_asymptomatic.add(Point(4, 1))

    chest_pain_param = FuzzyParameter('chestPain', CP_RANGE, name_in_rules='chest_pain')
    chest_pain_param.add_set(chest_typical_anginal)
    chest_pain_param.add_set(chest_atypical_anginal)
    chest_pain_param.add_set(chest_non_anginal)
    chest_pain_param.add_set(chest_asymptomatic)

    # Define age fuzzysets
    AGE_RANGE = (0, 100)

    age_param = FuzzyParameter(name='age', range=AGE_RANGE)
    age_param.create_set('young', [(AGE_RANGE[0], 1), (29, 1), (38, 0)])
    age_param.create_set('mild', [(33, 0), (38, 1), (45, 0)])
    age_param.create_set('old', [(40, 0), (48, 1), (58, 0)])
    age_param.create_set('veryold', [(52, 0), (60, 1), (AGE_RANGE[1], 1)])

    # Define Blood pressure fuzzysets
    BP_RANGE = (0, 350)

    blood_pressure_param = FuzzyParameter(name='bloodPressure', range=BP_RANGE, name_in_rules='blood_pressure')
    blood_pressure_param.create_set('low', [(BP_RANGE[0], 1), (111, 1), (134, 0)])
    blood_pressure_param.create_set('medium', [(127, 0), (139, 1), (153, 0)])
    blood_pressure_param.create_set('high', [(153, 0), (157, 1), (172, 0)])
    blood_pressure_param.create_set('veryhigh', [(154, 0), (171, 1), (BP_RANGE[1], 1)])

    # Define Blood sugar fuzzysets
    BS_RANGE = (0, 200)

    blood_sugar_param = FuzzyParameter(name='bloodSugar', range=BS_RANGE, name_in_rules='blood_sugar')
    blood_sugar_param.create_set('low', [(105, 0), (120, 1), (BS_RANGE[1], 1)])

    # Define cholesterol fuzzysets
    CH_RANGE = (0, 600)

    cholesterol_param = FuzzyParameter(name='cholesterol', range=CH_RANGE)
    cholesterol_param.create_set('low', [(CH_RANGE[0], 1), (151, 1), (197, 0)])
    cholesterol_param.create_set('medium', [(188, 0), (215, 1), (250, 0)])
    cholesterol_param.create_set('high', [(217, 0), (263, 1), (307, 0)])
    cholesterol_param.create_set('veryhigh', [(281, 0), (347, 1), (CH_RANGE[1], 1)])

    # Define heartrate fuzzysets
    HR_RANGE = (0, 600)

    heartrate_param = FuzzyParameter(name='heartRate', range=HR_RANGE, name_in_rules='maximum_heart_rate')
    heartrate_param.create_set('low', [(HR_RANGE[0], 1), (100, 1), (141, 0)])
    heartrate_param.create_set('medium', [(111, 0), (152, 1), (194, 0)])
    heartrate_param.create_set('high', [(152, 0), (210, 1), (HR_RANGE[1], 1)])

    # Define exercise fuzzysets
    CP_RANGE = (0, 1)
    
    exercise_false = FuzzySet('false')
    exercise_false.add(Point(0, 1))

    exercise_true = FuzzySet('true')
    exercise_true.add(Point(1, 1))

    exercise_param = FuzzyParameter('exercise', CP_RANGE)
    exercise_param.add_set(exercise_false)
    exercise_param.add_set(exercise_true)

    # Define thallium fuzzysets
    T_RANGE = (3, 7)
    thallium_normal = FuzzySet('normal')
    thallium_normal.add(Point(3, 1))

    thallium_medium = FuzzySet('medium')
    thallium_medium.add(Point(6, 1))

    thallium_high = FuzzySet('high')
    thallium_high.add(Point(7, 1))

    thallium_param = FuzzyParameter('thallium', T_RANGE)
    thallium_param.add_set(thallium_normal)
    thallium_param.add_set(thallium_medium)
    thallium_param.add_set(thallium_high)
    print(thallium_param.get_value(6))
    thallium_param.plot()

    # Define sex fuzzysets
    SEX_RANGE = (0, 1)

    sex_male = FuzzySet('male')
    sex_male.add(Point(0, 1))

    sex_female = FuzzySet('female')
    sex_female.add(Point(1, 1))

    sex_param = FuzzyParameter('sex', SEX_RANGE)
    sex_param.add_set(sex_male)
    sex_param.add_set(sex_female)

    # Define ecg fuzzysets
    ECG_RANGE = (-0.5, 2.5)

    ecg_param = FuzzyParameter(name='ECG', range=ECG_RANGE)
    ecg_param.create_set('normal', [(ECG_RANGE[0], 1), (0, 1), (0.4, 0)])
    ecg_param.create_set('abnormal', [(0.2, 0), (1, 1), (1.8, 0)])
    ecg_param.create_set('hypertrophy', [(1.4, 0), (1.9, 1), (ECG_RANGE[1], 1)])

    # Define old peak fuzzysets
    OP_RANGE = (0, 10)

    oldpeak_param = FuzzyParameter(name='oldPeak', range=OP_RANGE, name_in_rules='old_peak')
    oldpeak_param.create_set('low', [(OP_RANGE[0], 1), (1, 1), (2, 0)])
    oldpeak_param.create_set('risk', [(1.5, 0), (2.8, 1), (4.2, 0)])
    oldpeak_param.create_set('terrible', [(2.5, 0), (4, 1), (OP_RANGE[1], 1)])

    return [chest_pain_param, blood_pressure_param, cholesterol_param, blood_sugar_param,
           ecg_param, heartrate_param, exercise_param, oldpeak_param, thallium_param, age_param]

def init_output_fuzzy_sets():
    # Define output fuzzysets
    output_param = FuzzyParameter(name='output', range=(0, 1))
    output_param.create_set('sick1', [(0, 1), (0.25, 1), (1, 0)])
    output_param.create_set('sick2', [(0, 0), (1, 1), (2,0)])
    output_param.create_set('sick3', [(1, 0), (2, 1), (3,0)])
    output_param.create_set('sick4', [(2, 0), (3, 1), (4,0)])
    output_param.create_set('healthy', [(3, 0), (3.75, 1), (4, 1)])
    return output_param

if __name__ == '__main__':
    params = init_fuzzy_parameters()
    for param in params:
        param.plot()