from enum import Enum


class LangFunc(Enum):
    ADD = 'ADD'
    SUB = 'SUB'
    AND = 'AND'
    ASSIGN = 'ASSIGN'
    EQ = 'EQ'
    JPF = 'JPF'
    JP = 'JP'
    LT = 'LT'
    MULT = 'MULT'
    NOT = 'NOT'
    PRINT = 'PRINT'
    INT = 'int'
    VOID = 'void'


class CodeGenerator:
    def __init__(self):
        # INTERMEDIATE CODE GENERATOR FOR NC MINUS COMPILER
        # current scope is a list of scopes from outer to inner at the time of execution
        # 0 is the program scope in which everything is defined at
        # scope id's start from 0 and every time we reach a new scope we add 1
        # to the top_of_stack and get push it on top of current_scope
        # every time we get out of a scope we pop from the current_scope
        self.scope = [0]

        # the id of current scope
        self.scope_id = 0

        # a list of 4 pairs with the scope(list) in which the variables were defined at, the variable name,
        # the type of variable and the address of variable
        # e.g. var_scope_stack=[('x', [0,1,2], 'int', 540), ('y', [0,1,3], 'void', 544), (['x', [0,1,2], 'int', 548)]
        self.var_scope_stack = []

        # a list of 5 paris with the scope(list) in which the arrays were defined at, the variable name,
        # the type of variable, the address of the start of array and the address of the end of array
        # e.g. arr_scope_stack=[('x_arr', [0,1,2,4], 'int', 540, 564)]
        self.arr_scope_stack = []

        # a list of 4 pairs with the scope(list) in which the functions were defined at, the function name,
        # the argument types & names & address or value and return type
        # e.g. func_scope_stack=[('add_func', [0,1], [('a','int'), ('b','int')], 'int'), ('main', [0], [], 'void')]
        # must include ('main', [0], [], 'void') otherwise print error: "main function not found"
        self.func_scope_stack = [('output', [0], [('a', LangFunc.INT.name)], LangFunc.VOID.name)]

        # the array of (at most) 4 element pairs which needs to be filled with instructions
        # e.g. program_block=[('ADD', 500, 1000, 508), ('JPF', 512, 6, )]
        self.program_block = []

        # compilation time stack to be used by compiler
        self.semantic_stack = []

        # current address of data memory (increment by 4)
        self.data_ptr = 500

        # current address of program memory (increment by 1)
        self.program_ptr = 0

        # current address of temporary memory (increment by 4)
        self.tmp_ptr = 1000


def call_code_gen(token_string, token_type, methods, generator):
    if type(methods) is list:
        for i in range(len(methods)):
            method = methods[i]
            method(token_string, token_type, generator)
    else:
        methods(token_string, token_type, generator)


def pid_dec(token_string, token_type, generator):
    name = token_string
    generator.semantic_stack.append(name)
    scp = generator.scope.copy()
    generator.semantic_stack.append(scp)
    addr = generator.data_ptr
    generator.semantic_stack.append(addr)
    generator.data_ptr += 4


def var_dec_finish(token_string, token_type, generator):
    semantic_stack = generator.semantic_stack
    generator.var_scope_stack.append((semantic_stack[-3], semantic_stack[-2], semantic_stack[-4], semantic_stack[-1]))
    for i in range(4):
        semantic_stack.pop()
    return


def arr_len_dec(token_string, token_type, generator):
    length = int(token_string)
    generator.semantic_stack.append(length)
    generator.data_ptr += (length - 1) * 4


def ptype_int_dec(token_string, token_type, generator):
    generator.semantic_stack.append('int')


def ptype_void_dec(token_string, token_type, generator):
    generator.semantic_stack.append('void')


def arr_dec_finish(token_string, token_type, generator):
    semantic_stack = generator.semantic_stack
    end = semantic_stack[-2] + 4 * semantic_stack[-1]
    generator.arr_scope_stack.append(
        (semantic_stack[-4], semantic_stack[-3], semantic_stack[-5], semantic_stack[-2], end))
    for i in range(5):
        semantic_stack.pop()


