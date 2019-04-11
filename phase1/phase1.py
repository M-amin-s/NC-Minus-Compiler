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
            state = 2
        if state == 0 and c.isdigit():
            state = 1
            break
        if state == 2 and c.isdigit():
            state = 3
        if state == 3 and c.isalpha():
            state = 1
    if state == 2 or state == 3:
        return True
    else:
        return False


def is_whitespace(str):
    if (ord(str) == 32 or ord(str) == 10 or ord(str) == 13
            or ord(str) == 9 or ord(str) == 11 or ord(str) == 12):
        return True
    else:
        return False


def check_language(str):
    if is_comment(str):
        return 5
    elif is_keyword(str):
        return 3
    elif is_symbol(str):
        return 4
    elif is_num(str):
        return 1
    elif is_id(str):
        return 2
    elif is_whitespace(str):
        return 6
    return 0


def get_next_token(file, start_char, string):
    string = string + start_char
    token_type = 0
    end_char = ""
    while True:
        c = file.read(1)
        if not c:
            token_type = 7
        else:
            token_type_next = check_language(string + c)
            token_type = check_language(string)
            if token_type_next == 0:
                end_char = c
                break
    return string, token_type, end_char


# with open("test1.txt") as f:
#     start_char = ''
#     string = ""
#     while True:
#         string, token_type, start_char = get_next_token(f, start_char, string)
#         print(string)
#         print(token_type)


# TODO: RESULT FILE AND ERROR AND CALL GET_NEXT_TOKEN
