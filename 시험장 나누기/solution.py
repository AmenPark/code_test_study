import sys
sys.setrecursionlimit(1000000)
class node:
    '''
    문제에서 주어진 트리의 노드구현.
    해당 노드를 뿌리로 하는 서브트리의 값 합을 subsum으로 표현.
    '''
    def __init__(self,var):
        self.anc = None
        self.left = None
        self.right = None
        self.var = var
        self.subsum = 0
        
    def get_subsum(self):
        '''
        노드가 트리로 연결될 경우 하위 항목에 대해 subsum값을 구하기 위한 연산.
        '''
        var = self.var
        if self.left != None:
            var += self.left.get_subsum()
        if self.right != None:
            var += self.right.get_subsum()
        self.subsum = var
        return self.subsum
    
    def get_cut(self,x, k):
        '''
        노드 연결을 자르는 기준을 k번, x값 이상로 잡음.
        subsum값을 기반으로 x보다 커질 때에 맞춰서 자른다. 잘라진 subtree의 subsum을 누적으로 기억해서 이후 다른 조각에서의 subsum을 정확하게 구하도록 한다.
        subsum 중 가장 큰 값이 maximum으로 반환된다.
        '''
        devider = 0
        maximum = 0
        nowvar = 0
        now_varl = 0
        now_varr = 0
        if self.left != None:
            dvd,max_var, now_varl, tfl = self.left.get_cut(x,k)
            devider = dvd
            maximum = max_var
            nowvar += now_varl
            if tfl == False:
                return 0,0,0,False
        if self.right != None:
            dvd, max_var, now_varr, tfr = self.right.get_cut(x,k)
            if tfr == False:
                return 0,0,0,False
            devider += dvd
            maximum = max(maximum,max_var)
            nowvar += now_varr
        nowvar += self.var
        if nowvar > x:
            devider += 1
            nowvar -= max(now_varl, now_varr)
            maximum = max(maximum, now_varl,now_varr)
        if nowvar > x:
            devider += 1
            nowvar -= min(now_varl,now_varr)
        if devider > k-1:
            return 0,0,0,False
        if maximum > x:
            return 0,0,0,False
        return devider, maximum, nowvar, True
        
    def get_cut_tree(self,x,k):
        '''
        트리 자르기. 노드를 기준으로 부모와의 연결을 자른다.
        tf는 해당 자르기가 마지막일 경우 두 조각이 남는 경우, 두 조각을 모두 비교해야 하기 때문이다.
        '''
        dev, max_var, nowvar, tf = self.get_cut(x,k)
        if tf == False:
            return max_var, False
        else:
            max_var = max(max_var,nowvar)
            return max_var,True
            
        
def solution(k, num, links):
    N = len(num) + 1
    ndlist = [node(s) for s in num]
    answer = 0
    
    # 생성한 ndlist의 노드들을 주어진 트리정보에 맞춰서 생성.
    for n, (l, r )in enumerate(links):
        if l != -1:
            ndlist[n].left = ndlist[l]
            ndlist[l].anc = ndlist[n]
        if r != -1:
            ndlist[n].right = ndlist[r]
            ndlist[r].anc = ndlist[n]
    root = ndlist[0]
    while root.anc != None:
        root = root.anc
    
    #답은 0 이상, 트리 전체의 노드 값의 합 이하에 있음은 확실하다.
    maxvar = root.get_subsum()
    minvar = 0
    
    #이진탐색 기법을 통해서 찾는다.
    while maxvar > minvar + 1:
        temp = (maxvar + minvar) // 2
        max_var, tf = root.get_cut_tree(temp,k)
        if tf == True:
            maxvar = temp
        else:
            minvar = temp
    
    answer, tf = root.get_cut_tree(maxvar,k)
    return answer
