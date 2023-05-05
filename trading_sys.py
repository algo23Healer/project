import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

class system:
    
    def __init__(self):
        self.commodity = {'A':0, 'AG':0, 'AL':0, 'AP':0, 'AU':0, 'B':0, 'BB':0, 'BC':0, 'BU':0, 'C':0, \
                          'CF':0, 'CJ':0, 'CS':0, 'CU':0, 'CY':0, 'EB':0, 'EG':0, 'FB':0, 'FG':0, 'FU':0, \
                            'HC':0, 'I':0, 'IC':0, 'IF':0, 'IH':0, 'J':0, 'JD':0, 'L':0, 'M':0, 'MA':0, \
                            'NI':0, 'OI':0, 'PP':0, 'RB':0, 'RM':0, 'SC':0, 'SM':0, 'SN':0, 'SR':0, 'T':0, 'TA':0, 'Y':0}
        self.datetime = None
        
        self.signal = {'A':0, 'AG':0, 'AL':0, 'AP':0, 'AU':0, 'B':0, 'BB':0, 'BC':0, 'BU':0, 'C':0, \
                          'CF':0, 'CJ':0, 'CS':0, 'CU':0, 'CY':0, 'EB':0, 'EG':0, 'FB':0, 'FG':0, 'FU':0, \
                            'HC':0, 'I':0, 'IC':0, 'IF':0, 'IH':0, 'J':0, 'JD':0, 'L':0, 'M':0, 'MA':0, \
                            'NI':0, 'OI':0, 'PP':0, 'RB':0, 'RM':0, 'SC':0, 'SM':0, 'SN':0, 'SR':0, 'T':0, 'TA':0, 'Y':0}
        
        self.price = {'A':0, 'AG':0, 'AL':0, 'AP':0, 'AU':0, 'B':0, 'BB':0, 'BC':0, 'BU':0, 'C':0, \
                          'CF':0, 'CJ':0, 'CS':0, 'CU':0, 'CY':0, 'EB':0, 'EG':0, 'FB':0, 'FG':0, 'FU':0, \
                            'HC':0, 'I':0, 'IC':0, 'IF':0, 'IH':0, 'J':0, 'JD':0, 'L':0, 'M':0, 'MA':0, \
                            'NI':0, 'OI':0, 'PP':0, 'RB':0, 'RM':0, 'SC':0, 'SM':0, 'SN':0, 'SR':0, 'T':0, 'TA':0, 'Y':0}
        
        self.contract = {'A':'a2305', 'AG':'ag2302', 'AL':'al2302', 'AP':'ap2305', 'AU':'au2304', 'B':'b2302', 'BC':'bc2303', 'BU':'bu2302', 'C':'c2305', \
                          'CF':'cf2305', 'CJ':'cj2305', 'CS':'cs2305', 'CU':'cu2303', 'CY':'cy2305', 'EB':'eb2305', 'EG':'eg2305', 'FB':'fb2303', 'FG':'fg2305', 'FU':'fu2305', \
                            'HC':'hc2305', 'I':'i2305', 'IC':'ic2303', 'IF':'if2303', 'IH':'ih2303', 'J':'j2305', 'JD':'jd2305', 'L':'l2305', 'M':'m2305', 'MA':'ma2305', \
                            'NI':'ni2304', 'OI':'oi2305', 'PP':'pp2305', 'RB':'rb2305', 'RM':'rm2305', 'SC':'sc2305', 'SM':'sm2305', 'SN':'sn2305', 'SR':'sr2305', 'T':'t2303', 'TA':'ta2305', 'Y':'y2305'}
        
        self.rules ={'IF':300, 'IC':200, 'IH':300, 'T':1000000, 'AG':15, 'AL':5, 'AU':1000, 'BU':10, 'CU':5,'FU':50,'HC':10,'NI':1, 'RB':10,'SC':1000,'SN':1,'AP':10,'CF':5,'CJ':5, 'CY':5,'FG':20,'MA':10,
            'OI':10,'RM':10,'SR':10,'TA':5, 'A':10,'B':10,'BB':500,'C':10, 'CS':10,'EG':10,'FB':10,'I':100,'J':100, 'JD':5,'L':5,'M':10, 'PP':5,'Y':10,'EB':5}#各品种交易1手单位数
        
        self.balance = 10000000
        self.cost = 0.00013 #冲击成本+手续费
        self.position_list = []
        self.time_list = []
        

    def trade(self):
        for key, value in self.signal.items():
            if value == 0:
                continue
                # print('当前净值:{}'.format(self.position_value()))
            elif value == 1:
                volumn = 100000//(self.price[key]*(1+self.cost))
                if volumn != 0 and self.balance >= 100000:
                    self.balance = self.balance - 100000
                    self.commodity[key] += volumn
                    print('{}买入品种{},合约为:{},买入价为:{},买入{}手,剩余现金:{},当前净值:{}'.format(self.datetime, key, self.contract[key], self.price[key], volumn, self.balance, self.position_value()))
            else:
                if self.commodity[key] != 0:
                    self.balance = self.balance + self.commodity[key]*self.price[key]*(1-self.cost)
                    # print(self.commodity[key]*self.price[key]*(1-self.cost))
                    # if self.commodity[key]*self.price[key]*(1-self.cost) == 0:
                    #     print(self.commodity[key])
                    #     break
                    self.commodity[key] = 0
                    print('{}品种{}平仓,合约为:{},卖出价为:{},剩余现金:{},当前净值:{}'.format(self.datetime, key, self.contract[key], self.price[key], self.balance, self.position_value()))
                
    def position_value(self):
        position_value = self.balance
        for key, value in self.commodity.items():    
            if value != 0:
                position_value += value * self.price[key]
        return position_value
    
    def set_position_list(self):
        self.position_list.append(self.position_value())
        self.time_list.append(self.datetime)

def visualization(timelist,position_value_list):
    # plt.figure(dpi = 300,figsize=(24,8))
    plt.axis([datetime.datetime(2023,1,1,9,0,0), datetime.datetime(2023,1,31,19,0,0), 9500000, 10500000])
    plt.ion()
    
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    # plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.xlabel('Time')
    plt.ylabel('Portfolio Value')
    plt.plot(timelist,position_value_list)
    plt.pause(0.01)
    plt.clf()

# system1 = system()
# system1.datetime = '2023-03-01'
# system1.signal['A'] = 1
# system1.price['A'] = 100
# system1.trade()
# system1.signal['A'] = -1
# system1.price['A'] = 200
# system1.trade()
# system1.signal['AL'] = 2
# system1.signal['AP'] = 3
# system1.price['AL'] = 1000
# system1.price['AP'] = 1000
# print(system1.position_value())