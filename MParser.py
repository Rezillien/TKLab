# !/bin/python
import AST
from scanner import Scanner


class Parser:

    def __init__(self, debug=False):
        self.scanner = Scanner()
        self.debug = debug
        self.error = False

    tokens = Scanner.tokens

    precedence = (
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
        ('nonassoc', 'PLUS_ASSIGN', 'MINUS_ASSIGN', 'MUL_ASSIGN', 'DIV_ASSIGN'),
        ('right', '='),
        ('nonassoc', '>', '<', 'EQ', 'NEQ', 'GEQ', 'LEQ',),
        ('left', '+', '-', 'DOT_PLUS', 'DOT_MINUS'),
        ('left', '*', '/', 'DOT_MUL', 'DOT_DIV'),
        ('left', '\''),
        ('right', 'UNARY')
    )

    def p_error(self, p):
        if p:
            print("Syntax error at lineno {0}, column {1}: LexToken({2}, '{3}')"
                  .format(p.lineno, self.scanner.find_column(p), p.type, p.value))
        else:
            print("Unexpected end of input")
        self.error = True

    def p_start(self, p):
        """start : INSTRUCTIONS"""
        p[0] = AST.Program(p[1], p.lineno(1))
        if self.debug:
            print('p_start: {}'.format(p[0]))

    def p_instructions(self, p):
        """INSTRUCTIONS : INSTRUCTIONS INSTRUCTION
                        | INSTRUCTION"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[1].append(p[2])
            p[0] = p[1]
        if self.debug:
            print('p_instructions: {}'.format(p[0]))

    def p_instruction(self, p):
        """INSTRUCTION : STATEMENT ';'
                       | BLOCK_STATEMENT
                       | IF_STATEMENT
                       | WHILE_STATEMENT
                       | FOR_STATEMENT"""
        p[0] = p[1]
        if self.debug:
            print('p_instruction: {}'.format(p[0]))

    def p_statement(self, p):
        """STATEMENT : ASSIGNMENT
                     | KEYWORD"""
        p[0] = p[1]
        if self.debug:
            print('p_statement: {}'.format(p[0]))

    def p_assignment(self, p):
        """ASSIGNMENT : LEFT_ASSIGNMENT '=' EXPRESSION
                      | LEFT_ASSIGNMENT PLUS_ASSIGN EXPRESSION
                      | LEFT_ASSIGNMENT MINUS_ASSIGN EXPRESSION
                      | LEFT_ASSIGNMENT MUL_ASSIGN EXPRESSION
                      | LEFT_ASSIGNMENT DIV_ASSIGN EXPRESSION"""
        p[0] = AST.Assignment(p[1], p[2], p[3], p[1].lineno)
        if self.debug:
            print('p_assignment: {}'.format(p[0]))

    def p_left_assignment(self, p):
        """LEFT_ASSIGNMENT : CONST_ID
                           | ACCESS"""
        p[0] = AST.AssignTo(p[1], p[1].lineno)
        if self.debug:
            print('p_left_assignment: {}'.format(p[0]))

    def p_access(self, p):
        """ACCESS : CONST_ID '[' SEQUENCE ']'"""
        p[0] = AST.Access(p[1], p[3], p[1].lineno)
        if self.debug:
            print('p_access: {}'.format(p[0]))

    def p_sequence(self, p):
        """SEQUENCE : SEQUENCE ',' EXPRESSION
                    | EXPRESSION"""
        if len(p) == 2:
            p[0] = AST.Sequence([p[1]], p[1].lineno)
        elif len(p) == 4:
            p[1].append(p[3])
            p[0] = p[1]
        if self.debug:
            print('p_sequence: {}'.format(p[0]))

    def p_value(self, p):
        """VALUE : CONST_VALUE
                 | MATRIX
                 | ACCESS
                 | CONST_ID"""
        p[0] = p[1]
        if self.debug:
            print('p_value: {}'.format(p[0]))

    def p_const_value(self, p):
        """CONST_VALUE : FLOAT
                       | INT
                       | STRING"""
        p[0] = AST.ConstValue(p[1], p.lineno(1))
        if self.debug:
            print('p_const_value: {}'.format(p[0]))

    def p_const_id(self, p):
        """CONST_ID : ID"""
        p[0] = AST.ID(p[1], p.lineno(1))
        if self.debug:
            print('p_const_id: {}'.format(p[0]))

    def p_matrix(self, p):
        """MATRIX : '[' ROWS ']'"""
        p[0] = AST.Matrix(p[2], p.lineno(1))
        if self.debug:
            print('p_matrix: {}'.format(p[0]))

    def p_rows(self, p):
        """ROWS : ROWS ';' SEQUENCE
                | SEQUENCE"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[1].append(p[3])
            p[0] = p[1]
        if self.debug:
            print('p_rows: {}'.format(p[0]))

    def p_expression_matrix(self, p):
        """EXPRESSION : EXPRESSION DOT_PLUS EXPRESSION
                      | EXPRESSION DOT_MINUS EXPRESSION
                      | EXPRESSION DOT_MUL EXPRESSION
                      | EXPRESSION DOT_DIV EXPRESSION"""
        p[0] = AST.Expression(p[1], p[2], p[3], p[1].lineno)
        if self.debug:
            print('p_expression: {}'.format(p[0]))

    def p_math_math(self, p):
        """EXPRESSION : EXPRESSION '+' EXPRESSION
                      | EXPRESSION '-' EXPRESSION
                      | EXPRESSION '*' EXPRESSION
                      | EXPRESSION '/' EXPRESSION"""
        p[0] = AST.Expression(p[1], p[2], p[3], p[1].lineno)
        if self.debug:
            print('p_expression: {}'.format(p[0]))

    def p_expression_function(self, p):
        """EXPRESSION : EYE '(' EXPRESSION ')'
                      | ZEROS '(' EXPRESSION ')'
                      | ONES '(' EXPRESSION ')'"""
        p[0] = AST.Function(p[1], p[3], p.lineno(1))
        if self.debug:
            print('p_expression: {}'.format(p[0]))

    def p_expression_transopse(self, p):
        """EXPRESSION : EXPRESSION "'" """
        p[0] = AST.Transposition(p[1], p[1].lineno)
        if self.debug:
            print('p_expression: {}'.format(p[0]))

    def p_expression_value(self, p):
        """EXPRESSION : VALUE"""
        p[0] = p[1]
        if self.debug:
            print('p_expression: {}'.format(p[0]))

    def p_expression_group(self, p):
        """EXPRESSION : '(' EXPRESSION ')'"""
        p[0] = p[2]
        if self.debug:
            print('p_expression: {}'.format(p[0]))

    def p_expression_unary(self, p):
        """EXPRESSION : '-' EXPRESSION %prec UNARY"""
        p[0] = AST.Negation(p[2], p.lineno(1))
        if self.debug:
            print('p_expression: {}'.format(p[0]))

    def p_keyword(self, p):
        """KEYWORD : PRINT SEQUENCE
                   | BREAK
                   | CONTINUE
                   | RETURN EXPRESSION"""
        if p[1] == 'print':
            p[0] = AST.Print(p[2], p.lineno(1))
        elif p[1] == 'return':
            p[0] = AST.Return(p[2], p.lineno(1))
        elif p[1] == 'break':
            p[0] = AST.Break(p.lineno(1))
        elif p[1] == 'continue':
            p[0] = AST.Continue(p.lineno(1))
        if self.debug:
            print('p_keyword: {}'.format(p[0]))

    def p_condition(self, p):
        """CONDITION : EXPRESSION '<' EXPRESSION
                     | EXPRESSION '>' EXPRESSION
                     | EXPRESSION EQ EXPRESSION
                     | EXPRESSION NEQ EXPRESSION
                     | EXPRESSION GEQ EXPRESSION
                     | EXPRESSION LEQ EXPRESSION"""
        p[0] = AST.Condition(p[1], p[2], p[3], p[1].lineno)
        if self.debug:
            print('p_condition: {}'.format(p[0]))

    def p_block_statement(self, p):
        """BLOCK_STATEMENT : '{' INSTRUCTIONS '}'"""
        p[0] = AST.Instructions(p[2], p.lineno(1))
        if self.debug:
            print('p_block_statement: {}'.format(p[0]))

    def p_if_statement(self, p):
        """IF_STATEMENT : IF '(' CONDITION ')' INSTRUCTION %prec IFX
                        | IF '(' CONDITION ')' INSTRUCTION ELSE INSTRUCTION"""
        if len(p) == 8:
            p[0] = AST.IfElse(p[3], p[5], p[7], p.lineno(1))
        elif len(p) == 6:
            p[0] = AST.If(p[3], p[5], p.lineno(1))
        if self.debug:
            print('p_if_statement: {}'.format(p[0]))

    def p_while_statement(self, p):
        """WHILE_STATEMENT : WHILE '(' CONDITION ')' INSTRUCTION"""
        p[0] = AST.While(p[3], p[5], p.lineno(1))
        if self.debug:
            print('p_while_statement: {}'.format(p[0]))

    def p_for_statement(self, p):
        """FOR_STATEMENT : FOR CONST_ID '=' RANGE INSTRUCTION"""
        p[0] = AST.For(p[2], p[4], p[5], p.lineno(1))
        if self.debug:
            print('p_for_statement: {}'.format(p[0]))

    def p_range(self, p):
        """RANGE : EXPRESSION ':' EXPRESSION
                 | EXPRESSION ':' EXPRESSION ':' EXPRESSION"""
        if len(p) == 4:
            p[0] = AST.Range(p[1], p[3], p[1].lineno)
        elif len(p) == 6:
            p[0] = AST.Range(p[1], p[3], p[1].lineno, jump=p[5])
        if self.debug:
            print('p_range: {}'.format(p[0]))
