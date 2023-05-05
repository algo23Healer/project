import numpy as np
import pandas as pd
import os



def read_data():
    pass
    
def get_date(dir_name):
    list_ = dir_name.split('-')
    date = list_[1]+'-'+list_[2]+'-'+list_[3]
    return date, list_[0]
    
def listdir(current_date):
    '''
    paths: 文件夹路径
    current_date:所在时间
    
    return:
        contract_list: 一个存储当天合约的列表
        info_list: 按照合约列表的顺序存储他们当天的数据，每一个元素都是一个DataFrame
    '''
    paths = os.walk(r'./tick_data')
    contract_list = []
    info_list = []
    for path, dir_lst, file_lst in paths:
        for dir_name in dir_lst:
            paths1 = os.walk(path+r'/'+dir_name)
            for path1, dir_lst1, file_lst1 in paths1:
                for file_name in file_lst1:
                    date, contract = get_date(file_name)
                    if date == current_date:
                        contract_list.append(contract)
                        info = pd.read_csv(path1+r'/'+file_name)
                        info = info.drop(labels = ['a1', 'a1_v', 'a2', 'a2_v', 'a3', 'a3_v', 'a4', 'a4_v', 'a5', 'a5_v', 'amount', 'b1', 'b1_v', 'b2', 'b2_v', 'b3', 'b3_v', 'b4', 'b4_v', 'b5', 'b5_v'], axis = 1)
                        info_list.append(info)
    
    return contract_list, info_list
                                     

    
# contract_list, info_list = listdir(paths, '2023-01-10')
# print(info_list)