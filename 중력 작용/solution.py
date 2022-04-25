import random
import sys
sys.setrecursionlimit(1000000)

def FW_append(arr, var):
    '''
    0번은 버림. 1번부터 따짐.
    '''
    N = len(arr)
    w = (N & (-N)) - 1
    k = 1
    while w > 0:
        var += arr[N - k]
        k <<= 1
        w >>= 1
    arr.append(var)
def FW_add(arr, index, delta):
    '''
    FW로 만든 arr에 index의 값에 delta 더해서 보정.
    '''
    N = len(arr)
    while N > index:
        arr[index] += delta
        w = index & (-index)
        index += w
def FW_get(arr, index):
    '''
    FW로 만든 arr에 인덱스 1~index 구간의 합.
    '''
    rt = 0
    while index:
        w = index & (-index)
        rt += arr[index]
        index -= w
    return rt

class nd:
    def __init__(self, var, num):
        self.conn = []
        self.num = num
        self.var = var

    def get_chain(self, num2chain, anc=None):
        max_chain = None
        max_L = 0
        sumforFW = 0
        max_fw = 0

        for nd in self.conn:
            if nd == anc:
                continue
            else:
                fwsum, chain = nd.get_chain(num2chain, self)
                sumforFW += fwsum
                chain.anc = self.num
                if max_L < chain.w:
                    max_L = chain.w
                    max_chain = chain
                    max_fw = fwsum

        if max_chain == None:
            new_nd = treap_nd(self.num,self.var)
            chain = treap(new_nd)
            num2chain[self.num] = chain
            return self.var, chain
        else:
            sumforFW -= max_fw
            max_chain.anc = None
            FW_append(max_chain.FW, sumforFW)
            sumforFW += max_fw
            sumforFW += self.var
            num2chain[self.num] = max_chain
            new_nd = treap_nd(self.num,self.var)
            max_chain.push_new(new_nd)
            return sumforFW, max_chain
class empty_nd:
    def __init__(self):
        self.w = 0
        self.sum = 0
class treap_nd:
    def __init__(self, num, var):
        self.w = 1
        self.num = num
        self.var = var
        self.sum = var
        self.left = None
        self.right = None
        self.ran = random.random()

    def compran(self, nd):
        '''
        동일 노드를 입력으로 받는다.
        ran 값 비교하여 크면 True, 작으면 False.
        상대가 노드가 아니라면 True. 내가 노드가 아니면 애초에 에러다.
        두 번째 bool은 이번까지만 하자/계속하자를 의미한다.
        '''
        try:
            if self.ran > nd.ran:
                return True, True
            else:
                return False, True
        except:
            return True, False
