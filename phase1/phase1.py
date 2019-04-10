with open("test.txt") as f:
    while True:
        c = f.read(1)
        if not c:
            print("End of file")
            break
        print("Read a character:", c)


def check_language(state):
    if (is_comment(state)):
        return 5
    if (is_keyword(state)):
        return 3
    if (is_symbol(state)):
        return 4
    if (is_num(state)):
        return 1
    if (is_id(state)):
        return 2
    if (is_white_space(state)):
        return 6
    return 0

def get_next_token(file, start_char):
    state = "" + start_char
    token_type = 0
    end_char = ""
    while True:
        c = file.read(1)
        token_type_next = check_language(state + c)
        if token_type == 0:
            end_char = c
            break
        token_type = token_type_next
    return state, token_type, end_char

# TODO: RESULT FILE AND ERROR AND CALL GET_NEXT_TOKEN