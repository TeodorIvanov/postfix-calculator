import math, operator


class Expression:
    """Represents an expression in the expression history."""
    def __init__(self, expr=''):
        """initialize an expression"""
        self.expr = expr
        #global last_id     #TODO:Implement unique IDs for each entry in expression history
        #last_id +=1
        #self.id = last_id


class History:
    """Represents a collection of expressions that can be displayed"""
    def __init__(self):
        """Initialize the expression history with an empty list."""
        self.expr_history = []

    def new_expr(self, expr):
        """Create a new expression and add it to expr history."""
        self.expr_history.append(Expression(expr))


class Calc:
    def __init__(self):
        self.infix_expr = ""

    def parse_tokens(self, tokens):
        for op in self.single_character_operators:
            tokens = tokens.replace(op, " " + op + " ")
        return tokens.split()

    single_character_operators = ['+', '-', '*', '/', ',', '(', ')']

    constants = {'pi': math.pi,
                 'e': math.e
                  }

    prec = { "*": 2,    #operator precedence
             "/": 2,
             "+": 1,
             "-": 1
             }

    operators = list(prec.keys())

    ops = {'+': operator.add,
           '-': operator.sub,
           '*': operator.mul,
           '/': operator.truediv,
           'pow': operator.pow,
           'log': lambda base, x: math.log(x, base)
           }

    ops_1_args = {'sin': math.sin,
                  'tan': math.tan,
                  'cos': math.cos,
                  'cot': lambda a: ((math.cos(a))/(math.sin(a))),
                  'sqrt': math.sqrt
                    }

    def is_number(self, token):
        if token.isdigit() or token in self.constants:
            return True
        try:
            float(token)
            return True
        except:
            return False

    def is_function(self, token):
        return (not self.is_number(token)) and (token not in self.single_character_operators)

    def infix_to_postfix(self, infix_expr):
        '''Converts infix expressions to postfix expressions'''
        output_queue = []
        op_stack = []   #using a list-based operator stack
        token_list = self.parse_tokens(infix_expr)

        for token in token_list:
            if self.is_number(token):       #checking if the token is a number
                output_queue.append(token)
            elif self.is_function(token):   #checking if the token is a function
                op_stack.append(token)
            elif token == ',':
                while op_stack[-1] != '(':
                    output_queue.append(op_stack.pop())
            elif token in self.operators:   #checking if the token is an operator
                while ((op_stack != []) and
                       (op_stack[-1] in self.operators) and
                       (self.prec[token] <= self.prec[op_stack[-1]])):
                    output_queue.append(op_stack.pop())
                op_stack.append(token)
            elif token == '(':
                op_stack.append(token)
            elif token == ')':
                while op_stack[-1] != '(':
                    output_queue.append(op_stack.pop())
                op_stack.pop()
                if self.is_function(op_stack[-1]):
                    output_queue.append(op_stack.pop())

        while op_stack != []:
            output_queue.append(op_stack.pop())

        return output_queue




    def calculate(self, postfix_expr):    #calculating final result from RPN expression
        '''Calculates the final result from a postfix expression'''
        stack = []
        result = 0
        for i in postfix_expr:
            if i in self.constants:
                i = self.constants[str(i)]
                stack.insert(0, i)
            elif self.is_number(i):
                stack.insert(0, i)
            else:
                if i == '-' and len(stack) == 1:  #implementing negation
                    result = -float(stack.pop(0))
                    stack.insert(0,str(result))
                elif i in self.ops and len(stack) >= 2:  #functions and operators with 2 arguments
                    n1 = float(stack.pop(1))
                    n2 = float(stack.pop(0))
                    result = self.ops[i](n1,n2)
                    stack.insert(0,str(result))
                elif i in self.ops_1_args:         #functions with 1 argument
                    n1 = float(stack.pop(0))
                    result = self.ops_1_args[i](n1)
                    stack.insert(0, str(result))

        if result == int(result):
            result = int(result)
        return result
