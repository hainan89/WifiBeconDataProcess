'''
Created on 2016年7月7日

@author: Casey-NS
'''

import os
import time

def getAllFiles(rootDir): 
    list_dirs = os.walk(rootDir)
    files_list = [] 
    for root, dirs, files in list_dirs: 
        for d in dirs:
            files_list.append(os.path.join(root, d))
#             print(os.path.join(root, d))      
        for f in files: 
            files_list.append(os.path.join(root, f))
#             print(os.path.join(root, f)) 
    return(files_list)

def fileProcessStr(fileDir):
   
    file = open(fileDir)
    line_init_f = 0
    line = ""
    while 1:
        temp_line = file.readline()
        if (temp_line.find('cbid') >= 0) and (line_init_f == 0):
            line = temp_line
            line_init_f = 1
        elif (temp_line.find('cbid') >= 0) and (line_init_f == 1):
            strProcess(line)
            line = temp_line
            line_init_f = 0
        else:
            line = line + temp_line
            
            
        if not temp_line:
            break
    file.close()
    

    return
    
def strProcess(strVal):
    
    bsid_index = ['1a:16:b3:61:4d:ef:00:00:10:10:01:7C', 
                  '6f:64:a1:99:56:dc:00:00:10:10:0B:C0', 
                  'a7:f0:d7:c0:57:f1:00:00:10:10:02:B0']
    file_bsid_index = ['7C', 'C0', 'B0']
    
    data = eval(strVal.replace("\n", ""))
    
    for one_mac in data["mac_info"]:
        one_record = []
        one_record.append(one_mac["MacAddr"])
        one_record.append(one_mac["TimeInterval"])
        
        timeArray = time.localtime(one_mac["TimeInterval"])
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        one_record.append(otherStyleTime)
        
        one_record.append(data["cbid"])
        
        f_index = bsid_index.index(data["cbid"])
        f_index_str = file_bsid_index[f_index]
        file_name = time.strftime("%Y-%m-%d", timeArray) + "-" + f_index_str + ".txt"
        
#         print(one_record)
        record_str = one_record[0] + "\t" + str(one_record[1]) + "\t" + one_record[2] + "\t" + one_record[3]
        storeOneRecord(record_str, file_name)
        
#         print(one_record)
#         print(file_name)
    return

def storeOneRecord(oneRecordStr, fileName):
    file_str = "../output/"+fileName   
    with open(file_str, "a+") as f:
        f.write(oneRecordStr)
        f.write("\n")
    pass
    
if __name__ == '__main__':
    
    files_list = getAllFiles("../Raw Data/")
    process_file_index = 0
    for one_file_dir in files_list:
        
        process_file_index = process_file_index + 1
        
        print("Processing [{0}]: {1}".format(process_file_index, one_file_dir))
        fileProcessStr(one_file_dir)
        print("Processing End. [{0}]: {1}".format(process_file_index, one_file_dir))
    print("Done!")
    
    
    
    