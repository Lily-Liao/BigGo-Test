from multiprocessing import Pool
import os
 
result=[[1,2,3]]
 
 
def main_map(x):
  for i in x:
    print('子處理程序 ID: {}, 輸出結果: {}'.format(os.getpid(), i))

def shell(processor_num, data):
  pool = Pool(processor_num)
  pool.map_async(main_map, data)
  pool.close()
  pool.join()
 
if __name__=="__main__":
  print('主處理程序 ID:', os.getpid())
  shell(processor_num = 3, data = result*3)