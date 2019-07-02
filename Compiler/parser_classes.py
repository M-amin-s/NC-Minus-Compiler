from Compiler.scanner import TokenType
from Compiler.intermediate_code_generator import *


class Terminal:
    def __init__(self, token_type, token_string, is_epsilon=False):
        self.token_type = token_type
        self.token_string = token_string
        self.is_epsilon = is_epsilon
        self.first = [self]
        self.name = token_string

    def is_equal(self, token_type, token_string):
        if self.token_type != token_type:
            return False
        if self.token_type == TokenType.SYMBOL or self.token_type == TokenType.KEYWORD:
            return token_string == self.token_string
        return True


class Non_Terminal:
    def __init__(self, name):
        self.transition_diagram = None
        self.name = name
        self.first = []
        self.follow = []

    def set_transition_diagram(self, transition_diagram):
        self.transition_diagram = transition_diagram

    def set_first(self, first):
        self.first = first

    def set_follow(self, follow):
        self.follow = follow

    def is_epsilon_in_follow(self):
        for terminal in self.follow:
            if terminal.is_epsilon:
                return True
        return False

    def is_epsilon_in_first(self):
        for terminal in self.first:
            if terminal.is_epsilon:
                return True
        return False

    def is_in_follow(self, token_type, token_string):
        for terminal in self.follow:
            if terminal.is_equal(token_type, token_string):
                return True
        return False

    def is_in_first(self, token_type, token_string):
        for terminal in self.first:
            if terminal.is_equal(token_type, token_string):
                return True
        return False

    def __str__(self):
        return self.name


class Transition_diagram:
    def __init__(self, states, start_state):
        self.states = states
        self.start_state = start_state


class Edge:
    def __init__(self, start, end, label, codegen_method=None):
        self.start = start
        self.end = end
        self.label = label
        self.codegen_method = codegen_method

    def move(self, past_states, token_string, token_type, this_node, generator):
        if self.codegen_method is not None:
            call_code_gen(token_string, token_type, self.codegen_method, generator)
        if isinstance(self.label, Terminal):
            if self.label.is_epsilon:
                return self.end, False, past_states, this_node
            else:
                parent = this_node
                new_level = this_node.level + 1
                new_node = Node(self.label, new_level, parent, token_string)
                parent.add_child(new_node)
                return self.end, True, past_states, this_node
        else:
            parent = this_node
            new_level = this_node.level + 1
            new_node = Node(self.label, new_level, parent, self.label.name)
            parent.add_child(new_node)
            past_states.append(self.end)
            return self.label.transition_diagram.start_state, False, past_states, new_node


class State:
    def __init__(self, number, non_terminal, is_end=False, is_first=False, codegen_method=None):
        self.number = number
        self.is_end = is_end
        self.is_first = is_first
        self.edges = []
        self.non_terminal = non_terminal
        self.codegen_method = codegen_method

    def add_edge(self, edge):
        self.edges.append(edge)
        epsilon_edge_index = -1
        for i in range(len(self.edges)):
            if isinstance(edge.label, Terminal) and edge.label.is_epsilon:
                epsilon_edge_index = i
        self.edges[epsilon_edge_index], self.edges[-1] = self.edges[-1], self.edges[epsilon_edge_index]

    def next_state(self, past_states, token_string, token_type, this_node, eof, line_num, generator):
        if len(self.edges) == 1 and isinstance(self.edges[0], Terminal) and \
                        self.edges[0].label.token_type == TokenType.EOF and not eof:
            printer.print_error("%d: Syntax Error! Malformed Input" % line_num)
            return None, False, None, None
        if self.is_end:
            if self.codegen_method is not None:
                call_code_gen(token_string, token_type, self.codegen_method, generator)
            return past_states.pop(), False, past_states, this_node.parent
        for i in range(len(self.edges)):
            edge = self.edges[i]
            if isinstance(edge.label, Terminal):
                if edge.label.is_epsilon:
                    if self.non_terminal.is_in_follow(token_type, token_string) or eof:
                        return edge.move(past_states, token_string, token_type, this_node, generator)
                else:
                    if edge.label.is_equal(token_type, token_string):
                        return edge.move(past_states, token_string, token_type, this_node, generator)
                    else:
                        if len(self.edges) == 1:
                            if edge.label.token_type == TokenType.ID or edge.label.token_type == TokenType.NUM:
                                printer.print_error(
                                    "%d: Syntax Error! Missing %s" % (line_num, edge.label.token_type.name))
                            else:
                                printer.print_error(
                                    "%d: Syntax Error! Missing %s" % (line_num, edge.label.token_string))
                            return None, False, None, None
            if isinstance(edge.label, Non_Terminal):
                if (edge.label.is_in_first(token_type, token_string) or
                        edge.label.is_in_follow(token_type, token_string)) or \
                        (eof and edge.label.is_epsilon_in_first()):
                    if ((edge.label.is_in_first(token_type, token_string)) or
                                edge.label.is_epsilon_in_first() and
                                edge.label.is_in_follow(token_type, token_string)) or \
                            (eof and edge.label.is_epsilon_in_first()):
                        return edge.move(past_states, token_string, token_type, this_node, generator)
                    else:
                        if len(self.edges) == 1:
                            printer.print_error("%d: Syntax Error! Missing %s" % (line_num, edge.label))
                            parent = this_node
                            new_level = this_node.level + 1
                            new_node = Node(edge.label, new_level, parent, token_string)
                            parent.add_child(new_node)
                            return edge.end, False, past_states, this_node

                else:
                    if len(self.edges) == 1:
                        printer.print_error("%d: Syntax Error! Unexpected %s" % (line_num, token_string))
                        return self, True, past_states, this_node

    def __str__(self):
        return "state:%d" % self.number


class Node:
    def __init__(self, content, level, parent, name):
        self.content = content
        self.name = name
        self.level = level
        self.childs = []
        self.parent = parent

    def add_child(self, child):
        self.childs.append(child)

    def __str__(self):
        return "name:%s,level:%d" % (self.name, self.level)


class Printer:
    def __init__(self, result_addr, errors_addr):
        self.f_result = open(result_addr, "w+")
        self.f_error = open(errors_addr, "w+")

    def print_error(self, err):
        self.f_error.write(err + "\n")

    def print_tree(self, node):
        str = ""
        for i in range(node.level - 1):
            str += "\t"
        str += node.__str__()
        self.f_result.write(str + "\n")
        for child in node.childs:
            self.print_tree(child)


printer = Printer("../Tests/parser_test/parser_tree.txt", "../Tests/parser_test/errors.txt")
