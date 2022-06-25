from typing import List, Tuple

class RuleParser:

    operators = ['AND', 'OR']

    def __init__(self) -> None:
        pass

    def parse_rule(self, rule: str) -> Tuple[List, str]:
        '''Given a rule in rules.fcl format, returns the if and then clauses as a tuple.
        output format: tuple(if_clause: list, then_clause: str)
        '''
        # split then clause
        splitted_rule = rule.split('THEN')
        then_clause = splitted_rule[1][:-1].strip()
        # split if clause
        if_clause = splitted_rule[0].split('IF')[1].replace('(', '( ').replace(')', ' )').strip()
        if_clause = if_clause.split(' ')
        # loop over if statement to split words and operators
        if_clause_list, current_pair = [], []
        for word in if_clause:
            # do nothing if the word is paranthesis
            if word in ['(', ')']:
                continue
            # if the word is an operator, add the current pair to the list and start a new pair and add the operator to list.
            if word in self.operators:
                if_clause_list.append((current_pair[0], current_pair[1]))
                current_pair = []
                if_clause_list.append(word)
            # if the word is not an operator, add it to the current pair.
            elif word != 'IS':
                current_pair.append(word.strip())

        if len(current_pair) != 0:
            if_clause_list.append((current_pair[0], current_pair[1]))
        return if_clause_list, then_clause