class treap:
    def __init__(self, nd):
        self.root = nd
        self.num2pos = {nd.num: 0}
        self.FW = [0]
        self.anc = None
        self.w = 1


    def push_new(self, nd):
        self.num2pos[nd.num] = self.w
        self.w += 1
        self.push(nd)

    def find_var(self, pos):
        now_nd = self.root
        while True:
            left_var = 0
            if now_nd.left:
                left_var = now_nd.left.w
            if pos < left_var:
                now_nd = now_nd.left
            elif pos == left_var:
                return now_nd.var
            else:
                pos -= left_var+1
                now_nd = now_nd.right
                
    def push(self, nd):
        if nd.ran > self.root.ran:
            nd.left = self.root
            nd.sum += self.root.sum
            nd.w += self.root.w
            self.root = nd
        else:
            now_nd = self.root
            while True:
                now_nd.w += 1
                now_nd.sum += nd.sum
                if now_nd.right:
                    if now_nd.right.ran > nd.ran:
                        now_nd = now_nd.right
                    else:
                        nd.left = now_nd.right
                        nd.sum += nd.left.sum
                        nd.w += nd.left.w
                        now_nd.right = nd
                        break
                else:
                    now_nd.right = nd
                    break

    def delete_nd(self, pos):
        '''
        0-> 가장 왼쪽노드.
        타겟 노드를 찾아서 제거.
        상위 노드는 w와 sum이 감소.
        하위 노드는 당겨진다. 작은값과 큰 값 후보 존재. 후보가 하나면 그냥 이어주고 끝.
        작은거의 큰 값, 큰거의 작은값으로 계속 이어지면서 ran값을 비교한다.
        '''
        anc_nds = []
        isleft = True
        now_nd = self.root
        while True:
            left_var = 0
            if now_nd.left:
                left_var = now_nd.left.w
            if pos < left_var:
                anc_nds.append(now_nd)
                now_nd = now_nd.left
                isleft = True
            elif pos == left_var:
                break
            else:
                pos -= left_var + 1
                anc_nds.append(now_nd)
                now_nd = now_nd.right
                isleft = False
        del_var = now_nd.var
        anc = None
        for anc in anc_nds:
            anc.sum -= del_var
            anc.w -= 1
        compS = now_nd.left
        compL = now_nd.right
        bp = True
        if anc == None:
            try:
                left_up, bp = compS.compran(compL)
                if not bp:
                    compL = empty_nd()
            except:
                left_up, bp = False, False
                compS = empty_nd()
            if left_up:
                self.root = compS
                compS.sum += compL.sum
                compS.w += compL.w
                anc = compS
                isleft = False
                compS = compS.right
            else:
                self.root = compL
                compL.sum += compS.sum
                compL.w += compS.w
                anc = compL
                isleft = True
                compL = compL.left

        while bp:
            try:
                left_up, bp = compS.compran(compL)
                if not bp:
                    compL = empty_nd()
            except:
                left_up = False
                bp = False
                compS = empty_nd()
                if compL == None:
                    if isleft:
                        anc.left = None
                    else:
                        anc.right = None
                    break

            if left_up:
                compS.sum += compL.sum
                compS.w += compL.w
                if isleft:
                    anc.left = compS
                else:
                    anc.right = compS
                anc = compS
                isleft = False
                compS = compS.right
            else:
                compL.sum += compS.sum
                compL.w += compS.w
                if isleft:
                    anc.left = compL
                else:
                    anc.right = compL
                anc = compL
                isleft = True
                compL = compL.left
        return now_nd.var

    def get_sum(self, pos):
        fw_var = FW_get(self.FW, pos)
        now_nd = self.root
        now_sum = now_nd.sum
        while True:
            left_w = 0
            if now_nd.left:
                left_w = now_nd.left.w
            if left_w > pos:
                now_sum -= now_nd.sum
                now_nd = now_nd.left
                now_sum += now_nd.sum
            elif left_w == pos:
                if now_nd.right:
                    now_sum -= now_nd.right.sum
                return fw_var + now_sum
            else:
                pos -= left_w + 1
                now_nd = now_nd.right


def subcalcul(u,w,dic,var):
    now_chain = dic[u]
    anc_u = now_chain.anc
    pos = now_chain.num2pos[u]
    if anc_u == None:
        new_node = treap_nd(0, w)
        now_chain.push(new_node)
        del_var = now_chain.delete_nd(pos)
        return del_var
    new_var = subcalcul(anc_u, w, dic, var)
    new_node = treap_nd(0,new_var)
    now_chain.push(new_node)
    del_var = now_chain.delete_nd(pos)
    anc_chain = dic[anc_u]
    anc_pos = anc_chain.num2pos[anc_u]
    FW_add(anc_chain.FW, anc_pos, new_var - var)
    return del_var

def query2(u,w,dic):
    now_chain = dic[u]
    anc_u = now_chain.anc
    pos = now_chain.num2pos[u]
    if anc_u == None:
        new_node = treap_nd(0, w)
        now_chain.push(new_node)
        del_var = now_chain.delete_nd(pos)
        return del_var
    var = now_chain.find_var(pos)
    new_var = subcalcul(anc_u, w, dic, var)
    new_node = treap_nd(0,new_var)
    now_chain.push(new_node)
    del_var = now_chain.delete_nd(pos)
    anc_chain = dic[anc_u]
    anc_pos = anc_chain.num2pos[anc_u]
    FW_add(anc_chain.FW, anc_pos, new_var - del_var)  
    return del_var


def solution(values, edges, queries):
    answer = []
    N = len(values)
    nodedic = {i : nd(values[i-1],i) for i in range(1,N+1)}
    for a, b in edges:
        nodedic[b].conn.append(nodedic[a])
        nodedic[a].conn.append(nodedic[b])

    nd2chain = {}
    nodedic[1].get_chain(nd2chain)
    max_w = nd2chain[1].w
    assert max_w<81000
    for u,w in queries:
        chain = nd2chain[u]
        p = chain.num2pos[u]
        if w == -1:
            qn = chain.get_sum(p)
            answer.append(qn)
        else:
            query2(u,w,nd2chain)

    return answer
