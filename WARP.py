# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 19:19:25 2018

@author: Mill
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def data_collect(): #输入数据
    dim = int(input('请输入有几组数据：'))   
    data = np.full([dim*2,3], np.nan) 
    df=pd.DataFrame(data,columns=['price','amount','budget'])

    for i in range(dim):
        df.iloc[i*2]['price'] =float((input('请输入第%d组第一个商品价格：'%(i+1))))
        df.iloc[i*2]['amount']=float((input('请输入第%d组第一个商品数量：'%(i+1))))
        df.iloc[i*2+1]['price'] =float((input('请输入第%d组第二个商品价格：'%(i+1))))
        df.iloc[i*2+1]['amount']=float((input('请输入第%d组第二个商品数量：'%(i+1))))
        df.iloc[i*2+1]['budget']=df.iloc[i*2]['price']*df.iloc[i*2]['amount']+df.iloc[i*2+1]['price']*df.iloc[i*2+1]['amount']
    print(df)
    return df

def warp_plot(df):
    pass
    
def is_warp(df): #判断是否违背warp
    signal = None
    for i in range(int(len(df)/2)):
        for j in range(int(len(df)/2)):
            #budget1_1 第一组商品的预算 budget1_2 用第一组商品价格乘以第二组商品数量 budget2_1 用第二组商品价格乘以第一组商品数量 budget2_2 第二组商品的预算
            budget1_1=df.iloc[i*2]['price']*df.iloc[i*2]['amount']+df.iloc[i*2+1]['price']*df.iloc[i*2+1]['amount']
            budget1_2=df.iloc[i*2]['price']*df.iloc[j*2]['amount']+df.iloc[i*2+1]['price']*df.iloc[j*2+1]['amount']
            budget2_1=df.iloc[j*2]['price']*df.iloc[i*2]['amount']+df.iloc[j*2+1]['price']*df.iloc[i*2+1]['amount']
            budget2_2=df.iloc[j*2]['price']*df.iloc[j*2]['amount']+df.iloc[j*2+1]['price']*df.iloc[j*2+1]['amount']
            #若在购买消费束x的时候，有能力购买消费束y,那么在购买消费束y的时候，x的消费束一定在购买力之外
            if budget1_1>budget1_2: 
                if budget2_2>budget2_1:
                    print('False')
                    signal = False
            elif budget1_1<budget1_2:
                if budget2_2<budget2_1:
                    print('False')
                    signal = False
    print('True')
    signal = True
    
    return signal
    
    
    
if __name__=='__main__':
    df=data_collect()
    is_warp(df)