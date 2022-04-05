def solution(k, room_number):
    answer = []
    dic = {}        #None -> 빈방, N -> N이 빈방일 것이다.
    for num in room_number:
        if dic.get(num,0) != 0:
            r_num = num
            while dic.get(r_num,0) != 0:
                dic[r_num] = dic.get(dic[r_num],r_num+1)
                r_num = dic[r_num]
            dic[num] = r_num+1
            dic[r_num] = r_num+1
            answer.append(r_num)
        else:
            answer.append(num)
            dic[num] = num+1
    return answer

  
  
class target:
    __slots__ = ['target']
    def __init__(self,var):
        self.target = var
        
    def get_var(self):
        if type(self.target) == type(self):
            return self.target.get_var()
        else:
            return self.target
    
    def inc(self):
        if type(self.target) == type(self):
            self.target = self.target.inc()
            return self.target
        else:
            self.target += 1
            return self
        
        
def solution2(k, room_number):
    answer = []
    dic = {}        #None -> 빈방, N -> N이 빈방일 것이다.
    for num in room_number:
        if dic.get(num,None) == None:
            answer.append(num)
            if dic.get(num-1,None) == None:
                dic[num] = dic.get(num+1,target(num+1))
            else:
                if dic.get(num+1,None) == None:
                    dic[num] = dic[num-1]
                    dic[num].inc()
                else:
                    dic[num] = dic[num+1]
                    dic[num-1].target = dic[num]
        else:
            ans = dic[num].get_var()
            answer.append(ans)
            if dic.get(ans+1,None) == None:
                dic[num].inc()
                dic[ans] = dic[ans-1]
            else:
                dic[ans] = dic[ans+1]
                dic[ans-1].target = dic[ans+1]
    return answer
