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

        # a list of 5 pairs with the scope(list) in which the functions were defined at, the function name,
        # the argument types & names & address, return type e.g. func_scope_stack=[('add_func', [0,1],
        # [('a', 500','num','void'), ('b',504','array','int')], 508, 5), ('main',[], [], , ?)] must include ('main',
        # [], [], , ?) otherwise print error: "main function not found"
        # TODO: change fss initialization of output
        self.func_scope_stack = [('output', [0], [('a', 1000, 'num', LangFunc.INT.name)], LangFunc.VOID.name, 1)]

        # the array of (at most) 4 element pairs which needs to be filled with instructions
        # e.g. program_block=[('ADD', 500, 1000, 508), ('JPF', 512, 6, )]
        self.program_block = [""]

        # compilation time stack to be used by compiler
        self.semantic_stack = []

        # current address of data memory (increment by 4)
        self.data_ptr = 500

        # current address of program memory (increment by 1)
        self.program_ptr = 0

        # current address of temporary memory (increment by 4)
        self.tmp_ptr = 1004

        # shows if program is inside a while loop
        self.in_while = False

        # shows if program is inside a switch loop
        self.in_switch = False

    def check_scope_definitions(self, scope):
        currnet_scope = self.scope
        index = 0
        correct = True
        if len(currnet_scope) < len(scope):
            correct = False
        else:
            while index < len(scope):
                if len(scope) == index or len(currnet_scope) == index:
                    break
                elif scope[index] == currnet_scope[index]:
                    index += 1
                elif scope[index] != currnet_scope[index]:
                    correct = False
        return correct

    def search_arr_scope_stack(self, name):
        for arr in self.arr_scope_stack:
            if arr[0] == name:
                if self.check_scope_definitions(arr[1]):
                    return arr
                else:
                    print("'%s' is not defined" % arr[0])
        print("'%s' is not defined" % name)
        return None

    def search_var_scope_stack(self, name):
        for var in self.var_scope_stack:
            if var[0] == name:
                if self.check_scope_definitions(var[1]):
                    return var
                else:
                    print("'%s' is not defined" % var[0])
                    return None
        print("'%s' is not defined" % name)
        return None

    def search_func_scope_stack(self, name):
        for func in self.func_scope_stack:
            if func[0] == name:
                if self.check_scope_definitions(func[1]):
                    return func
                else:
                    print("function '%s' is not defined" % func[0])
        print("function '%s' is not defined" % name)
        return None


def call_code_gen(token_string, token_type, methods, generator):
    if type(methods) is list:
        for i in range(len(methods)):
            method = methods[i]
            method(token_string, token_type, generator)
    else:
        try:
            methods(token_string, token_type, generator)
        except:
            print("hello")


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
    if not semantic_stack[-4] == 'void':
        generator.var_scope_stack.append(
            (semantic_stack[-3], semantic_stack[-2], semantic_stack[-4], semantic_stack[-1]))
    else:
        print("Illegal type of void!")
    for i in range(4):
        semantic_stack.pop()
    return


def arr_len_dec(token_string, token_type, generator):
    length = int(token_string)
    generator.semantic_stack.append("#" + str(length))
    generator.data_ptr += (length - 1) * 4


def ptype_int_dec(token_string, token_type, generator):
    generator.semantic_stack.append('int')


def ptype_void_dec(token_string, token_type, generator):
    generator.semantic_stack.append('void')


def arr_dec_finish(token_string, token_type, generator):
    semantic_stack = generator.semantic_stack
    end = semantic_stack[-2] + 4 * semantic_stack[-1]
    if not semantic_stack[-5] == 'void':
        generator.arr_scope_stack.append(
            (semantic_stack[-4], semantic_stack[-3], semantic_stack[-5], semantic_stack[-2], end))
    else:
        print("Illegal type of void!")
    for i in range(5):
        semantic_stack.pop()


def enter_scope(token_string, token_type, generator):
    generator.scope.append(generator.scope_id + 1)
    generator.scope_id = generator.scope_id + 1


