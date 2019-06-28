### INTERMEDIATE CODE GENERATOR FOR NC MINUS COMPILER ###


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


# current scope is a list of scopes from outer to inner at the time of execution
# 0 is the program scope in which everything is defined at
# scope id's start from 0 and every time we reach a new scope we add 1
# to the top_of_stack and get push it on top of current_scope
# every time we get out of a scope we pop from the current_scope
scope = [0]

# the id of current scope
scope_id = 0

# a list of 4 pairs with the scope(list) in which the variables were defined at, the variable name,
# the type of variable and the address of variable
# e.g. var_scope_stack=[('x', [0,1,2], 'int', 540), ('y', [0,1,3], 'void', 544), (['x', [0,1,2], 'int', 548)]
var_scope_stack = []

# a list of 5 paris with the scope(list) in which the arrays were defined at, the variable name,
# the type of variable, the address of the start of array and the address of the end of array
# e.g. arr_scope_stack=[('x_arr', [0,1,2,4], 'int', 540, 564)]
arr_scope_stack = []

# a list of 4 pairs with the scope(list) in which the functions were defined at, the function name,
# the argument types & names & address or value and return type
# e.g. func_scope_stack=[('add_func', [0,1], [('a','int'), ('b','int')], 'int'), ('main', [0], [], 'void')]
# must include ('main', [0], [], 'void') otherwise print error: "main function not found"
func_scope_stack = [('output', [0], [('a', INT)], VOID)]

# the array of (at most) 4 element pairs which needs to be filled with instructions
# e.g. program_block=[('ADD', 500, 1000, 508), ('JPF', 512, 6, )]
program_block = []

# compilation time stack to be used by compiler
semantic_stack = []

# current address of data memory (increment by 4)
data_ptr = 500

# current address of program memory (increment by 1)
program_ptr = 0

# current address of temporary memory (increment by 4)
tmp_ptr = 1000






