import sys
sys.setrecursionlimit(100000000)      # 재귀상한증가

class node:
    def __init__(self, name):
        self.name = name            #명칭
        self.anc = None             #부모
        self.conn = []              #연결된 노드들
        self.depth = 0              #루트에서 얼마나 먼가?
        
    def get_anc(self,anc):
        '''
        노드의 부모를 찾아주는 과정. 재귀적이다.
        '''
        self.anc = anc
        for son in self.conn:
            if son != anc:
                son.get_anc(self)
                
    def get_root(self):
        '''
        루트찾기. 가장 긴 사슬의 끝단을 골랐다.
        '''
        connum = len(self.conn)
        if self.anc != None:
            connum -= 1
        if connum == 0:
            return (0,self,0,self,self)  #체인 최대길이, 끝단, 가장 긴 체인, 끝단 둘.
        elif connum == 1:
            for nd in self.conn:
                if nd == self.anc:
                    continue
                a,b,c,d,e = nd.get_root()
                a += 1
                if c <= a:
                    c = a
                    d = b
                    e = self
                return a,b,c,d,e
        else:
            max_length = 0
            second_length = 0
            end_node = None
            send_node = None
            long_chain = 0
            end_chain = None
            end2_chain = None
            for nd in self.conn:
                if nd == self.anc:
                    continue
                a,b,c,d,e = nd.get_root()
                if max_length <= a:
                    second_length = max_length
                    max_length = a
                    send_node = end_node
                    end_node = b
                elif second_length <= a:
                    send_node = b
                    second_length = a
                if long_chain <= c:
                    long_chain = c
                    end_chain = d
                    end2_chain = e
            max_length += 1
            second_length += 1
            if max_length + second_length >= long_chain:
                long_chain = max_length+second_length
                end_chain = end_node
                end2_chain = send_node
            return max_length, end_node, long_chain, end_chain, end2_chain
          
    def to_anc(self, anc):
        if self.anc == None:
            self.anc = anc
        else:
            self.anc.to_anc(self)
            self.anc = anc
            
#     def repr_dict(self):                                    # 노드가 제대로 작동하는지 출력해보기 위해 만들어보았다.
#         rt = {}
#         rt[self.name] = []
#         for son in self.conn:
#             if son != self.anc:
#                 rt[self.name].append(son.repr_dict())
#         return rt
#     def __repr__(self):
#         return str(self.name)

    def get_max_depth(self):                                # 최대깊이 찾기.
        rt = 0
        for nd in self.conn:
            if nd == self.anc:
                continue
            else:
                rt = max(rt,nd.get_max_depth() + 1)
        return rt
    
    def get_chain(self,bann,n,l):                         # 재귀적으로 최대깊이와 동일한 깊이인 노드가 존재하는지 찾는다. 있다면 T, 없다면 F 반환.
        target = min(n,l)
        for nd in self.conn:
            if nd == self.anc or nd == bann:
                continue
            k = nd.get_max_depth()
            if k == target:
                return True
        if self.anc == None:
            return False
        return self.anc.get_chain(self,n+1, l-1)

def solution(n, edges):
    answer = 0
    ndlist = [node(_) for _ in range(n+1)]
    for e1,e2 in edges:
        ndlist[e1].conn.append(ndlist[e2])
        ndlist[e2].conn.append(ndlist[e1])
    ndlist[1].get_anc(None)
    _,_, lc, root1, root2 = ndlist[1].get_root()
    root2.to_anc(None)
    if root1.get_chain(None,-1, lc - 1):          # 가장 긴 체인을 기준으로 해당 체인에서 꼬다리만큼의 길이가 존재한다면 가장 긴 체인길이가 되고 아니라면 -1한값이 된다.
        return lc
    else:
        return lc-1
    return answer
