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
for i in range(1,2*layout,2):
  for j in range(i,i+2*(layout-1)+1,2):
    a.append(j)
for k in a:
  print((leaf*k).center(max(a)," "))
 
for p in range(1,layout):
  print("***".center(max(a)," "))



