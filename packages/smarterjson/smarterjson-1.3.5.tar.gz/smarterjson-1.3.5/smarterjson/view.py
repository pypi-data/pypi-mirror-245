def tree(expression, space: str='   '):
    """
    values mode:
        string = 'values  ->  key1  ->  value_data'
        list = ['values','key1','value_data']
        That expression(string or list) can summon tree, like this:

        values
        |- key1
        |  |-> value_data

    keys mode:
        string = 'keys  ->  key1  ->  key2  ->  key3  ->  final_key'
        list = ['keys','key1','key2','key3','final_key']
        That expression(string or list) can summon tree, like this:

        keys
        |- key1
        |  |- key2
        |     |- key3
        |        |--> final_key

    :param expression: type: str or list
    :param space: fill
    :return: tree
    """
    if type(expression) == str:
        expression = expression.replace(" ","").split("->")
    struct_tree = []
    for t in range(len(expression)):
        if expression[0] == "values":
            if t == 0:
                struct_tree.append(f"{expression[t]}")
            elif t == len(expression)-1:
                struct_tree.append(f"|{space*t}|-> ('{expression[t]}')")
            else:
                struct_tree.append(f"|{space*t}|- {expression[t]}")
        elif expression[0] == "keys":
            if t == 0:
                struct_tree.append(f"{expression[t]}")
            elif t == len(expression) - 1:
                struct_tree.append(f"|{space * t}|--> {expression[t]}")
            else:
                struct_tree.append(f"|{space * t}|- {expression[t]}")
        else:
            raise PosError(f"Invalid pos {expression[0]}, should be keys or values")
    return '\n'.join(struct_tree)

class PosError(IndexError):
    pass