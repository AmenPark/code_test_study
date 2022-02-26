class node:
    '''
    노드 선언. 하나의 노드는 하나의 사람을 의미
    var - 해당 인원이 창출해내는 값어치.
    boss - 해당 노드의 부모노드
    dp_boss - 해당 노드까지의 서브트리 기준에서 해당 노드가 포함될 경우의 매출 하락값
    dp_not - 해당 노드까지의 서브트리에서 매출 하락 최소지만 해당 노드는 미포함일 경우
    dp_mate - 자식노드들의 리스트
    '''
    def __init__(self,sale):
        self.var = sale
        self.boss = None
        self.dp_boss = None
        self.dp_not = None
        self.mate = []
        
    def get_dp_boss(self):
        '''
        해당 노드가 루트가 되는 서브트리 기준으로 해당 노드를 포함하면서 매출 하락이 최소가 될 경우
        이것은 자식 노드들의 매출 하락 최소 서브트리의 합에 해당 노드의 값을  더한 값이다.
        이 때 자식노드들의 매출 하락 최소값은 해당 자식노드 자체를 포함할 필요는 없다.
        '''
        if self.dp_boss == None:
            self.dp_boss = 0
            if len(self.mate) == 0:
                self.dp_boss = self.var
                return self.dp_boss
            else:
                for nd in self.mate:
                    self.dp_boss += min(nd.get_dp_boss(),nd.get_dp_not())
                self.dp_boss += self.var
                return self.dp_boss
        else:
            return self.dp_boss
          
    def get_dp_not(self):
        '''
        해당 노드가 루트가 되는 서브트리 기준으로 해당 노드가 포함되지 않으며 매출 하락이 최소가 되는 경우
        자식 노드들에 대해서 최솟값을 찾아서 다 더해주면 된다.
        다만 최상위 그룹에 대해서 누군가 하나가 포함되어야 하기 때문에 만약 모든 서브트리들이 루트를 미포함한다면 루트 포함과의 차이가 가장 적은 것을 루트가 포함하도록 바꿔준다.
        코드에서는 루트 포함과 미포함의 차이 중 가장 작은 것을 기억하고, 서브트리가 모두 루트 미포함일 경우 그 값을 추가로 더하는 것으로 해결하였다.
        '''
        if self.dp_not == None:
            self.dp_not = 0
            if len(self.mate) == 0:
                self.dp_not = 0
                return self.dp_not
            else:
                min_var = self.mate[0].dp_boss
                bosscheck = False
                for nd in self.mate:
                    if nd.get_dp_boss() < nd.get_dp_not():
                        bosscheck = True
                    if nd.get_dp_boss() - nd.get_dp_not() < min_var:
                        min_var = nd.dp_boss - nd.dp_not
                    self.dp_not += min(nd.get_dp_boss(),nd.get_dp_not())
                if bosscheck == False:
                    self.dp_not += min_var
                return self.dp_not
        else:
            return self.dp_not
          
def solution(sales, links):
    N = len(links) + 1
    nddic = {}
    for i in range(N):  #노드생성
        nddic[i+1] = node(sales[i])
        
    for a,b in links: #노드 관계 생성
        nddic[b].boss = nddic[a]
        nddic[a].mate.append(nddic[b])
        
    answer = min(nddic[1].get_dp_boss(),nddic[1].get_dp_not()) # 루트노드를 포함하거나, 포함하지 않거나 중 작은 것을 반환
    return answer
