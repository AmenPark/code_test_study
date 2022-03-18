# encoding, decoding 함수 필요
# action: status, value -> status, value의 함수들 필요.
# funcs : action의 리스트
# checker : 기존 기록과 새로운 기록을 비교. True일 경우 그대로, False일 경우 덮어쓰기를 하는 용도의 함수.

class dp:
  def __init__(self, funcs, start_status, checker = None):
    self.funcs = funcs
    self.data = {}
    self.done = {}
    self.start = start_status
    if checker == None:
      self.checker = lambda x,y : x>y
    else:
      self.checker = checker
      
  def calcul(self, target_status):
    to_do = list(self.data.items())
    
    while (len(to_do) > 0 and self.data.get(target_status,None)==None):
      next_to_do = []
      for before_status, before_cost in to_do:
        if self.done.get(before_status,None) != None:
          continue
        else:
          self.done[before_status] = True
        for func in funcs:
          next_status, next_cost = func(before_status, before_cost)
          if self.data.get(next_status,None) != None:
            if self.checker(self.data[next_status], next_cost):
              self.data[next_status] = next_cost
              next_to_do.append((next_status,next_cost))
      to_do = next_to_do
    return self.data.get(target_status,None)
  
