from sympy import *
import time
import re
import random


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

def concave():
    global raw_U, horizon, vertical, Optimal_x, Optimal_y
    temp = U.subs(x, horizon).subs(y, 0) - U.subs(y, vertical).subs(x, 0)
    if temp > 0:
        Optimal_x = horizon
        Optimal_y = 0
    elif temp == 0:
        Optimal_x = horizon
        Optimal_y = 0
    else:
        Optimal_x = 0
        Optimal_y = vertical
    return


def concave_max():
    global raw_U, horizon, vertical, Optimal_x, Optimal_y
    
    temp = ineq1.subs(x, horizon).subs(y, 0) - ineq2.subs(y, vertical).subs(x, 0) #而顺序不一定,TODO
    if temp > 0:
        Optimal_x = horizon
        Optimal_y = 0
    elif temp == 0:
        Optimal_x = horizon
        Optimal_y = 0
    else:
        Optimal_x = 0
        Optimal_y = vertical
    return

def convex():
    global raw_U, horizon, vertical, Optimal_x, Optimal_y, ans
    try:
        ans[0]
        try:
            Optimal_x = solve(Eq(ans[0][y], budegt_constrain_line))[0]
        except:
            Optimal_x = ans[0][x]  # 拟线性函数
    except:
        print('Oppps！好像无解')

def is_concave():
    global horizon, vertical, U
    random_x1 = random.uniform(0, horizon)
    random_y1 = solve(Eq(U. subs(x, random_x1), 4), y)[0]  # 这个要把x带进去
    random_x2 = random.uniform(0, horizon)
    random_y2 = solve(Eq(U.subs(x, random_x2), 4), y)[0]
    mp_x = (random_x1 + random_x2) / 2
    mp_y = (random_y1 + random_y2) / 2
    temp = U.subs(x, mp_x).subs(y, mp_y) - \
        U.subs(x, random_x1).subs(y, random_y1)
    if temp < 0:
        return True
    else:
        return False

x = Symbol('x')
y = Symbol('y')

raw_U = 'y+46x-2*x**2'  # input('输入效用函数 U = ')
if raw_U.startswith('min') or raw_U.startswith('Min'):
    raw_U = raw_U.replace('min', 'Min')
    U = simplify(initial(raw_U))
    raw_two_eq = re.findall(r'\((.*?),(.*?)\)', raw_U)
    ineq1 = simplify(initial(raw_two_eq[0][0]))
    ineq2 = simplify(initial(raw_two_eq[0][1]))
    boundary = solve(Eq(ineq1, ineq2), y)[0]
elif raw_U.startswith('max') or raw_U.startswith('Max'):
    raw_U = raw_U.replace('max', 'Max')
    U = simplify(initial(raw_U))
    raw_two_eq = re.findall(r'\((.*?),(.*?)\)', raw_U)
    ineq1 = simplify(initial(raw_two_eq[0][0]))
    ineq2 = simplify(initial(raw_two_eq[0][1]))
else:
    U = simplify(initial(raw_U))  # 将字符串输入转化为sympy表达式

raw_M = '18x+y'  # input('输入约束函数 M = ')
M = simplify(initial(raw_M))
m = 135  # float(input('输入收入 m = '))
t0 = time.time()
raw_budget = solve(M - m, y) #当预算线y有多解时，将x=0带入舍去负值，因为当x=0时y必然为正
if len(raw_budget) == 1:
    budegt_constrain_line = solve(M - m, y)[0]
else:
    for i in raw_budget:
        if i.subs(x,0)<=0:
            pass
        else:
            budegt_constrain_line = i
horizon = solve(M - m, x)[0].subs(y, 0)
vertical = budegt_constrain_line.subs(x, 0)


if raw_U.startswith('min') or raw_U.startswith('Min'):
    Optimal_x = solve(Eq(boundary, budegt_constrain_line))[0]
elif raw_U.startswith('max') or raw_U.startswith('Max'):
    concave_max()
else:
    MRS_U = diff(U, x) / diff(U, y)
    MRS_M = diff(M, x) / diff(M, y)
    ans = solve(Eq(MRS_U, MRS_M), (y,x))
    if is_concave():
        concave()
    else:
        convex()

Optimal_y = budegt_constrain_line.subs(x, Optimal_x)
Consumption_bundle = (round(Optimal_x, 5), round(Optimal_y, 5))
print('Consumption_bundle is ' + str(Consumption_bundle))

Utility = U.subs(x, Optimal_x).subs(y, Optimal_y)
p1 = plot_implicit(Eq(U, Utility), (x, 0, 1.2 * horizon),
                   (y, 0, 1.2 * vertical), line_color='#df0070', title='Consumption bundle is ' + str(Consumption_bundle), show=False)
p1.extend(plot_implicit(M < m, (x, 0, 1.2 * horizon),
                        (y, 0, 1.2 * vertical), line_color='#00a8a8', show=False))
tpy = time.time() - t0
p1.show()
print('duration in seconds %7.3f' % tpy)