from fuzzification import init_fuzzy_parameters, init_output_fuzzy_sets
from abc import ABC, abstractmethod
from typing import Tuple, List
from dataclasses import dataclass
from rule_parser import RuleParser

class FuzzyOperator(ABC):
    '''An abstract class to represent a fuzzy operator'''
    def __init__(self, name: str) -> None:
        self.name = name
    
    @abstractmethod
    def get_fuzzy_value(self, operand1:float, operand2:float) -> float:
        '''Calculate the fuzzy value of 2 operands.'''
        pass

class AndOperator(FuzzyOperator):
    '''A class to represent the AND operator'''
    def __init__(self) -> None:
        super().__init__('AND')
    
    def get_fuzzy_value(self, operand1: float, operand2: float) -> float:
        return min(operand1, operand2)

class OrOperator(FuzzyOperator):
    '''A class to represent the OR operator'''
    def __init__(self) -> None:
        super().__init__('OR')
    
    def get_fuzzy_value(self, operand1: float, operand2: float) -> float:
        return max(operand1, operand2)

class OperatorFactory:
    '''A class to create fuzzy operators.'''
    operators = {'AND': AndOperator(), 'OR': OrOperator()}
    
    @classmethod
    def get_operator(self, operator_name: str) -> FuzzyOperator:
        return self.operators[operator_name]

@dataclass
class RuleTerm:
    '''A class to represent a rule term which is a tuple like (parameter_name, fuzzyset_name)'''
    parameter_name: str
    fuzzyset_name: str

class Rule:
    '''A class to represent a rule which has a if clause, a then clause and an operator.'''
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
    '''A class to represent a fuzzy intelligent system. this class is used to calculate 
    the fuzzy values of the output parameters'''

    def __init__(self, rules_file='rules.fcl') -> None:
        self.fuzzy_rules = [] # type: List[Rule]
        self.__extract_rules(rules_file) 
        self.fuzzy_parameters = dict()
        self.output_param = init_output_fuzzy_sets()
        for param in init_fuzzy_parameters():
            self.fuzzy_parameters[param.name_in_rules] = param

    def __extract_rules(self, rules_file) -> None:
        '''Extract rules from a file.'''
        with open(rules_file, 'r') as f:
            # loop through each line
            for line in f:
                # parse the line to get the if clause and then clause
                if_clause, then_clause = RuleParser.parse_rule(line[:-1])
                # create a rule
                self.fuzzy_rules.append(Rule(if_clause, then_clause))

    def calculate_result(self, input_dict: dict) -> float:
        '''Calculate the fuzzy value of the output parameter given an input dictionary.'''
        # init max_value for each output fuzzy set
        max_values = dict()
        for key in self.output_param.sets.keys():
            max_values[key] = 0
        # calculate the output with respect to the rules
        for rule in self.fuzzy_rules:
            result_value = 0
            term = rule.if_clause_items[0]
            # calculate the result for the first term in the if clause
            if term.parameter_name in input_dict:
                # check if the parameter is in the fuzzy system or not
                if term.parameter_name in self.fuzzy_parameters:
                    # if the parameter is in the fuzzy system, calculate the fuzzy value
                    result_value = self.fuzzy_parameters[term.parameter_name].get_value_in_set(
                        int(input_dict[term.parameter_name]), term.fuzzyset_name)
                else:
                    raise ValueError(f'Parameter {term.parameter_name} is not in fuzzy parameters')
            else:
                raise ValueError(f'Parameter {term.parameter_name} is not in input dict')
            
            # calculate the result for the rest of the terms in the if clause
            for i, term in enumerate(rule.if_clause_items[1:]):
                # check if the parameter is in the input dictionary or not
                if term.parameter_name in input_dict:
                    # check if the parameter is in the fuzzy system or not
                    if term.parameter_name in self.fuzzy_parameters:
                        # if the parameter is in the fuzzy system, calculate the fuzzy value
                        term_value = self.fuzzy_parameters[term.parameter_name].get_value_in_set(
                            int(input_dict[term.parameter_name]), term.fuzzyset_name)
                        # update the result value using the fuzzy operator
                        result_value = rule.operator.get_fuzzy_value(result_value, term_value)
                    else:
                        raise ValueError(f'Parameter {term.parameter_name} is not in fuzzy parameters')
                else:
                    raise ValueError(f'Parameter {term.parameter_name} is not in input dict')

            # update the max value of the output fuzzy set if the result is greater than the current max value
            if result_value > max_values[rule.then_clause_item.fuzzyset_name]:
                max_values[rule.then_clause_item.fuzzyset_name] = result_value
        return max_values
