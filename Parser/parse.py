import ply.yacc as yacc
import sys
from lex import tokens
import networkx as nx
import matplotlib.pyplot as plt

import graphviz

class Node:
    def __init__(self, my_operation, my_kids, i):
        self.operation = my_operation
        self.kids = my_kids
        self.id = i

class Result:
    def __init__(self):
        self.start_nonterm = []
        self.node_names = []
        self.used_nodes = []
        self.graph = graphviz.Graph(format='png')
        self.num_of_nodes = 0
    def add_node(self, nd):
        self.graph.node(str(self.num_of_nodes), nd.operation)
        self.num_of_nodes += 1
        for element in nd.kids:
            self.graph.edge(str(nd.id), str(element.id))
    def print_nonterm(self):
        if len(self.start_nonterm) != 1:
            raise Exception("Incorrect number of start nonterm")
        if self.start_nonterm[0] not in self.node_names:
            raise Exception("Start node ID is not defined")
        print("Non terminal is " + self.start_nonterm[0])
    def check_nondefined(self):
        for all_used in self.used_nodes:
            if all_used not in self.node_names:
                raise Exception("It is undefined ID - " + all_used)

def p_lang(p):
    '''Language : Rule
                | Start_nonterm
                | COMMENT'''

def p_rule(p):
    ''' Rule : ID EQUALITY Expr '''
    p[0] = Node("ID: " + p[1], [p[3]], parser.my_result.num_of_nodes)
    parser.my_result.add_node(p[0])
    parser.my_result.node_names.append(p[1])

def p_start(p):
    ''' Start_nonterm : START EQUALITY ID '''
    parser.my_result.start_nonterm.append(p[3])

def p_expr_symbol(p):
    ''' Expr : SYMBOL '''
    p[0] = Node("Symbol: " + p[1], [], parser.my_result.num_of_nodes)
    parser.my_result.add_node(p[0])

def p_expr_epsilon(p):
    ''' Expr : EPSILON '''
    p[0] = Node("Symbol: Epsilon", [], parser.my_result.num_of_nodes)
    parser.my_result.add_node(p[0])

def p_expr_arg(p):
    ''' Expr : ID
             | L_BRACKETS Expr R_BRACKETS
             | Expr MULT
    '''
    if len(p) == 2:
        p[0] = Node("ID: " + p[1], [], parser.my_result.num_of_nodes)
        parser.my_result.used_nodes.append(p[1])
        parser.my_result.add_node(p[0])
    elif len(p) == 3:
        p[0] = Node("*", [p[1]], parser.my_result.num_of_nodes)
        parser.my_result.add_node(p[0])
    elif len(p) == 4:
        p[0] = p[2]
def p_sqr_brkts(p):
    ''' Expr : L_SQUARE Expr R_SQUARE '''
    p[0] = Node("[]", [p[2]], parser.my_result.num_of_nodes)
    parser.my_result.add_node(p[0])

def p_expr_args_plus(p):
    ''' Expr : Expr PLUS Expr '''
    p[0] = Node("+", [p[1], p[3]], parser.my_result.num_of_nodes)
    parser.my_result.add_node(p[0])

def p_expr_args_alt(p):
    ''' Expr : Expr ALT Expr '''
    p[0] = Node("|", [p[1], p[3]], parser.my_result.num_of_nodes)
    parser.my_result.add_node(p[0])

# def p_expr_exception_oper(p):
#     ''' Expr : Expr Expr '''
#     raise Exception("Expect operator between two expressions: \"" + p[1].operation + "\" and \"" + p[2].operation + "\"")

def p_error(p):
    raise Exception("Syntax error at symbol ", p)

parser = yacc.yacc()

parser.my_result = Result()
parser.is_ok = True

sys.stdin = open(sys.argv[1], 'r')
sys.stdout = open(sys.argv[1] + '.out', 'w')

while True:
    try:
        s = input()
    except EOFError:
        break
    if not s:
        continue
    try:
        result = parser.parse(s)
    except Exception as e:
        print("Error: " + str(e))
        parser.is_ok = False
        break

if parser.is_ok:
    try:
        parser.my_result.check_nondefined()
        parser.my_result.print_nonterm()
        parser.my_result.graph.render(sys.argv[1] + ".graph", view=True)
    except Exception as e:
        print("Error: " + str(e))
        parser.is_ok = False

