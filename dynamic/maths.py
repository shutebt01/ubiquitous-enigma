"""
Standard dynamic code spec:

args passed in kwargs from json

return: (datatype {mime}, data, [code {if not present: 200}])
"""

def solve(**kwargs):
    strequ = kwargs["eq"]
    tgt = kwargs["val"]
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
    transform = standard_transformations+(convert_xor,implicit_multiplication_application,)
    equation = parse_expr(strequ, transformations=transform)
    from sympy import solve
    solution = solve(equation, tgt)
    #TODO: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition
    return dict(datatype="text/plain", data=str(solution))

def toLatex(**kwargs):
    strequ = kwargs["eq"]
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
    transform = standard_transformations+(convert_xor,implicit_multiplication_application,)
    equation = parse_expr(strequ, transformations=transform)
    from sympy import latex
    return dict(datatype="text/x-latex", data=latex(equation))
