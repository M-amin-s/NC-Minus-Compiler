### INTERMEDIATE CODE GENERATOR FOR NC MINUS COMPILER ###

# current scope is a list of scopes from outer to inner at the time of execution
# scope id's start from 0 and every time we reach a new scope we add 1
# to the top_of_stack and get push it on top of current_scope
# every time we get out of a scope we pop from the current_scope
current_scope = []

# a list of pairs with the scope(list) in which the variables were defined at and the variable name
# e.g. var_scope_stack=[('x', [0,1,2]), ('y', [0,1,3]), (['x', [0,1,2])]
var_scope_stack = []

# a list of 4 pairs with the scope(list) in which the functions were defined at, the function name,
# the number of arguments and return type
# e.g. func_scope_stack=[('add_func', [0,1], 2, 'int'), ('main', [0], 0, 'void')]
# must include ('main', [0], 0, 'void') otherwise print error: "main function not found"
func_scope_stack = []

# the array of 4 element pairs which needs to be filled with instructions
# e.g. program_block=[('ADD', 500, 1000, 508), ('JPF', 512, 6)]
program_block = []

# compilation time stack to be used by compiler
semantic_stack = []

# current address of data memory (increment by 4)
data_ptr = 500

# current address of program memory (increment by 4)
program_ptr = 0

# current address of temporary memory (increment by 4)
tmp_ptr = 1000

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





