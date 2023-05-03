"""
정렬된 리스트를 트리 형태로 저장.
어떤 값에 대해 가장 가까운 값과 가장 멀리있는 값을 찾기.
값을 기반으로 해당 값의 리프를 제거.
의 기능을 갖고있다.
"""

class leaf:
  def __init__(self, var):
    self.var = var
    self.isleft = False
    self.anc = None
    self.small=var
    self.big=var

  def pprint(self,tab=0):
    print("\t"*tab + f"{'／￣' if self.isleft else '＼__' }{self.var}")

  def drop(self,v):
    if self.var == v:
      return True
  def neighbor(self,v):
    return self.var


class node:
  def __init__(self, left, right):
    self.left=left
    self.right=right
    self.isleft=False
    self.var = None
    left.anc=self
    right.anc=self
    left.isleft=True
    self.small=self.left.small
    self.big=self.right.big

  def pprint(self, tab=0):
    self.left.pprint(tab+1)
    print("\t"*tab + f"{'／￣' if self.isleft else '＼__' }({self.small}~{self.big})")
    self.right.pprint(tab+1)

  def drop(self, v):
    if v > self.left.big:
      if self.right.drop(v):
        self.right=None
        if self.isleft:
          self.anc.setLeft(self.left)
        else:
          self.anc.setRight(self.left)
          self.left.isleft=False
        
        self.left.anc=self.anc
    else:
      if self.left.drop(v):
        self.left=None
        if self.isleft:
          self.anc.setLeft(self.right)
          self.right.isleft=True
        else:
          self.anc.setRight(self.right)
        self.right.anc=self.anc
  def setLeft(self, left):
    self.left = left
    self.small=self.left.small
    if self.isleft:
      self.anc.setLeft(self)

  def setRight(self,right):
    self.right = right
    self.big=self.right.big
    if not self.isleft:
      self.anc.setRight(self)

  def neighbor(self,v):
    lb = self.left.big
    if lb>=v:
      return self.left.neighbor(v)
    rs = self.right.small
    if rs<=v:
      return self.right.neighbor(v)
    if abs(lb-v) > abs(rs-v):
      return rs
    else:
      return lb
    


class tree:
  def __init__(self, l):
    nds = [leaf(r) for r in l]
    while len(nds)>1:
      next_nds = [node(nds[i],nds[i+1]) for i in range(0,(len(nds)&(-2)),2)]
      if len(nds)%2==1:
        next_nds.append(nds[-1])
      nds=next_nds
    self.root = nds[0]
    self.root.anc=self

  def drop(self,v):
    if self.root.var == v:
      self.root = None
    else:
      self.root.drop(v)

  def pprint(self):
    self.root.pprint()
  
  def setLeft(self,nd):
    self.root=nd
  def setRight(self,nd):
    self.setLeft(nd)

  def findNear(self, v):
    sval = self.root.small
    mval = self.root.big
    if abs(v-sval) < abs(v-mval):
      return mval
    else:
      return sval

  def findDiff(self,v):
    return self.root.neighbor(v)
