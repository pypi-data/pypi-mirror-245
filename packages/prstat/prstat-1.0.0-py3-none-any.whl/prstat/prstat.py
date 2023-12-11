import sympy 
from math import comb
x=sympy.Symbol('x')
y=sympy.Symbol('y')
e=sympy.E
I=sympy.I

def pr_b_a(pr_a_b,pr_a,pr_b):
    return pr_a_b*pr_a/pr_b 

def multiset(n,r):
    """
    구분하는 단위가 n입니다.
    만약 (x+y+z)=6의 자연수 해의 쌍은 3H9이니 mulitiset(3,9)로 나타낼 수 있습니다.
    """
    return comb(n+r-1,r) 

def communication_system(pr_0t, pr_1t, pr_0r_0t, pr_1r_0t, pr_0r_1t, pr_1r_1t):
    """
    입력 : pr_0t, pr_1t, pr_0r_0t, pr_1r_0t, pr_0r_1t, pr_1r_1t 
    """
    pr_0r = (pr_0r_0t * pr_0t) + (pr_0r_1t * pr_1t)
    pr_1r = (pr_1r_0t * pr_0t) + (pr_1r_1t * pr_1t)
    
    pr_1t_0r = pr_b_a(pr_0r_1t,pr_1t,pr_0r)
    pr_0t_1r = pr_b_a(pr_1r_0t,pr_0t,pr_1r)
    
    pr_error= (pr_0r_1t * pr_1t) + (pr_1r_0t * pr_0t)
    
    print(f"pr_0r={pr_0r}")
    print(f"pr_1r={pr_1r}")
    print(f"pr_1t_0r={pr_1t_0r}")
    print(f"pr_0t_1r={pr_0t_1r}")
    print(f"pr_error={pr_error}")
    return(pr_0r,pr_1r,pr_1t_0r,pr_0t_1r,pr_error)