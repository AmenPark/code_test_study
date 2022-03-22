class node:                           # 문제를 구체화 하는 과정에서 일단 만들어보고 시작했다. 사실 클래스로 만들 필요는 없었을 듯.
    def __init__(self,var):
        self.var = var
        self.conn = []
        self.m2t = {}
        self.t2m = {}
        
class edge:
    def __init__(self, start,end, money):
        self.start = start
        self.end = end
        self.money = money
        
def get_ans(dp_min,q,z,upperB):
    '''
    쿼리에 대한 답을 구하는 함수.
    z의 제곱 이하의 수에 대해서 dp로 구해두고, 그 이상의 값은 z**2 이하중 가장 큰 수와 %z가 같은 값을 고른다.
    가만히 있어도 z씩 벌기 때문인데, 상한이 z**2인 이유는 간단하다.
    %z가 같은 경로에 대해서는 n턴 기다리는 것 보다 더 적은 턴을 소모하는 경우가 없기 때문이다.
    %z 연산을 하면 z종류가 나오기 때문에, z개 넘는 경로는 중간에 대기타는 것과 동일하거나 더 긴 턴을 소모한다.
    '''
    if q < upperB:
        return dp_min.get(q,-1)
    else:
        de = q // z
        te = q % z
        var = te + z * (z-1)
        de -= z-1
        if var+z <  upperB:
            var += z
            de -= 1
        if dp_min.get(var,-1) == -1:
            return -1
        else:
            return dp_min[var] + de
        
def solution(n, z, roads, queries):
    ndlist = [node(i) for i in range(n)]          # 노드생성. 이렇게 클래스 쓸 필요까지는 없다.
    edgelist = []                                 # 이 문제의 주인공은 엣지이다. 엣지를 기준으로 문제를 풀어야 수월하다.
    for u,v,w in roads:
        e = edge(ndlist[u], ndlist[v], w)
        ndlist[u].conn.append(e)
        edgelist.append(e)

    upperB = z**2+1                               #상한선 설정. 사실 +1은 하나 마나이다.
    min_dict = {0 : 0}  # money -> turn           # 최소값 글로벌 사전을 만든다. 돈->턴.
    turn_dict = {0:[0], 1:[z]} # turn -> money    # 턴->돈의 리스트의 글로벌 사전.
    ndlist[0].m2t[0] = 0
    ndlist[0].t2m[0] = [0]
    for e in ndlist[0].conn:                      # 최초 0번도시 연결 edge는 1턴만에 이용 가능하므로 미리 처리를 해 준다. 0번에서 시작하는 조건 때문이다.
        if min_dict.get(e.money, None) == None :  # 글로벌 기준으로 이미 해당 돈을 버는데 걸리는 턴수가 중복인지 체크하기 위함.
            min_dict[e.money] = 1                 # 중복이 아니면 기입.
            turn_dict[1].append(e.money)          # 그 역 사전 또한 저장해둔다.
        e.end.m2t[e.money] = 1                    # 노드에 대해서도 사전을 작성한다. 최초 edge이용이므로 중복될 일은 없다.
        e.end.t2m[1] = [e.money]                  # 노드에 대한 사전. 그 역 버전도 작성.
    ndlist[0].m2t[z] = 1                          # 제자리에서 한 번 가만히 있는 경우. z원은 1턴. 1턴은 z원은 명백하다.
    ndlist[0].t2m[1] = [z]
    min_dict[z] = 1
    t = 2                                         # 반복문은 2턴부터 시작한다. 위의 것들은 1턴에서 행하는 것들이다.
    while len(turn_dict.get(t-2,[])):             # t-2턴, 즉 순간이동타는 경우가 있기에 전전턴이 없어야 반복이 종료된다.
        for m_before in turn_dict.get(t-1,[]):    # 글로벌 사전으로 이전 턴에서 대기를 타는 경우.
            now_m = m_before + z                  
            if now_m < upperB:                    
                if min_dict.get(now_m,False) == False:
                    min_dict[now_m] = t
                    try:
                        turn_dict[t].append(now_m)
                    except:
                        turn_dict[t] = [now_m]
                
        for e in edgelist:                      # 각 엣지에 대해 반복
            startnd = e.start
            endnd = e.end
            money = e.money
            for m_before in startnd.t2m.get(t-1,[]):    # 시작 도시에 t-1턴에 돈에 대해서.
                next_m = m_before + money               # 거기에 번 돈을 더해주면 현 턴의 돈.
                if next_m < upperB:                     # 제한을 넘기지 않는다면
                    if min_dict.get(next_m,False) == False: # 글로벌 최솟값 딕셔너리에 기록되지 않았을 경우
                        min_dict[next_m] = t                # 최솟값이므로 모두 갱신해야 한다.
                        try:
                            turn_dict[t].append(next_m)     
                        except:
                            turn_dict[t] = [next_m]
                        endnd.m2t[next_m] = t
                        try:
                            endnd.t2m[t].append(next_m)
                        except:
                            endnd.t2m[t] = [next_m]
                    elif min_dict.get(next_m,False) == t:           # 최솟값과 현 값이 동일한 경우
                        if endnd.m2t.get(next_m,False) == False:    # 끝 도시에 기록이 중복인지 체크
                            endnd.m2t[next_m] = t                   
                            try:
                                endnd.t2m[t].append(next_m)
                            except:
                                endnd.t2m[t]=[next_m]
                    else:   # 그 외의 경우. 즉 최솟값이 이미 있는 경우
                        pass    # a-b-c로 w원에 c에 도착하는 경우나 a-d로 w원 벌고 c순간이동하나 같으므로 패스.
                        
            for m_before in turn_dict.get(t-2,[]):                  # 두 턴 전의 돈 기록. 전체에서. 
                next_m = m_before + money                           # 텔포타고 와서 해당 엣지 이용하면 2턴. 현재 돈이다.
                if next_m < upperB:                                 # 상한을 넘지 않을 경우. 이하 위와 동일.
                    if min_dict.get(next_m,False) == False:
                        min_dict[next_m] = t
                        try:
                            turn_dict[t].append(next_m)
                        except:
                            turn_dict[t] = [next_m]
                        endnd.m2t[next_m] = t
                        try:
                            endnd.t2m[t].append(next_m)
                        except:
                            endnd.t2m[t] = [next_m]
                    elif min_dict.get(next_m,False) == t:
                        if endnd.m2t.get(next_m,False) == False:
                            endnd.m2t[next_m] = t
                            try:
                                endnd.t2m[t].append(next_m)
                            except:
                                endnd.t2m[t]=[next_m]
        t+=1
    answer = []
    for q in queries:
        answer.append(get_ans(min_dict,q,z,upperB))
    return answer
