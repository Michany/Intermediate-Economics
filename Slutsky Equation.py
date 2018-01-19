from sympy import *
import re

#init_printing(use_latex=True) #用于.ipynb文件中显示Latex

def insert(original, new, pos):
    '''Inserts new inside original at pos.'''
    new = original[:pos] + new + original[pos:]
    return new


def initial(s):
    waiting = []
    count = 0
    for i in range(len(s) - 1):
        if s[i] in '123456789.' and (s[i + 1] == 'x' or s[i + 1] == 'y'):
            waiting.append(i)
    for i in waiting:
        count += 1
        s = insert(s, '*', (i + count))
    return s


x = Symbol('x')
y = Symbol('y')
px = Symbol('px')
#py = Symbol('py')

print('__________________________')
raw_U = 'x**2*y'  # input('输入效用函数 U = ')
U = simplify(initial(raw_U))
income = []
income.append(float(input('|输入收入m = ')))
raw_M = 'px*x+y'  # input('输入约束函数 M = ')
M = simplify(initial(raw_M))
raw_budget = solve(M - m, y)
MRS_U = diff(U, x) / diff(U, y)
MRS_M = diff(M, x) / diff(M, y)
ans = solve(Eq(MRS_U, MRS_M),y)
try:
    ans[0]
    Eq_x = solve(Eq(M.subs(y,ans[0]),m),x)
except: #解只有x没有y
    ans = solve(Eq(MRS_U, MRS_M),x)
    Eq_x = ans
x_star = Eq_x[0]

pxl = []
pxl.append(float(input('|输入初始px = ')))
pxl.append(float(input('|输入变化后px = ')))
x_consume = []
x_consume.append(x_star.subs(m, income[0]).subs(px, pxl[0]))
x_consume.append(0.)
x_consume.append(x_star.subs(m, income[0]).subs(px, pxl[1]))  # 代入变动后价格
dm = x_consume[0] * (pxl[1] - pxl[0])
income.append(income[0] + dm)
x_consume[1] = x_star.subs(m, income[1]).subs(px, pxl[1])
dxs = x_consume[1] - x_consume[0]  # 替代效应
dxn = x_consume[2] - x_consume[1]  # 收入效应
dx = dxs + dxn
#print('|__________________________')
#pprint(x_star)
print('|__________________________')
print('|替代效应△x^s = ' + str(round(dxs, 5)))
print('|替代效应△x^n = ' + str(round(dxn, 5)))
print('|__________________________')
if dxs*dxn>0:
    print('|普通商品 Ordinary Good', end = ';')
    if dxn>0:
        print('正常商品 Normal Good')
    else:
        print('')
elif dxs*dxn<0:
    print('|低档商品 Inferior Good',end = ';')
    if abs(dxs)<abs(dxn):
        print(' 吉芬商品 Giffen Good ')
    else:
        print('')
elif dxs == 0:
    print('|完全互补品 Perfect Complements ;')
print('|__________________________')

p1 = plot_implicit(Eq(M.subs(px,pxl[0])-income[0]),(x,0,income[0]/pxl[0]),(y,0,200),show=False)
p2 = plot_implicit(Eq(M.subs(px,pxl[1])-income[1]),(x,0,income[1]/pxl[1]),(y,0,200),show=False,line_color = 'r')
p1.extend(p2)
p1.extend(plot_implicit(Eq(M.subs(px,pxl[1])-income[0]),(x,0,income[1]/pxl[0]),(y,0,200),show=False,line_color = 'g'))
p1.show()
x_star