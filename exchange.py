'''
# 交换 

example:
>>> import exchange 
>>> p1=exchange.Person(13,5,'Min(x,y)')
>>> p2=exchange.Person(8,6,'2*x+y')
>>> exchange.change(p1,p2)
>>> print(p1.status())

'''
from sympy import *
import re




class Person():
    '''
    # Person

    Class Person takes 2 parameters while initializing:

    >>> Person(endowment_1,endowment_2)

    Meanings for each attributes:

        good_1, good_2: the good that THE PERSON has in hand now;

        endowment_1, endowment_2: the endowment the THE PERSON has before the exchange;
    '''
    xa = Symbol('xa')
    ya = Symbol('ya')
    xb = Symbol('xb')
    yb = Symbol('yb')
    #px = symbol('px')
    py = Symbol('py')
    good_1 = Symbol('x')
    good_2 = Symbol('y')
    endowment_1 = 0
    endowment_2 = 0
    utility_function = xa - xa
    equation = xa-xa
    relative_price_2 = dict()


    def __init__(self, endowment_1, endowment_2, *utility_function):
        '''读入初始禀赋，可包含效用函数，若效用函数是Min则另作处理'''
        self.endowment_1 = endowment_1
        self.endowment_2 = endowment_2
        self.utility_function = simplify(utility_function) 
        if ('Min' in utility_function[0]) or ('min' in utility_function[0]):
            raw_two_eq = re.findall(r'\((.*?),(.*?)\)', utility_function[0])
            ineq1 = simplify(raw_two_eq[0][0])
            ineq2 = simplify(raw_two_eq[0][1])
            self.equation = Eq(ineq1, ineq2)
            
        else:# 不知为何要加一个[0]才行，本来simplify以后只有一个式子的，这边怎么变成tuple了
            self.equation = Eq(diff(self.utility_function[0],Symbol('x'))/diff(self.utility_function[0],self.good_2), 1/self.py)

    def status(self):
        return (self.endowment_1,self.endowment_2)
def _change(person_1, person_2):

    Eq1 = Eq(person_1.endowment_1 + person_1.endowment_2 * person_1.py, person_1.good_1 + person_1.good_2 * person_1.py)
    Eq1 = Eq1.subs(person_1.good_1, person_1.xa).subs(person_1.good_2, person_1.ya)
    Eq2 = Eq(person_2.endowment_1 + person_2.endowment_2 * person_2.py, person_2.good_1 + person_2.good_2 * person_1.py)
    Eq2 = Eq2.subs(person_2.good_1, person_2.xb).subs(person_2.good_2, person_2.yb)
    Eq3 = Eq(person_1.good_1 + person_2.good_1, person_1.endowment_1 + person_2.endowment_1)
    Eq3 = Eq3.subs(person_1.good_1,person_1.xa).subs(person_2.good_1,person_2.xb)
    Eq4 = Eq(person_1.good_2 + person_2.good_2, person_1.endowment_2 + person_2.endowment_2)
    Eq4 = Eq4.subs(person_1.good_2,person_1.ya).subs(person_2.good_2,person_2.yb)
    Eq5 = person_1.equation.subs(person_1.good_1,person_1.xa).subs(person_1.good_2,person_1.ya)
    Eq6 = person_2.equation.subs(person_2.good_1,person_1.xb).subs(person_2.good_2,person_1.yb)
    print(Eq1,Eq2,Eq3,Eq4,Eq5,Eq6,sep='\n')
    s = solve([Eq1,Eq2,Eq3,Eq4,Eq5,Eq6])

    
    # 筛选一下
    #person_1.relative_price_2[(person_1, person_2)] = py
    print(s)


def change(person_1, person_2): 
    '''
    # 交换 过程

    Stimulate the exchanging process between two Person object. Can re-exchange again anytime.

    Keep the record of exchange in the form of relative price for good_2.
    '''
    try:
        s = solve([Eq(person_1.endowment_1 + person_1.endowment_2 * person_1.py, person_1.xa + person_1.ya * person_2.py),
                Eq(person_2.endowment_1 + person_2.endowment_2 * person_1.py, person_2.xb + person_2.yb * person_1.py),
                Eq(person_1.xa + person_2.xb, person_1.endowment_1 + person_2.endowment_1),
                Eq(person_1.ya + person_2.yb, person_1.endowment_2 + person_2.endowment_2),
                person_1.equation.subs(person_1.good_1,person_1.xa).subs(person_1.good_2,person_1.ya),
                person_2.equation.subs(person_2.good_1,person_2.xb).subs(person_2.good_2,person_2.yb)])
    except:
        print('>>> Solving failed somehow.')
    try:
        ans = s[0]

        #更新物品禀赋
        #取两位小数方便运算；也可以增加随机性
        person_1.endowment_1 = round(ans[person_1.xa],2) 
        person_1.endowment_2 = round(ans[person_1.ya],2) 
        person_2.endowment_1 = round(ans[person_2.xb],2)
        person_2.endowment_2 = round(ans[person_2.yb],2)

        #记录某两人间交易的相对价格
        person_1.relative_price_2[person_2] = ans[person_1.py]
        person_2.relative_price_2[person_1] = ans[person_1.py]    
        print(s)
    except:
        print('>>> No exchange happened!')
    
