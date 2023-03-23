import matplotlib_inline
import matplotlib.pyplot as plt 
import numpy as np
import xrayutilities as xu
import glob
import os,re

# read files and sorted with time.
file_list = sorted(glob.glob("*.xrdml"),key=os.path.getmtime)

read_file = xu.io.XRDMLFile

"""Class method!"""

class make_read_list_class(object):
    def __init__(self,file_list):
        name = self.__dict__
        for i in range(len(file_list)):
            file = read_file(file_list[i])
            name['data_' + str(i)] = file
            
 
 
 All_data = make_read_list_class(file_list)
 data_dict = All_data.__dict__
 
 
 def find_times(data):
    line_tmp = re.search(r'countTime with \D\d+',str(data_dict[data]))
    times_tmp = re.findall(r'\d+',line_tmp[0])
    num = int(times_tmp[0])
    return num
    
 
 class make_line_list_class(object):
    def __init__(self,data_dict):
        lines = self.__dict__
        for d in data_dict:
            line_name = f"line_{d}"
            lines[line_name] =  find_times(d)
            
            
num_dict = make_line_list_class(data_dict).__dict__


class make_count_dict():
    def __init__(self,data_dict):
        counts = self.__dict__
        for d in data_dict:
            count = data_dict[d].scan.ddict['counts']
            if count.ndim > 1:
                counts['count_' + str(d)] = np.sum(count,axis=0)/find_times(d)
            else:
                counts['count_' + str(d)] = count
                

count_averaged = make_count_dict(data_dict).__dict__

list_count = [value for value in count_averaged.values()]

all_count = np.concatenate(list_count)

class make_theta_dict():
    def __init__(self,data_dict):
        thetas = self.__dict__
        for t in data_dict:
            theta = data_dict[t].scan.ddict['2Theta']
            if theta.ndim > 1:
                thetas['2theta_' + str(t)] = theta[0]
            else:
                thetas['2theta_' + str(t)] = theta
 

theta_dict = make_theta_dict(data_dict).__dict__

list_theta = [value for value in theta_dict.values()]
all_theta = np.concatenate(list_theta)

plt.plot(all_theta,all_count)
plt.show()

final_data = np.array((all_theta,all_count))

np.savetxt("final_data.xy",final_data,delimiter=' ')
