import numpy as np
def inputprocess(s:str):
    global t,out
    t =[]
    out = []
    t = s.split()
    for i in range(len(t)):
        out.append(float(t[i]))
    return  
def is_warp():
    global mat_star
    bool = True
    for i in range(info):
        for j in range(info):
            if mat_star[i,j] == 1 and mat_star[j,i] == 1:
                bool = False
                break
            else:
                pass
    return bool

try:
    info = int(input('请输入数据组数：'))
except:
    print('给我一个正常的整数嘛~')
    print('不理你了 哼！')

p = np.zeros((info,2))
c = np.zeros((2,info))
for row in range(info):
    p[row][0]=float(input('输入第'+str(row+1)+'次消费(用空格或逗号隔开)(p1,p2) = '))
    p[row][1]=float(input('输入第'+str(row+1)+'次消费(用空格或逗号隔开)(p1,p2) = '))
    c[0][row]=float(input('输入第'+str(row+1)+'次价格(用空格或逗号隔开)(x1,x2) = '))
    c[1][row]=float(input('输入第'+str(row+1)+'次价格(用空格或逗号隔开)(x1,x2) = '))
mat_m = p.dot(c)
print('数据表如下')
print(mat_m)
mat_star = np.zeros(np.shape(mat_m))
for i in range(info):
    for j in range(info):
        if mat_m[i][j]<mat_m[i][i]:
            mat_star[i][j] = 1
print('---------------------------')
print('是否\'*\'如下(1代表打星号)')

if is_warp():
    print(mat_star)
    print('Yes.')
else:
    print(mat_star)
    print('Hell no!')