"""
Standard dynamic code spec:

args passed in kwargs from json

return: (datatype {mime}, data, [code {if not present: 200}])
"""

def solve(**kwargs):
    strequ = kwargs["eq"]
    tgt = kwargs["val"]
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
    transform = standard_transformations+(implicit_multiplication_application,convert_xor,)
    equation = parse_expr(strequ, transformations=transform)
    from sympy import solve, latex
    solution = solve(equation, tgt)
    return dict(datatype="application/x-latex", data=latex(solution))