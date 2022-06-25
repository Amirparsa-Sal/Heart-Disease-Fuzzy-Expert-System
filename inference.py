from fuzzification import init_fuzzy_parameters
from abc import ABC, abstractmethod
from typing import Tuple, List
from dataclasses import dataclass
from rule_parser import RuleParser

class FuzzyOperator(ABC):
    def __init__(self, name: str) -> None:
        self.name = name
    
    @abstractmethod
    def get_fuzzy_value(self, operand1:float, operand2:float) -> float:
        pass

class AndOperator(FuzzyOperator):
    def __init__(self) -> None:
        super().__init__('AND')
    
    def get_fuzzy_value(self, operand1: float, operand2: float) -> float:
        return min(operand1, operand2)

class OrOperator(FuzzyOperator):
    def __init__(self) -> None:
        super().__init__('OR')
    
    def get_fuzzy_value(self, operand1: float, operand2: float) -> float:
        return max(operand1, operand2)

class OperatorFactory:
    operators = {'AND': AndOperator(), 'OR': OrOperator()}
    
    @classmethod
    def get_operator(self, operator_name: str) -> FuzzyOperator:
        return self.operators[operator_name]

@dataclass
class RuleTerm:
    parameter_name: str
    fuzzyset_name: str

class Rule:
    def __init__(self, if_clause: List, then_clause: Tuple) -> None:
        self.if_clause_items = []
        self.operator = None
        for term in if_clause:
            if isinstance(term, Tuple):
                self.if_clause_items.append(RuleTerm(term[0], term[1]))
            elif not self.operator:
                self.operator = OperatorFactory.get_operator(term)
            
        self.then_clause_item = RuleTerm(then_clause[0], then_clause[1])
    
    def __str__(self) -> str:
        return '{} {} {}'.format(self.if_clause_items, self.operator, self.then_clause_item)

class FuzzyIntelligentSystem:
    
    def __init__(self, rules_file='rules.fcl') -> None:
        self.fuzzy_rules = []
        self.__extract_rules(rules_file)
        self.fuzzy_parameters = dict()
        for param in init_fuzzy_parameters():
            self.fuzzy_parameters[param.name] = param

    def __extract_rules(self, rules_file) -> None:
        with open(rules_file, 'r') as f:
            for line in f:
                if_clause, then_clause = RuleParser.parse_rule(line[:-1])
                self.fuzzy_rules.append(Rule(if_clause, then_clause))
    
fs = FuzzyIntelligentSystem()
fs.extract_rules()
print(fs.rules[0])