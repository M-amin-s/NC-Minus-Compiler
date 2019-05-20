from Compiler.parser_make_data import *
from Compiler.scanner import get_next_token, TokenType


def print_tree(node):
    str = ""
    for i in range(node.level - 1):
        str += "\t"
    str += node.__str__()
    print(str)
    for child in node.childs:
        print_tree(child)


with open("../Tests/parser_test/test1.txt") as f:
    eof = False
    start_char = ''
    # token_string, token_type, start_char, eof = get_next_token(f, start_char)
    this_state = state_0
    past_states = []
    root_node = Node(E, 1, None, E.name)
    this_node = root_node
    token_string, token_type_value, start_char, eof = get_next_token(f, start_char)
    while this_state != state_2 or len(past_states) > 0:
        # print(this_node)
        # print(this_state)
        this_state, is_token_moved, past_states, this_node = \
            this_state.next_state(past_states, token_string, TokenType(token_type_value), this_node, eof)
        if is_token_moved and not eof:
            token_string, token_type_value, start_char, eof = get_next_token(f, start_char)
            while (TokenType(token_type_value) == TokenType.COMMENT or
                           TokenType(token_type_value) == TokenType.WHITESPACE) and not eof:
                token_string, token_type_value, start_char, eof = get_next_token(f, start_char)
        elif is_token_moved and eof:
            # TODO
            pass
    print_tree(root_node)