def exit_scope(token_string, token_type, generator):
    generator.scope.pop()
    generator.scope_id = generator.scope[-1]


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
        "(%s, %d, %d,)" % (LangFunc.JPF.name, generator.semantic_stack[-3], generator.program_ptr)


def if_label_end(token_string, token_type, generator: CodeGenerator):
    generator.program_block[generator.semantic_stack[-1]] = \
        "(%s, %d,,)" % (LangFunc.JP.name, generator.program_ptr + 1)
    generator.semantic_stack.pop()
    generator.semantic_stack.pop()
    generator.semantic_stack.pop()


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
        "(%s, %d, %d,)" % (LangFunc.JPF.name, generator.semantic_stack[-2], generator.program_ptr + 1)
    generator.semantic_stack.pop()
    generator.semantic_stack.pop()
    generator.semantic_stack.pop()


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
    generator.semantic_stack.pop()
    generator.semantic_stack.pop()


def switch_jmpc_skip(token_string, token_type, generator: CodeGenerator):
    t = generator.tmp_ptr
    generator.tmp_ptr += 4
    generator.program_block[generator.program_ptr] = \
        "(%s, %s, %s, %s)" % (LangFunc.EQ.name, str(generator.semantic_stack[-1]),
                              str(generator.semantic_stack[-2]), str(t))
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
        "(%s, %d, %d,)" % (LangFunc.JPF.name, generator.semantic_stack[-2], generator.program_ptr)
    generator.semantic_stack.pop()
    generator.semantic_stack.pop()


def push_ss(token_string, token_type, generator: CodeGenerator):
    generator.semantic_stack.append("#" + token_string)


def pid_ref(token_string, token_type, generator: CodeGenerator):
    name = token_string
    generator.semantic_stack.append(name)


def arr_ref(token_string, token_type, generator: CodeGenerator):
    name = generator.semantic_stack[-2]
    arr = generator.search_arr_scope_stack(name)
    address = arr[2]
    if isinstance(generator.semantic_stack[-1], str):
        ss_top = int(generator.semantic_stack[-1][1:])
    element_addr = 4 * ss_top + address
    generator.semantic_stack.pop()
    generator.semantic_stack.pop()
    generator.semantic_stack.append(element_addr)


def var_ref(token_string, token_type, generator: CodeGenerator):
    name = generator.semantic_stack[-1]
    var = generator.search_var_scope_stack(name)
    address = var[3]
    generator.semantic_stack.pop()
    generator.semantic_stack.append(address)


def assignment(token_string, token_type, generator: CodeGenerator):
    try:
        generator.program_block[generator.program_ptr] = \
            "(%s, %s, %s,)" % (
                LangFunc.ASSIGN.name, str(generator.semantic_stack[-1]), str(generator.semantic_stack[-2]))
    except Exception as e:
        print(e)
    generator.program_ptr += 1
    generator.program_block.append("")
    generator.semantic_stack.pop()
    generator.semantic_stack.pop()


def multopc(token_string, token_type, generator: CodeGenerator):
    generator.program_block[generator.program_ptr] = \
        "(%s, %s, %s, %s)" % (LangFunc.MULT.name, str(generator.semantic_stack[-1]),
                              str(generator.semantic_stack[-2]), str(generator.tmp_ptr))
    for i in range(2):
        generator.semantic_stack.pop()
    generator.semantic_stack.append(generator.tmp_ptr)
    generator.tmp_ptr += 4
    generator.program_ptr += 1
    generator.program_block.append("")


def addop_p(token_string, token_type, generator: CodeGenerator):
    generator.semantic_stack.append(LangFunc.ADD)


def addop_m(token_string, token_type, generator: CodeGenerator):
    generator.semantic_stack.append(LangFunc.SUB)


