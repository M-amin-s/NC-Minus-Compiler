with open("test.txt") as f:
    while True:
        c = f.read(1)
        if not c:
            print("End of file")
            break
        print("Read a character:", c)


def is_keyword(str):
    if (str == 'if' or str == 'else' or str == 'void' or str == 'int' or str == 'while'
            or str == 'break' or str == 'continue' or str == 'switch' or str == 'default'
            or str == 'case' or str == 'return'):
        return True
    else:
        return False


def is_comment(str):
    return True


def is_symbol(str):
    if (str == ';' or str == ':' or str == ',' or str == '[' or str == ']'
            or str == '(' or str == ')' or str == '{' or str == '}'
            or str == '+' or str == '-' or str == '*' or str == '='
            or str == '<' or str == '=='):
        return True
    else:
        return False


def is_num(str):
    ans = False
    for c in str:
        if c.isdigit():
            ans = True
        else:
            ans = False
            break
    return ans


def is_id(str):
    state = 0
    for c in str:
        if state == 0 and c.isalpha():
            state = 1
        if state == 0 and c.isdigit():
            state = 2
            break
        if state == 1 and c.isdigit():
            state = 1
        if state == 1 and c.isalpha():
            state = 2
            break
    if state == 1:
        return True
    if state == 2:
        return False


def is_whitespace(str):
    if (ord(str) == 32 or ord(str) == 10 or ord(str) == 13
            or ord(str) == 9 or ord(str) == 11 or ord(str) == 12):
        return True
    else:
        return False


def check_language(state):
    if is_comment(state):
        return 5
    elif is_keyword(state):
        return 3
    elif is_symbol(state):
        return 4
    elif is_num(state):
        return 1
    elif is_id(state):
        return 2
    elif is_whitespace(state):
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
