from Compiler.parser_make_data import *
from Compiler.scanner import get_next_token, TokenType, scan_errors

with open("../Tests/codegen_test/basic_tests/test14.txt") as f:
    eof = False
    start_char = ''
    # token_string, token_type, start_char, eof = get_next_token(f, start_char)
    line_num = 1
    generator = CodeGenerator()
    this_state = state_1
    past_states = []
    root_node = Node(program, 1, None, program.name)
    this_node = root_node
    isEnded = False
    token_string, token_type_value, start_char, eof = get_next_token(f, start_char)
    while this_state != state_2 or len(past_states) > 0:
        print(this_node)
        print(this_state)
        print(token_string, TokenType(token_type_value))
        this_state, is_token_moved, past_states, this_node = \
            this_state.next_state(past_states, token_string, TokenType(token_type_value), this_node, eof, line_num, generator)
        if this_state is None:
            break
        if is_token_moved and not eof:
            token_string, token_type_value, start_char, eof = get_next_token(f, start_char)
            while (TokenType(token_type_value) == TokenType.COMMENT or
                           TokenType(token_type_value) == TokenType.WHITESPACE or
                   TokenType(token_type_value) == TokenType.NOT_A_TYPE) and not eof:
                if ord(token_string[0]) == 10 and TokenType(token_type_value) == TokenType.WHITESPACE:
                    line_num += 1
                token_string, token_type_value, start_char, eof = get_next_token(f, start_char)
        elif is_token_moved and eof:
            if isEnded:
                printer.print_error("%d: Syntax Error! Unexpected EndOfFile" % line_num)
                break
            isEnded = True
    printer.print_tree(root_node)
    scan_errors()
    jmp_to_main("", None, generator)
    print("semantic_stack:", generator.semantic_stack)
    print("var_scope_stack:", generator.var_scope_stack)
    print("arr_scope_stack:", generator.arr_scope_stack)
    print("func_scope_stack:", generator.func_scope_stack)
    print("scope:", generator.scope)
    print("scope_id:", generator.scope_id)
    print("data_ptr:", generator.data_ptr)
    print("program_ptr:", generator.program_ptr)
    print("program_block", generator.program_block)
    printer.print_code(generator)

