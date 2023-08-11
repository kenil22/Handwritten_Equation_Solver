import sympy as sym
from sympy import *
def solve_equation(equation):
    try:

        if 'x' in equation or 'X' in equation and '=' in equation:

            if 'X' in equation: 
                x = sym.symbols('X')
            else:
                x = sym.symbols('x')
            left, right = equation.split("=")

            eq = left+'-'+right

            result = sym.solve(eq, (x))

            return result
        elif 'x' in equation or 'X' in equation and '=' not in equation:
            if 'X' in equation: 
                x = sym.symbols('X')
            else:
                x = sym.symbols('x')
            result = sym.solveset(equation, x)
            return result

        elif 'z' in equation or 'Z' in equation and '=' in equation:

            if 'Z' in equation: 
                z = sym.symbols('Z')
            else:
                z = sym.symbols('z')

            left, right = equation.split("=")
    
            # print("6")
            eq = left+'-'+right
    
            result = sym.solve(eq, (z))
           
            return result
        elif 'z' in equation or 'Z' in equation and '=' not in equation:

            if 'Z' in equation: 
                z = sym.symbols('Z')
            else:
                z = sym.symbols('z')

            z = sym.symbols('z')
            result = sym.solveset(equation, z)
            return result
        
        elif 'y' in equation and '=' in equation:
            # y = sym.symbols('y')
            if 'Y' in equation:
                y = sym.symbols('Y')
            else:
                y = sym.symbols('y')
            left, right = equation.split("=")
            # print("6")
            eq = left+'-'+right
            # print('---------------')
            result = sym.solve(eq, (y))

            return result
        elif 'y' in equation and '=' not in equation:
            y=sym.symbols('y')
            result = sym.solveset(equation,y)
            return result
        
        elif 'x' in equation and 'y' in equation and '=' in equation :
            x,y = sym.symbols('x,y')

            left, right = equation.split("=")
            # print("6")
            eq = left+'-'+right
            # print('---------------')
            result = sym.solve(eq, (x,y))

            return result
        elif    equation == 'tan30' or equation == 'cos30' or equation == 'sin30' or \
                equation == 'tan60' or equation == 'cos60' or equation == 'sin60' or \
                equation == 'tan90' or equation == 'cos90' or equation == 'sin90':
            #   equation == 'tan0' or equation == 'cos0' or equation == 'sin0':
            theta = sym.symbols('theta')

            trigo_val = equation[0:3]
            if trigo_val == 'tan':
                tan_theta = sym.tan(theta)
            elif trigo_val == 'sin':
                tan_theta == sym.sin(theta)
            elif trigo_val == 'cos':
                tan_theta = sym.cos(theta)
            degree_equ = equation[-2:]

            trigo_equ = tan_theta.subs(theta, sym.deg(int(degree_equ)))

            result = trigo_equ.evalf()
            return result
        elif equation == 'tan0' or equation == 'sin0' or equation == 'cos0':
            theta = sym.symbols('theta')

            tan_theta = sym.tan(theta)

            degreeequ = equation[-1:]

            trigo_equ = tan_theta.subs(theta, sym.deg(int(degreeequ)))
    
            result = trigo_equ.evalf()
        
        elif '=' in equation and 'sin' in equation or 'tan' in equation or 'cos' in equation:
            if 'x' in equation and 'y' in equation:
                x,y = symbols('x,y')
                eq_sympy = sympify(equation)
                result = solve((eq_sympy), (x,y))
                return result
            elif 'x' in equation:
                x = symbols('x')
                eq_sympy = sympify(equation)
                result = solve((eq_sympy), x)
                return result
            elif 'y' in equation:
                y = symbols('y')
                eq_sympy = sympify(equation)
                result = solve((eq_sympy), y)
                return result
            else:
                pass
        else:
            pass
        # print("2")

        if "=" not in equation:

            if 'sin' in equation or 'tan' in equation:
                eq = sympify(equation)
                result = eq.evalf()
                return result
            
            # print("3")
            result = sym.simplify(equation)
            # print("4")
            return result
        
        else:
            left, right = equation.split("=")
            # print("6")
            result = sym.solve(left,right)


            if len(result) == 0:
                return "No solution found." 
            else:
                return result

    except (ValueError, TypeError, AttributeError, RuntimeError, SyntaxError) as e:
        # print(f"Error: {e}")
        return str(e)