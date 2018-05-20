#!/usr/bin/python
import AST
import scanner
import ply.yacc as yacc


class Mparser(object):
    def __init__(self):
        self.scanner = scanner
        # self.scanner.build()

    #
    tokens = scanner.tokens

    level = 0

    precedence = (
        ("right", '=', 'EQUAL', 'PLUSEQUAL', 'MINUSEQUAL', 'MULTIPLEEQUAL', 'DIVIDEEQUAL'),
        ("nonassoc", '<', '>', 'ISLESSOREQUAL', 'ISMOREOREQUAL', 'ISNOTEQUAL'),
        ("left", '+', '-', 'DOTPLUS', 'DOTMINUS'),
        ("left", '*', '/', 'DOTMULTIPLE', 'DOTDIVIDE'),
    )

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_column(p),
                                                                                      p.type, p.value))
        else:
            print("Unexpected end of input")

    def p_program(self, p):
        """program : instructions"""
        p[0] = p[1]

    def p_instructions(self, p):
        """instructions : instructions instruction
                    | instruction"""
        if len(p) == 3:
            p[0] = AST.InstructionList() if p[1] is None else p[1]
            p[0].addInstruction(p[2])
        else:
            p[0] = AST.InstructionList()
            p[0].addInstruction(p[1])

    def p_instruction(self, p):  # fixme
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
        p[0] = AST.Instruction(p[1])

    def p_assignment(self, p):
        """assignment : ID '=' operation ';'
                    | ID '[' INT ',' INT ']' '=' operation ';'
                    | ID '=' '[' rows ']' ';'
                    | ID '=' zeros ';'
                    | ID '=' ones ';'
                    | ID '=' eye ';' """
        if len(p) == 5:
            p[0] = AST.AssignInstruction(p[1], p[3])
        elif len(p) == 7:
            p[0] = AST.AssignInstruction(p[1], p[4])
        elif len(p) == 10:
            p[0] = AST.ElementAssign(p[1], p[3], p[8])

    def p_zeros(self, p):
        """zeros : ZEROS '(' INT ')' """
        p[0] = AST.Zeros(p[3])

    def p_ones(self, p):
        """ones : ONES '(' INT ')' """
        p[0] = AST.Ones(p[3])

    def p_eye(self, p):
        """eye : EYE '(' INT ')' """
        p[0] = AST.Eye(p[3])

    def p_rows(self, p):
        """rows : nums
                    | rows ';' nums """
        p[0] = AST.Rows()
        if len(p) > 2:
            p[0].cons_row(p[1].row_list, p[3])
        else:
            p[0].append_row(p[1])

    def p_nums(self, p):
        """nums : num
                    | nums ',' num """
        p[0] = AST.Row()
        if len(p) > 2:
            p[0].cons_int(p[1].int_list, p[3])
        else:
            p[0].append_int(p[1])

    def p_for_instruction(self, p):
        """for_instruction : FOR iterator instruction """
        p[0] = AST.ForInstruction(p[2], p[3])

    def p_while_instruction(self, p):
        """while_instruction : WHILE '(' bool_expression ')' instruction """
        p[0] = AST.WhileInstruction(p[3], p[5])

    def p_if_instruction(self, p):
        """if_instruction : IF '(' bool_expression ')' instruction
                    | IF '(' bool_expression ')' instruction ELSE instruction"""
        if len(p) == 6:
            p[0] = AST.IfInstruction(p[3], p[5])
        else:
            p[0] = AST.IfElseInstruction(p[3], p[5], p[7])

    def p_print_instruction(self, p):
        """print_instruction : PRINT operation ';'
                    | PRINT operation ',' operation ';'
                    | PRINT num ';' """
        if len(p) == 4:
            p[0] = AST.PrintInstruction(p[2], None)
        else:
            p[0] = AST.PrintInstruction(p[2], p[4])

    def p_operation(self, p):
        """operation : num
                    | id
                    | unary_minus
                    | matrix_transposition
                    | '(' operation ')'
                    | operation '+' operation
                    | operation '-' operation
                    | operation '*' operation
                    | operation '/' operation
                    | operation DOTMINUS operation
                    | operation DOTPLUS operation
                    | operation DOTMULTIPLE operation
                    | operation DOTDIVIDE operation """
        if len(p) == 2:
            p[0] = p[1]
        elif p[1] == "(":
            p[0] = AST.GroupedExpression(p[2])
        else:
            p[0] = AST.BinExpression(p[2], p[1], p[3])

    def p_unary_minus(self, p):
        """unary_minus : '-' id """
        p[0] = AST.UnaryMinus(p[1])

    def p_matrix_transposition(self, p):
        """matrix_transposition : id "'" """
        # todo
        p[0] = AST.MatrixTransposition(p[1])

    def p_break_instruction(self, p):
        """break_instruction : BREAK ';' """
        p[0] = AST.BreakInstruction()

    def p_continue_instruction(self, p):
        """continue_instruction : CONTINUE ';' """
        p[0] = AST.ContinueInstruction()

    def p_return_instruction(self, p):
        """return_instruction : RETURN operation ';'
                    | RETURN ';' """
        p[0] = AST.ReturnInstruction()

    def p_compound_instruction(self, p):
        """compound_instruction : '{' instructions '}'"""
        p[0] = AST.CompoundInstruction(p[2])

    def p_iterator(self, p):
        """iterator : ID '=' int_or_id ':' int_or_id """
        p[0] = AST.Iterator(p[1], p[3], p[5])

    def p_int_or_id(self, p):
        """int_or_id : id
                    | num_i """
        p[0] = p[1]
        
    def p_id(self, p):
        """id : ID """
        p[0] = AST.Variable(p[1])

    def p_num(self, p):
        """num : num_s
                    | num_f
                    | num_i """
        p[0] = p[1]

    def p_num_s(self, p):
        """num_s : STRING """
        p[0] = AST.String(p[1])

    def p_num_f(self, p):
        """num_f : FLOAT """
        p[0] = AST.Float(p[1])

    def p_num_i(self, p):
        """num_i :  INT """
        p[0] = AST.Integer(p[1])

    def p_bool_expression(self, p):
        """bool_expression : id
                    | operation EQUAL operation
                    | operation '<' operation
                    | operation '>' operation
                    | operation ISLESSOREQUAL operation
                    | operation ISMOREOREQUAL operation
                    | operation ISNOTEQUAL operation"""
        if len(p) == 2:
            p[0] = AST.BoolExpression(p[1], None, None)
        else:
            p[0] = AST.BoolExpression(p[2], p[1], p[3])

    def p_assignment_operation(self, p):
        """assignment_operation : id PLUSEQUAL operation ';'
                    | id MINUSEQUAL operation ';'
                    | id MULTIPLEEQUAL operation ';'
                    | id DIVIDEEQUAL operation ';' """
        p[0] = AST.AssignOperation(p[2], p[1], p[3])

    parser = yacc.yacc()
