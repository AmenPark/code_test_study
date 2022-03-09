import sys
sys.setrecursionlimit(10**6)

class Node:
    def __init__(self,x,y,i):
        self.var = i
        self.y = y
        self.x = x
        self.anc = None
        self.left = None
        self.right = None
        self.chk = 0

    def get_front(self,a):        #전위
        a.append(self.var)
        if self.left!=None:
            self.left.get_front(a)
        if self.right!=None:
            self.right.get_front(a)
            
    def get_back(self,a):         #후위
        if self.left!=None:
            self.left.get_back(a)
        if self.right!=None:
            self.right.get_back(a)
        a.append(self.var)
    
class Tree :
    def __init__(self):
        self.root = None
            
    def get_node(self,nd):
        if self.root == None:
            self.root = nd
        else:
            anc_nd = self.root
            while True:
                if nd.x > anc_nd.x:
                    if anc_nd.right == None:
                        break
                    anc_nd = anc_nd.right
                else:
                    if anc_nd.left == None:
                        break
                    anc_nd = anc_nd.left
            if nd.x > anc_nd.x:
                anc_nd.right=nd
                nd.anc = anc_nd
            else:
                anc_nd.left = nd
                nd.anc = anc_nd
    def get_front(self,a):
        return self.root.get_front(a)
    def get_back(self,a):
        return self.root.get_back(a)
                
def solution(nodeinfo):
    answer = [[],[]]
    infos = [[nodeinfo[i][0],nodeinfo[i][1],i+1]for i in range(len(nodeinfo))]
    infos.sort(key = lambda x:[x[1],-x[0]],reverse = True)
    tree = Tree()
    for e,info in enumerate(infos):  #x,y,i
        tree.get_node(Node(info[0],info[1],info[2]))
    tree.get_front(answer[0])
    tree.get_back(answer[1])
    return answer
