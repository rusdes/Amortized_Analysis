import ast
import math

exec(open("input.py").read())
dict = locals().copy()

dict.pop('ast')
dict.pop('math')
for i in list(dict.keys()):
    if i[0] == '_':
        dict.pop(i)

data_strutures = ["DynamicArray"]

def get_functions(filename):
    with open(filename) as file:
        node = ast.parse(file.read())

    functions = [n for n in node.body if isinstance(n, ast.FunctionDef)]
    classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
    funcs = []

    for function in functions:
        if function.name[0] != '_':
            funcs.append(function.name)

    for class_ in classes:
        print("Class name:", class_.name, "\n")
        methods = [n for n in class_.body if isinstance(n, ast.FunctionDef)]
        for method in methods:
            if method.name[0] != '_':
                funcs.append(method.name)
    return funcs

def get_funcs_from_input(funcs, dict):
    instance = {}
    for i in dict.keys():
        for j in data_strutures:
            if j in str(dict[i]) and "class" not in str(dict[i]):
                instance[j] = i
    return instance

for i in data_strutures:
    if i not in dict:
        data_strutures.remove(i)

functions = get_functions("data_structures/DynamicArray.py")
funcs_in_input = get_funcs_from_input(functions, dict)

# read input
funcs_present = []
inputfile = open("input.py").read()
for line in inputfile.strip().split('\n'):
    for cl, instance in list(funcs_in_input.items()):
        for func in functions:
            if line.find(instance+'.'+func) > -1:
                funcs_present.append(func)
                # if cl not in funcs_present:
                #     funcs_present[cl] = (func,1)
                # else:
                #     funcs_present[cl] = (func, funcs_present[cl][1]+1)

print("Data Structures available:",data_strutures, "\n")

print("funcs available in current data structure:", functions, "\n")

print("Functions detected in input file:",funcs_present, "\n")

# print(funcs_in_input)
print("Class and object initiaized with its memory address", dict, "\n")

def amortized_aggregate_dynamic(func):
    # count = number of total operations
    # func = list of funcs in order

    cost = 0
    removed = 0
    for i in range(len(func)):
        if i == 0:
            cost += 1
        elif math.log2(i - removed).is_integer() and func[i] == "append":
            cost += i
        elif func[i] == "delete":
            removed += 1
        cost += 1

    amortized_cost = cost/len(func)
    return int(math.ceil(amortized_cost))

def amortized_accounting_dynamic(func):
    #  trial and error
    # func = list of funcs in order
    bank = 0
    try_cost = 1
    removed = 0
    while bank >= 0:
        for i in range(len(func)):
            if func[i] == "append":
                if i - removed > 0 and math.log2(i - removed).is_integer():
                    bank -= i - removed
                bank += try_cost
                bank -= 1
            if func[i] == 'delete':
                removed += 1
                bank -= 1
            if bank < 0:
                try_cost += 1
                break
        if bank >= 0:
            return try_cost
        bank = 0

    #  assume 'd' coins for each insertion. 1 coin for inserting if we dont need to resize.
    #  So, we save d-1 coins at each step to pay for extra cost whike copying array in future.
    # Suppose we resize at size k, k/2 elements haven't been copied before. So we can use the coins saved while inserting them.
    # (d - 1)*k/2 >= k
    # d >= 3
    # So, minimum cost is 3

def amortized_potential_dynamic(func):
    # potential func = 2n - m
    # n = current number of elements
    # m = length of array
    removed = 0
    n = 0
    m = 0

    actual_cost = 0

    for i in range(len(func)):
        if func[i] == "append":
            if n > 0 and m == n and math.log2(n).is_integer():
                m *= 2
                actual_cost += n
            if n == 0:
                actual_cost += 1
                m = 1
            n += 1
            actual_cost += 1
        if func[i] == 'delete':
            removed += 1
            n -= 1
            actual_cost += 1
        
    return int(math.ceil((actual_cost + (2*n - m) - 0) / len(func)))

print("Aggregate:", amortized_aggregate_dynamic(funcs_present))

print("Accounting:", amortized_accounting_dynamic(funcs_present))

print("Potential:", amortized_potential_dynamic(funcs_present))