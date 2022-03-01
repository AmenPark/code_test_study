class Node:
    '''
    각 방을 노드로 표현
    anc - 부모노드
    name - 번호
    conn - 연결된 노드의 리스트
    condition - True면 바로 방문 가능, False면 선행 조건 존재
    condition_of - 현 노드를 방문해서 선행조건 만족으로 방문 가능하게 되는 노드
    next_checker - True라면 해당 노드는 어떤 노드의 선행 조건
    '''
    def __init__(self, name):
        self.anc = None   
        self.name = name  
        self.conn = []
        self.condition = True
        self.condition_of = None
        self.next_checker = False  #True면 다음에 할 것?
        
    def make_path(self,node):
        '''
        해당 노드와 인자가 되는 노드의 conn에 서로를 추가
        '''
        self.conn.append(node)
        node.conn.append(self)
    
    def make_condition(self,node):
        '''
        조건 노드에 대해 처리
        '''
        self.condition_of = node
        node.condition = False
    
    def get_anc(self,anc):
        '''
        노드의 부모를 찾아줌.
        '''
        self.anc = anc
        for son in self.conn:
            if son != self.anc:
                son.get_anc(self)
                
    def search(self):
        '''
        노드에서 탐색을 진행. 하위 노드로 이어지며 방문 가능한 노드를 따라 내려간다.
        방문할 노드가 선행 조건이 달성되었거나 없는지를 체크하며 방문한다.
        방문 가능한 노드가 어떤 노드의 선행조건이라면 후행 가능한 노드의 방문가능상태를 변경해준다. 
        재귀적으로 반복한다.
        첫 T/F 인자로 추가 방문이 있었는지를, 두번째 인자는 이후 체크 할 노드를, 마지막으로 make_true로 조건을 몇 개 달성했는지를 반환한다.
        '''
        rt = []
        if self.condition == False:
            self.next_checker = True
            return False, [], 0
        else:
            self.next_checker = False
            make_true = 0
            if self.condition_of != None:
                self.condition_of.condition = True
                if self.condition_of.next_checker == True:
                    rt.append(self.condition_of)
                make_true += 1
            for nd in self.conn:
                if nd == self.anc:
                    continue
                else:
                    _,to_do, true_sum = nd.search()
                    rt.extend(to_do)
                    make_true += true_sum
            return True, rt, make_true
        
    def __repr__(self):
        return str(self.name)

def solution(n, path, order):
    ndlist = [Node(i) for i in range(n)]    # 노드생성
    answer = True
    for a,b in path:                        # 노드간 커넥션 정보 생성
        ndlist[a].make_path(ndlist[b])
    
    for a,b in order:                       # 노드간 선행/후행 방문조건 주입
        ndlist[a].make_condition(ndlist[b])
    
    ndlist[0].get_anc(None)                 #노드간 부모정보 주입
        
    to_do = [ndlist[0]]
    new_added = True
    checker = 0
    while new_added:                        # 전전 사이클과 이번 사이클에 방문 가능 노드에 변화가 없다면 정지
        next_to_do = []           
        new_added = False
        for nd in to_do:
            a,b,c = nd.search()             
            new_added = a | new_added       # 추가 방문 가능 노드가 생기면 a는 True이며, 그렇지 않다면 false이다.
            next_to_do.extend(b)            # 이후 탐색 가능한 노드 리스트에 b를 추가해준다.
            checker += c                    # 만족한 조건의 합산을 저장한다.
        to_do = next_to_do
        
    if checker == len(order):               # 주어진 조건을 모두 달성했다면 모든 노드 방문 가능, 그렇지 않다면 불가능이다.
        return True
    return False
