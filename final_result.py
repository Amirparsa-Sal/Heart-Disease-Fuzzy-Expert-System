from unittest import result
from inference import FuzzyIntelligentSystem

class ProvideResult(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ProvideResult, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def get_final_result(input_dict: dict) -> str:
        fs = FuzzyIntelligentSystem()
        result = fs.calculate_result(input_dict)
        message = fs.get_health_status(result)
        return f'{message}: {result}'