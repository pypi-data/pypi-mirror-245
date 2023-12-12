"""
import sympy as sp는 미리 선언 되어있습니다.
사용할땐 from prstat.prstat import * 하시면 됩니다.
"""

import sympy as sp
from fractions import Fraction as frac
x=sp.Symbol('x')
y=sp.Symbol('y')
e=sp.E
pi=sp.pi
inf=sp.oo

symbol=sp.Symbol
exp=sp.exp 
lim=sp.limit
log=sp.log
diff=sp.diff
integral=sp.integrate
solve=sp.solve


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
    """
    활용예시 : pr_s_k=pr_b_a(pr_k_s,pr_s,pr_k) 즉 인자는 뒤집은것, 원래함수의 | 앞에있는것, 원래함수의 | 뒤에있는것 순서로 씁니다.
    """
    return pr_a_b*pr_a/pr_b 

bayes=pr_b_a

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
        pr_ok += comb(n,i) * (p**i) * ((1-p)**(n-i))
    print(f"Pr_error : {1-pr_ok}")
    return (1-pr_ok)

def light_bulb_manufacturer(La,Sa,pr_l,pr_s,k,equ=None):
    """
    전구수명찾는 문제입니다. 입력형식 : L타입a, S타입a, L타입확률, S타입확률, k시간, 방정식(디폴트는(1-a)*(a**k))을 받습니다.
    """
    a=sp.Symbol('a')
    if not equ:
        equ=(1-a)*(a**k)
    try:
        pr_k_s=equ.subs(a,Sa)
        pr_k_l=equ.subs(a,La)
    except:
        print("""방정식 형식이 올바르지 않습니다. 방정식 생성 예시
a=sp.Symbol('a')
equ=(1-a)*(a**k)
              """)
        return
    pr_k= (pr_k_s*pr_s)+(pr_k_l*pr_l)
    
    pr_s_k=pr_b_a(pr_k_s,pr_s,pr_k)
    pr_l_k=pr_b_a(pr_k_l,pr_l,pr_k)
    
    pr_error=pr_l_k

    print(f"pr_k_s : {pr_k_s}")
    print(f"pr_k_l : {pr_k_l}")
    print(f"pr_s_k : {pr_s_k}")
    print(f"1-pr_l_k : {1-pr_l_k}")
    if pr_s_k>pr_l_k:
        print("S type일것이라고 추측가능")
    else:
        print("L type일것이라고 추측가능")    
    print(pr_error)
    return

def what_is_pmf():
    print("PMF stands for Probability Mass Function and usually notated as PX(k). It is used to describe probabilisitc characteristics of a discrete random variable.")
def what_is_CDF():
    print("CDF stands for Cumulative Distribution Function and usually notated as FX(x). It is used to describe probabilisitc characteristics of a both discrete and continuous random variable.")
def what_is_PDF():
    print("PDF stands for Probability Density Function and usually notaed as fx(x). It is used to describe probability characteristics of a continuous random variable.")

def auditorium_row_seat(row,seat,max_row,zero_row_seat=10):
    """
    Row1=11seats와 같이 강당그림이 그려진 문제입니다.
    """
    row_seat=row+zero_row_seat #해당 row의 자리 개수
    if seat>row_seat:
        pr_s_r=0
    else:
        pr_s_r=1/row_seat
    
    pr_s=0
    for r in range(1,max_row+1):
        row_seat=r+zero_row_seat
        pr_s+=frac((seat<=row_seat),row_seat)/max_row
    
    pr_r=1/max_row
    pr_r_s=pr_b_a(pr_s_r,pr_r,pr_s)
    
    print(pr_s_r)
    print(pr_r_s)
    return

def is_CDF(function):
    """
    CDF인지 판단해주는 함수. 음의무한대극한이 0이고, 무한대극한이 1이고, 감소하지않으며, 연속이여야합니다.
    """
    if lim(function,x,-inf)!=0:
        return 0
    if lim(function,x,inf)!=1:
        return 0
    tmp=sp.Symbol('tmp')
    if sp.simplify(lim(function,x,tmp,'+')-lim(function,x,tmp,'-'))!=0:
        return 0
    diff_x=diff(function,x)
    if sp.solveset(diff_x<0, domain=sp.S.Reals).is_empty!=1:
        return 0
    return 1
    
    
    
    
    

if __name__=="__main__":
    pass
    