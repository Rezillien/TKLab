#!/usr/bin/python

import scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    # ("nonassoc", 'IFX'),
    # ("nonassoc", 'ELSE'),
    ("right", 'EQUAL', 'PLUSEQUAL', 'MINUSEQUAL', 'MULTIPLEEQUAL', 'DIVIDEEQUAL'),
    # ("left", 'OR'),
    # ("left", 'AND'),
    # ("left", '|'),
    # ("left", '^'),
    # ("left", '&'),
    ("nonassoc", 'ISLESS', 'ISMORE', 'ISLESSOREQUAL', 'ISMOREOREQUAL', 'ISNOTEQUAL', 'ISEQUAL'),
    # ("left", 'SHL', 'SHR'),
    ("left", '+', '-', 'DOTPLUS', 'DOTMINUS'),
    ("left", '*', '/', 'DOTMULTIPLE', 'DOTDIVIDE'),
)




def p_error(p):
    if p:
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_tok_column(p),
                                                                                  p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions"""


def p_instructions(p):
    """instructions : instructions instruction
                | """


def p_instruction(p):
    """instruction : assignment
                | for_instruction
                | while_instruction
                | if_instruction
                | operation
                | print_instruction
                | break_instruction
                | continue_instruction
                | return_instruction
                | compound_instruction
                | assignment_operation"""


def p_assignment(p):
    """assignment : ID EQUAL operation ';' """


def p_for_instruction(p):
    """for_instruction : FOR iterator instruction """

def p_while_instruction(p):
    """while_instruction : WHILE '(' bool_expression ')' instruction """

def p_if_instruction(p):
    """if_instruction : IF '(' bool_expression ')' instruction
                | IF '(' bool_expression ')' instruction ELSE instruction"""

def p_print_instruction(p):
    """print_instruction : PRINT operations ';'"""

def p_operations(p):
    """operations : operations ',' operation
                | operation """

def p_operation(p):
    """operation : num
                | ID
                | operation DOTMINUS operation
                | operation DOTPLUS operation
                | operation DOTMULTIPLE operation
                | operation DOTDIVIDE operation """

def p_break_instruction(p):
    """break_instruction : BREAK ';' """

def p_continue_instruction(p):
    """continue_instruction : CONTINUE ';' """

def p_return_instruction(p):
    """return_instruction : RETURN operation ';'
                | RETURN ';' """

def p_compound_instruction(p):
    """compound_instruction : '{' instructions '}'"""

def p_iterator(p):
    """iterator : ID EQUAL int_or_id ':' int_or_id """

def p_int_or_id(p):
    """int_or_id : ID
                | INT """

def p_num(p):
    """num : FLOAT
                | INT """

def p_bool_expression(p):
    """bool_expression : ID
                | operation ISLESS operation
                | operation ISMORE operation
                | operation ISLESSOREQUAL operation
                | operation ISMOREOREQUAL operation
                | operation ISNOTEQUAL operation
                | operation ISEQUAL operation """

def p_assignment_operation(p):
    """assignment_operation : ID PLUSEQUAL operation
                | ID MINUSEQUAL operation
                | ID MULTIPLEEQUAL operation
                | ID DIVIDEEQUAL operation """




parser = yacc.yacc()

