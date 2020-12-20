from multiprocessing import Pool
import os
 
result=[[1,2,3]]
 
 
def main_map(x):
  for i in x:
    print('子處理程序 ID: {}, 輸出結果: {}'.format(os.getpid(), i))

def shell(processor_num, data):
  #設定處理程序的數量
  pool = Pool(processor_num)
  #不會阻塞且能併行觸發
  pool.map_async(main_map, data)
  # close 和 join 是確保主程序結束後，子程序仍然繼續進行
  pool.close()
  pool.join()
 
if __name__=="__main__":
  print('主處理程序 ID:', os.getpid())
  shell(processor_num = 3, data = result*3)