from trading_sys import *
import numpy as np

class evaluation:
    
    def __init__(self, position_list):
        self.position_list = position_list
        
    def cal_max_drawdown(self):
        drawdown = 0
        for i in range(len(self.position_list)):
            for j in range(i+1, len(self.position_list)):
                if self.position_list[j] - self.position_list[i] < drawdown:
                    drawdown = self.position_list[j] - self.position_list[i]
        return drawdown
    
    def cal_sharp_ratio(self):
        return_rate = (self.position_list[-1]-10000000)/10000000*np.sqrt(252)/np.sqrt(15)
        return return_rate/np.std(self.position_list)
    
# list = [1, 1.1, 1.2, 0.7, 0.8, 0.9]
# evaluation1 = evaluation(list)
# print(evaluation1.cal_max_drawdown(), evaluation1.cal_sharp_ratio())
    