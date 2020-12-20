# -*- coding: utf-8 -*-

while True:
  layout=input("請輸入大於兩層的聖誕樹層數:")
  layout=int(layout)
  if layout > 2 :
    break
  else:
    print("層數大於2層才會好看~請重新輸入吧!!")
 
leaf="*"
a=[]
#根據規律寫出其演算法
for i in range(1,2*layout,2):
  for j in range(i,i+2*(layout-1)+1,2):
    a.append(j)

#將葉子從中間對齊列印出來
for k in a:
  print((leaf*k).center(max(a)," "))

#印出樹幹的部分 
for p in range(1,layout):
  print("***".center(max(a)," "))



