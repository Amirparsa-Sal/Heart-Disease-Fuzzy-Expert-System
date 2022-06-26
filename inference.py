from ast import operator
from fuzzification import init_fuzzy_parameters, init_output_fuzzy_sets
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
        self.then_clause_item = RuleTerm(then_clause[0], then_clause[1])
        self.operator = None
        for term in if_clause:
            if isinstance(term, Tuple):
                self.if_clause_items.append(RuleTerm(term[0], term[1]))
            elif not self.operator:
                self.operator = OperatorFactory.get_operator(term)
    
    def __str__(self) -> str:
        return '{} {} {}'.format(self.if_clause_items, self.operator, self.then_clause_item)

class FuzzyIntelligentSystem:
    
    def __init__(self, rules_file='rules.fcl') -> None:
        self.fuzzy_rules = []
        self.__extract_rules(rules_file)
        self.fuzzy_parameters = dict()
        self.output_param = init_output_fuzzy_sets()
        for param in init_fuzzy_parameters():
            self.fuzzy_parameters[param.name_in_rules] = param

    def __extract_rules(self, rules_file) -> None:
        with open(rules_file, 'r') as f:
            for line in f:
                if_clause, then_clause = RuleParser.parse_rule(line[:-1])
                self.fuzzy_rules.append(Rule(if_clause, then_clause))

    def calculate_result(self, input_dict: dict) -> float:
        max_values = dict()
        for key in self.output_param.sets.keys():
            max_values[key] = 0
        for rule in self.fuzzy_rules:
            result_value = 0
            term = rule.if_clause_items[0]
            if term.parameter_name in input_dict:
                if term.parameter_name in self.fuzzy_parameters:
                    result_value = self.fuzzy_parameters[term.parameter_name].get_value_in_set(
                    int(input_dict[term.parameter_name]), term.fuzzyset_name)
                else:
                    raise ValueError(f'Parameter {term.parameter_name} is not in fuzzy parameters')
            else:
                raise ValueError(f'Parameter {term.parameter_name} is not in input dict')
            
            for i, term in enumerate(rule.if_clause_items[1:]):
                if term.parameter_name in input_dict:
                    if term.parameter_name in self.fuzzy_parameters:
                        term_value = self.fuzzy_parameters[term.parameter_name].get_value_in_set(
                            int(input_dict[term.parameter_name]), term.fuzzyset_name)
                        result_value = rule.operator.get_fuzzy_value(result_value, term_value)
                    else:
                        raise ValueError(f'Parameter {term.parameter_name} is not in fuzzy parameters')
                else:
                    raise ValueError(f'Parameter {term.parameter_name} is not in input dict')

            if result_value > max_values[rule.then_clause_item.fuzzyset_name]:
                max_values[rule.then_clause_item.fuzzyset_name] = result_value
        return max_values
