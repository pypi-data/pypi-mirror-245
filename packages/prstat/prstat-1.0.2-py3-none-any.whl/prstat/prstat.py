import sympy 
x=sympy.Symbol('x') #변수 x가 미리 정의되어있습니다.
y=sympy.Symbol('y') #변수 y가 미리 정의되어있습니다.
e=sympy.E #sympy에서 사용할 e가 미리 정의되어있습니다.

"""
import sympy는 미리 되어있습니다.
사용할땐 from prstat.prstat import * 하시면 됩니다.
"""


def fact(n):
    """
    팩토리얼입니다. 내장함수로 제작되었으므로 import 하지마세요
    """
    ret=1
    for i in range(1,n+1):
        ret*=i
    return ret

def comb(n,r):
    """
    조합입니다. 혹시나 컴퓨터에 파이썬 버전이 낮을경우를 대비해 내장함수로 제작하였습니다.
    """
    return fact(n)//(fact(r)*fact(n-r))

def multi_comb(n,r):
    """
    구분하는 단위가 n입니다. 만약 (x+y+z)=6의 자연수 해의 쌍은 3H9이니 multi_comb(3,9)로 나타낼 수 있습니다.
    """
    return comb(n+r-1,r) 

def pr_b_a(pr_a_b,pr_a,pr_b):
    return pr_a_b*pr_a/pr_b 

def communication_system(pr_0t, pr_1t, pr_0r_0t, pr_1r_0t, pr_0r_1t, pr_1r_1t):
    """
    Pr(0received|0transmitted)하는 문제입니다. 입력 : pr_0t, pr_1t, pr_0r_0t, pr_1r_0t, pr_0r_1t, pr_1r_1t 
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

def digital_communication(n,k,t,p):
    """
    디지털통신에서 codeword 수신 실패하는 문제입니다. 입력형식 : n,k,t,p
    """
    pr_ok = 0
    for i in range(t+1) :
        Pr_OK += comb(n,i) * (p**i) * ((1-p)**(n-i))
    print(f"Pr_error : {1-pr_ok}")
    return (1-pr_ok)

if __name__=="__main__":
    digital_communication(15,7,2,0.02)