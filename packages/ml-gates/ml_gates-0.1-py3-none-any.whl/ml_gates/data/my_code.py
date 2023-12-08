import numpy as np

"""# And function"""

def step(yin):
  if(yin>=0):
    return 1
  else:
    return 0
def and_func(x):
  w=np.array([1,1])
  b=-2
  yin=np.dot(x,w)+b
  ynet=step(yin)
  return ynet

test1=np.array([0,0])
and_func(test1)

test2=np.array([0,1])
and_func(test2)

test3=np.array([1,0])
and_func(test3)

test4=np.array([1,1])
and_func(test4)

"""# NOT function"""

def step(yin):
  if(yin>=0):
    return 1
  else:
    return 0
def not_func(x):
  w=-1
  b=0.5
  yin=np.dot(x,w)+b
  ynet=step(yin)
  return ynet

test1=np.array(0)
not_func(test1)

test2=np.array(1)
not_func(test2)

"""#OR Function"""

def step(yin):
  if(yin>=0):
    return 1
  else:
    return 0
def or_func(x):
  w=np.array([1,1])
  b=-0.5
  yin=np.dot(x,w)+b
  ynet=step(yin)
  return ynet

test1=np.array([0,0])
or_func(test1)

test2=np.array([0,1])
or_func(test2)

test3=np.array([1,0])
or_func(test3)

test4=np.array([1,1])
or_func(test4)

"""#NOR Function"""

def step(yin):
  if(yin>=0):
    return 1
  else:
    return 0
def nor_func(x):
  w=np.array([1,1])
  b=-0.5
  yin=np.dot(x,w)+b
  ynet=step(yin)
  if(ynet==0):
    ynet=1
  else:
    ynet=0
  return ynet

test1=np.array([0,0])
nor_func(test1)

test2=np.array([0,1])
nor_func(test2)

test3=np.array([1,0])
nor_func(test3)

test4=np.array([1,1])
nor_func(test4)

"""#NAND Function"""

def step(yin):
  if(yin>=0):
    return 1
  else:
    return 0
def nand_func(x):
  w=np.array([1,1])
  b=-2
  yin=np.dot(x,w)+b
  ynet=step(yin)
  if(ynet==0):
    ynet=1
  else:
    ynet=0
  return ynet

test1=np.array([0,0])
nand_func(test1)

test2=np.array([0,1])
nand_func(test2)

test3=np.array([1,0])
nand_func(test3)

test4=np.array([1,1])
nand_func(test4)

"""#XOR Function"""

def step(yin):
  if(yin>=0):
    return 1
  else:
    return 0
def not_func(a):
  if(a==1):
    return 0
  else:
    return 1
def xor_func(x):
  y1=and_func(x)
  y2=or_func(x)
  y3=not_func(y1)
  finx=np.array([y2,y3])
  ynet=and_func(finx)
  return ynet

test1=np.array([0,0])
xor_func(test1)

test2=np.array([0,1])
xor_func(test2)

test3=np.array([1,0])
xor_func(test3)

test4=np.array([1,1])
xor_func(test4)