def addopc(token_string, token_type, generator: CodeGenerator):
    semantic_stack = generator.semantic_stack
    try:
        generator.program_block[generator.program_ptr] = "(%s, %d, %d, %d)" % (
            semantic_stack[-2].name, semantic_stack[-1], semantic_stack[-3], generator.tmp_ptr)
    except Exception as e:
        print(e)
    for i in range(3):
        semantic_stack.pop()
    semantic_stack.append(generator.tmp_ptr)
    generator.tmp_ptr += 4
    generator.program_ptr += 1
    generator.program_block.append("")


def relop_lt(token_string, token_type, generator: CodeGenerator):
    generator.semantic_stack.append(LangFunc.LT)


def relop_eq(token_string, token_type, generator: CodeGenerator):
    generator.semantic_stack.append(LangFunc.EQ)


def relopc(token_string, token_type, generator: CodeGenerator):
    semantic_stack = generator.semantic_stack
    generator.program_block[generator.program_ptr] = \
        "(%s, %s, %s, %s)" % (semantic_stack[-2].name, str(semantic_stack[-1]),
                              str(semantic_stack[-3]), str(generator.tmp_ptr))
    for i in range(3):
        semantic_stack.pop()
    semantic_stack.append(generator.tmp_ptr)
    generator.tmp_ptr += 4
    generator.program_ptr += 1
    generator.program_block.append("")


def negate_factor(token_string, token_type, generator: CodeGenerator):
    generator.program_block[generator.program_ptr] = \
        "(%s, %d, #0, %d)" % (LangFunc.SUB.name, generator.semantic_stack[-1], generator.tmp_ptr)
    generator.semantic_stack.pop()
    generator.semantic_stack.append(generator.tmp_ptr)
    generator.tmp_ptr += 4
    generator.program_ptr += 1
    generator.program_block.append("")


def push_num_exp(token_string, token_type, generator: CodeGenerator):
    generator.semantic_stack.append("#" + token_string)


def func_def(token_string, token_type, generator: CodeGenerator):
    generator.semantic_stack.pop()
    generator.data_ptr -= 4
    semantic_stack = generator.semantic_stack
    if semantic_stack[-3] == 'int':
        generator.func_scope_stack.append((semantic_stack[-2], semantic_stack[-1], [], generator.data_ptr, None))
        generator.data_ptr += 4
    elif semantic_stack[-3] == 'void':
        generator.func_scope_stack.append((semantic_stack[-2], semantic_stack[-1], [], None, None))
    for i in range(3):
        semantic_stack.pop()


def save_func_begin(token_string, token_type, generator: CodeGenerator):
    generator.semantic_stack.append(generator.program_ptr)
    generator.program_ptr += 1
    generator.program_block.append("")
    mend_func = generator.func_scope_stack[-1]
    generator.func_scope_stack[-1] = (mend_func[0], mend_func[1], mend_func[2], mend_func[3], generator.program_ptr)


def end_func(token_string, token_type, generator: CodeGenerator):
    generator.program_block[generator.semantic_stack[-1]] = \
        "(%s, %d,,)" % (LangFunc.JP.name, generator.program_ptr)
    generator.semantic_stack.pop()


def no_params(token_string, token_type, generator: CodeGenerator):
    generator.semantic_stack.pop()


def pid_param_def(token_string, token_type, generator: CodeGenerator):
    name = token_string
    generator.semantic_stack.append(name)
    func_scope = generator.scope.copy()
    generator.semantic_stack.append(func_scope)
    addr = generator.data_ptr
    generator.semantic_stack.append(addr)
    generator.data_ptr += 4


def array_param_def(token_string, token_type, generator: CodeGenerator):
    ss = generator.semantic_stack
    generator.func_scope_stack[-1][2].append((ss[-3], ss[-1], 'array', ss[-4]))
    generator.arr_scope_stack.append((ss[-3], ss[-2], ss[-1], ss[-4],))
    for i in range(4):
        ss.pop()


def var_param_def(token_string, token_type, generator: CodeGenerator):
    ss = generator.semantic_stack
    generator.func_scope_stack[-1][2].append((ss[-3], ss[-1], 'num', ss[-4]))
    generator.var_scope_stack.append((ss[-3], ss[-2], ss[-4], ss[-1]))
    for i in range(4):
        ss.pop()


