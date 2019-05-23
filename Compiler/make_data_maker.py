type = input()
if type == "t":
    a, b = map(int, input().split())
    nonT = input()
    output = ""
    arr_string = "["
    for i in range(a, b + 1):
        if i == a:
            output += "\nstate_%d = State(%d, %s, is_first=True)" % (i, i, nonT)
        elif i == b:
            output += "\nstate_%d = State(%d, %s, is_end=True)" % (i, i, nonT)
        else:
            output += "\nstate_%d = State(%d, %s)" % (i, i, nonT)
        arr_string += "state_%d, " % i
    t = ""
    while True:
        start, end = map(int, input().split())
        t = input()
        if t == "end":
            break
        output += "\nstate_%d.add_edge(Edge(state_%d, state_%d, %s))" % (start, start, end, t)
    output += "\n%s.set_transition_diagram(Transition_diagram(%s], state_%d))" % (nonT, arr_string, a)
    print(output)
elif type == "f":
    output = ""
    first_follow = input()
    while True:
        line_words = input().split()
        if line_words[0] == "end":
            break
        firsts = ""
        line_words[0] = line_words[0].lower()
        for i in range(1, len(line_words)):
            if line_words[i] == ",," or line_words[i] == ",":
                line_words[i] = "comma"
            line_words[i] = line_words[i].replace(",", "")
            if line_words[i] == "$":
                continue
            if line_words[i] == "*":
                line_words[i] = "star"
            if line_words[i] == "+":
                line_words[i] = "plus"
            if line_words[i] == "-":
                line_words[i] = "minus"
            if line_words[i] == "ε":
                line_words[i] = "epsilon"
            if line_words[i] == "(":
                line_words[i] = "open_parant"
            if line_words[i] == "[":
                line_words[i] = "open_bracket"
            if line_words[i] == ")":
                line_words[i] = "close_parant"
            if line_words[i] == "]":
                line_words[i] = "close_bracket"
            if line_words[i] == "{":
                line_words[i] = "open_crosh"
            if line_words[i] == "}":
                line_words[i] = "close_crosh"
            if line_words[i] == ";":
                line_words[i] = "semicolon"
            if line_words[i] == ":":
                line_words[i] = "double_dot"
            if line_words[i] == "<":
                line_words[i] = "lower"
            if line_words[i] == "=":
                line_words[i] = "equal"
            firsts += "t_" + line_words[i]
            if i != len(line_words) - 1:
                firsts += ", "
        output += "\n%s.set_%s([%s])"%(line_words[0], first_follow, firsts)
    print(output)