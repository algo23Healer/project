from database import *
import datetime
from chinese_calendar import is_workday, is_holiday
from database import *
from trading_sys import *
from evaluation import *
import time

begin = datetime.date(2023,1,1)
end = datetime.date(2023,1,31)
trading_system = system()

def bolling(data):
    data['MA'] = data['last'].rolling(3600).mean()
    data['std'] = data['last'].rolling(3600).std()
    return data
 
def handle_time(time):
    time = datetime.datetime.strptime(time+' 09:00:00', "%Y-%m-%d %H:%M:%S")
    return time

for i in range((end - begin).days+1):
    day = begin + datetime.timedelta(days=i)
    if is_holiday(day) == False and day != datetime.date(2023,1,28) and day != datetime.date(2023,1,29) and day != datetime.date(2023,1,3):
        day_str = day.strftime('%Y-%m-%d')
        contract_list, info_list = listdir(day_str)
        for info in info_list:
            info = bolling(info)
            # print(datetime.datetime.strptime(handle_time(info.loc[1,'timestamp']), "%Y-%m-%d %H:%M:%S"))
        
        current_time = handle_time(day_str)
        for j in range(36000):
            trading_system.datetime = current_time
            for key, value in trading_system.contract.items():
                index_ = contract_list.index(value)
                if len(info_list[index_]) <= j:
                    continue
                trading_system.price[key] = info_list[index_].loc[j, 'last'] #setting price
            
            for k in range(len(info_list)):
                if len(info_list[k]) <= j:
                    continue
                if np.isnan(info_list[k].loc[j, 'MA']) != True:
                    commodity = None
                    for key, value in trading_system.contract.items():
                        if value == contract_list[k]:
                            commodity = key
                    if info_list[k].loc[j, 'last'] > info_list[k].loc[j, 'MA'] + 2 * info_list[k].loc[j, 'std']:
                        trading_system.signal[commodity] = -1
                        
                    elif info_list[k].loc[j, 'last'] < info_list[k].loc[j, 'MA'] - 10 * info_list[k].loc[j, 'std']:
                        trading_system.signal[commodity] = 1
                        
                    else:
                        trading_system.signal[commodity] = 0
                        
            trading_system.trade()
            current_time = current_time + datetime.timedelta(hours=0, minutes=0, seconds=1)
            # time.sleep(1)
            if j % 60 == 0 and j > 3600:
                trading_system.set_position_list()
                # visualization(trading_system.time_list, trading_system.position_list)
                
        print('当前净值:{}'.format(trading_system.position_value()))    
        trading_system.set_position_list()
        visualization(trading_system.time_list, trading_system.position_list)
        
evaluation_ = evaluation(trading_system.position_list)
print('最大回撤为:{}, 夏普率为:{}'.format(evaluation_.cal_max_drawdown, evaluation_.cal_sharp_ratio()))
        

                    
                    
            
            
        
        