def assign_return(token_string, token_type, generator: CodeGenerator):
    out = generator.func_scope_stack[-1][3]
    try:
        generator.program_block[generator.program_ptr] = \
            "(%s, %s, %s,)" % (LangFunc.ASSIGN.name, str(generator.semantic_stack[-1]), str(out))
        generator.program_ptr += 1
        generator.program_block.append("")
    except Exception as e:
        print(e)
    generator.semantic_stack.pop()


def func_call_name(token_string, token_type, generator: CodeGenerator):
    func_name = token_string
    generator.semantic_stack.append(func_name)


def swap_name(token_string, token_type, generator: CodeGenerator):
    name = generator.semantic_stack[-3]
    num_of_args = generator.semantic_stack[-2]
    arg = generator.semantic_stack[-1]
    generator.semantic_stack.pop()
    generator.semantic_stack.pop()
    generator.semantic_stack.pop()
    generator.semantic_stack.append(arg)
    generator.semantic_stack.append(name)
    generator.semantic_stack.append(num_of_args + 1)


def call_function(token_string, token_type, generator: CodeGenerator):
    num_of_args = generator.semantic_stack[-1]
    generator.semantic_stack.pop()
    func_name = generator.semantic_stack[-1]
    func = generator.search_func_scope_stack(func_name)
    generator.semantic_stack.pop()
    if num_of_args == len(func[2]):
        for i in range(len(func[2]) - 1, -1, -1):
            addr = func[2][i][1]
            type = func[2][i][2]
            if type == 'num':
                generator.program_block[generator.program_ptr] = \
                    "(%s, %s, %s,)" % (LangFunc.ASSIGN.name, str(generator.semantic_stack[-1]), str(addr))
            elif type == 'array':
                generator.program_block[generator.program_ptr] = \
                    "(%s, @%s, %s,)" % (LangFunc.ASSIGN.name, str(generator.semantic_stack[-1]), str(addr))
            generator.program_ptr += 1
            generator.program_block.append("")
            generator.semantic_stack.pop()
        func_ptr = func[4]
        generator.program_block[generator.program_ptr] = \
            "(%s, %d,,)" % (LangFunc.JP.name, func_ptr)
        generator.program_ptr += 1
        generator.program_block.append("")
        result = func[3]
        generator.semantic_stack.append(result)
    else:
        print("Mismatch in numbers of arguments of '%s'" % func_name)


def save_main(token_string, token_type, generator: CodeGenerator):
    generator.program_ptr += 1
    generator.program_block.append("")
    generator.program_block[1] = "(%s, %d,,)" % (LangFunc.PRINT.name, 1000)
    generator.program_ptr += 1
    generator.program_block.append("")


def is_main(func):
    correct = True
    if len(func[1]) != 1 or func[1][0] != 0:
        correct = False
    elif len(func[2]) != 0:
        correct = False
    return correct


def jmp_to_main(token_string, token_type, generator: CodeGenerator):
    func = generator.search_func_scope_stack("main")
    if func is not None:
        if is_main(func):
            generator.program_block[0] = "(%s, %d,,)" % (LangFunc.JP.name, func[4])
        else:
            print("main function not found")
    else:
        print("main function not found")


def push_num_of_args(token_string, token_type, generator: CodeGenerator):
    generator.semantic_stack.append(0)


def enter_while(token_string, token_type, generator: CodeGenerator):
    generator.in_while = True


def exit_while(token_string, token_type, generator: CodeGenerator):
    generator.in_while = False


def enter_switch(token_string, token_type, generator: CodeGenerator):
    generator.in_switch = True


def exit_while(token_string, token_type, generator: CodeGenerator):
    generator.in_switch = False


def check_for_while(token_string, token_type, generator: CodeGenerator):
    if not generator.in_while:
        print("continue used outside of while")


def check_for_while_switch(token_string, token_type, generator: CodeGenerator):
    if not generator.in_while and not generator.in_switch:
        print("break used outside of while or switch")
