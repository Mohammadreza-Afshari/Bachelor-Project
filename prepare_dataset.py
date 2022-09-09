import os 
import shutil
import numpy as np
from upsample import slice_datasets


def shuffle_pick(num,path,dest):
    
    n = 0
    li = os.listdir(path)
    moved = []
    seed = 0
    while(n < num):
        for i in li:
            if 'wav' not in i.split('.') and 'mp3' not in i.split('.'):
                continue
            rand = np.random.randint(0,100)
            if rand > 50 and i not in moved:
                moved.append(i)
                shutil.move(path+'//'+i,dest)
                n += 1
            if n > num:
                break
        seed += 1
        np.random.seed(seed)
    
    
    

    
    
li = os.listdir('E://project//data2//test//augmented')
n = 0
for i in li:
    if 'wav' in i.split('.'):
        n += 1
    
print(n)
    
    
  
    
    
    
#shuffle_pick(20000, 'E://project//data2//validated', 'E://project//data2//test//augmented')

path = 'E://project//data2//test//augmented'
li = os.listdir(path)


for i in li:
    l1 = os.listdir(path+'//11')
    l2 = os.listdir(path+'//22')
    l3 = os.listdir(path+'//33')
    if 'wav' not in i.split('.') and 'mp3' not in i.split('.'):
        continue
    rand = np.random.randint(0,100)
    if rand <= 33 and i not in l1:
        shutil.move(path+'//'+i,path+'//11')    
    elif rand <= 66 and i not in l2:
        shutil.move(path+'//'+i,path+'//22')
    elif i not in l3:
        shutil.move(path+'//'+i,path+'//33')




