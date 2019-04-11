def is_keyword(str):
    if (str == 'if' or str == 'else' or str == 'void' or str == 'int' or str == 'while'
        or str == 'break' or str == 'continue' or str == 'switch' or str == 'default'
        or str == 'case' or str == 'return'):
        return True
    else:
        return False


def is_comment(str):
    if str.find('\n') == -1 and len(str) >= 2:
        if str[0] == '/' and str[1] == '/':
            return True
    state = 0
    for c in str:
        if state == 0:
            if c == '/':
                state = 1
            else:
                state = -1
        elif state == 1:
            if c == '*':
                state = 2
            else:
                state = -1
        elif state == 2:
            if c == '*':
                state = 3
        elif state == 3:
            if c == '/':
                state = 4
            else:
                state = 2
        elif state == 4:
            state = -1
    if state == 4 or state == 2 or state == 3:
        return True
    else:
        return False


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
        if state == 0 and not c.isalpha():
            state = 1
            break
        if state == 2 and c.isdigit():
            state = 3
        if state == 2 and not c.isalpha() and not c.isdigit():
            state = 1
        if state == 3 and c.isalpha():
            state = 1
    if state == 2 or state == 3:
        return True
    else:
        return False


def is_char_whitespace(char):
    if (ord(char) == 32 or ord(char) == 10 or ord(char) == 13
        or ord(char) == 9 or ord(char) == 11 or ord(char) == 12):
        return True
    else:
        return False


def is_whitespace(str):
    state = 0
    for c in str:
        if state == 0 and is_char_whitespace(c):
            state = 1
        if state == 1 and not is_char_whitespace(c):
            state = 0
    if state == 1:
        return True
    else:
        return False


def check_language(str):
    if len(str) == 0:
        return 0
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


def get_next_token(file, start_char):
    string = '' + start_char
    next_string = string
    is_accepted = False
    m_token_type = 0
    end_char = ""
    while True:
        string = next_string
        c = file.read(1)
        next_string = string + c
        m_token_type = check_language(string)
        if m_token_type != 0 and not is_accepted:
            is_accepted = True
        if not c:
            token_type_next = 7
        else:
            token_type_next = check_language(next_string)
            if primaries[m_token_type] < primaries[token_type_next]:
                token_type_next = 0
        if token_type_next == 0 or token_type_next == 7 and is_accepted:
            end_char = c
            break
    eof = token_type_next == 7
    return string, m_token_type, end_char, eof


types = ["NOT A TYPE", "NUM", "ID", "KEYWORD", "SYMBOL", "COMMENT", "WHITESPACE"]
primaries = [7, 4, 5, 2, 3, 1, 6]
f_out_results = open("scanner.txt", "w+")
f_out_errors = open("lexical_errors.txt", "w+")
# print(is_comment("/* comment */"))
with open("test.txt") as f:
    start_char = ''
    token_type = 0
    line_num = 1
    f_out_results.write("1. ")
    f_out_errors.write("1. ")
    eof = False
    while not eof:
        string, token_type, start_char, eof = get_next_token(f, start_char)
        if token_type != 0 and token_type != 6 and token_type != 5:
            f_out_results.write("(%s, %s) " % (types[token_type], string))
        elif token_type == 6 and ord(string[0]) == 10:
            line_num += 1
            f_out_results.write("\n%d. " % line_num)
            f_out_errors.write("\n%d. " % line_num)
        elif token_type == 0:
            f_out_errors.write("(%s, invalid input) " % string)
f.close()
f_out_errors.close()
f_out_results.close()
# TODO: not write line number if there is nothing in a line
# TODO: handle errors better