def enter_scope(token_string, token_type, generator):
    generator.scope.append(generator.scope_id + 1)
    generator.scope_id = generator.scope_id + 1


def exit_scope(token_string, token_type, generator):
    generator.scope.pop()


def if_jmpc_else(token_string, token_type, generator: CodeGenerator):
    generator.semantic_stack.append(generator.program_ptr)
    generator.program_ptr += 1
    generator.program_block.append("")


def if_jmpu_end(token_string, token_type, generator: CodeGenerator):
    generator.semantic_stack.append(generator.program_ptr)
    generator.program_ptr += 1
    generator.program_block.append("")


def if_label_else(token_string, token_type, generator: CodeGenerator):
    generator.program_block[generator.semantic_stack[-2]] = \
        "(%s, %d, %d,)" % (LangFunc.JPF.name, generator.semantic_stack[-2], generator.program_ptr)


def if_label_end(token_string, token_type, generator: CodeGenerator):
    generator.program_block[generator.semantic_stack[-1]] = \
        "(%s, %d,,)" % (LangFunc.JP.name, generator.program_ptr)


def while_label_start(token_string, token_type, generator: CodeGenerator):
    generator.semantic_stack.append(generator.program_ptr)


def while_jmpc_end(token_string, token_type, generator: CodeGenerator):
    generator.semantic_stack.append(generator.program_ptr)
    generator.program_ptr += 1
    generator.program_block.append("")


def while_jmpu_start(token_string, token_type, generator: CodeGenerator):
    generator.program_block[generator.program_ptr] = \
        "(%s, %d,,)" % (LangFunc.JP.name, generator.semantic_stack[-3])


def while_label_end(token_string, token_type, generator: CodeGenerator):
    generator.program_block[generator.semantic_stack[-1]] = \
        ("%s, %d, %d,)" % (LangFunc.JPF.name, generator.semantic_stack[-2], generator.program_ptr + 1))


def switch_jmpu_ignore(token_string, token_type, generator: CodeGenerator):
    generator.program_ptr += 1
    generator.program_block.append("")


def switch_label_start(token_string, token_type, generator: CodeGenerator):
    pass


def switch_jmpu_end(token_string, token_type, generator: CodeGenerator):
    generator.semantic_stack.append(generator.program_ptr)
    generator.program_ptr += 1
    generator.program_block.append("")


def switch_label_ignore(token_string, token_type, generator: CodeGenerator):
    generator.program_block[generator.program_ptr - 2] = \
        "(%s, %d,,)" % (LangFunc.JP.name, generator.program_ptr)


def switch_label_end(token_string, token_type, generator: CodeGenerator):
    generator.program_block[generator.semantic_stack[-2]] = \
        "(%s, %d,,)" % (LangFunc.JP.name, generator.program_ptr)


def switch_jmpc_skip(token_string, token_type, generator: CodeGenerator):
    t = generator.tmp_ptr
    generator.tmp_ptr += 4
    generator.program_block[generator.program_ptr] = \
        "(%s, %d, %d, %d)" % (LangFunc.EQ.name, generator.semantic_stack[-1],
                              generator.semantic_stack[-2], t)
    generator.semantic_stack.pop()
    generator.semantic_stack.append(t)
    generator.program_ptr += 1
    generator.program_block.append("")
    generator.semantic_stack.append(generator.program_ptr)
    generator.program_ptr += 1
    generator.program_block.append("")


def switch_jmpu_start(token_string, token_type, generator: CodeGenerator):
    generator.program_block[generator.program_ptr] = \
        "(%s, %d,,)" % (LangFunc.JP.name, generator.semantic_stack[-4])
    generator.program_ptr += 1
    generator.program_block.append("")


def switch_label_skip(token_string, token_type, generator: CodeGenerator):
    generator.program_block[generator.semantic_stack[-1]] = \
        "(%s, %d, %d,)"%(LangFunc.JPF.name, generator.semantic_stack[-2], generator.program_ptr)


def push_ss(token_string, token_type, generator: CodeGenerator):
    num = float(token_string)
    generator.semantic_stack.append(num)
