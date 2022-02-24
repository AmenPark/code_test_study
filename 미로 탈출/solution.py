class node:
    '''
    각 방을 노드로 표현했다.
    name: 해당 방의 이름.
    dp: 방의 방문기록. status: cost로 기록한다.
    arrow_in, out, trap_in, out: 외부에서 들어오거나 나가는 연결된 길. 연결된 반대편이 트랩이라면 trap_으로 처리. 이름:코스트로 type은 dict.
    trap_status : 1,2,4...로 trap을 기록. status ^= trap_status로 해당 방을 방문하면 status가 변경된다.
    '''
    def __init__(self, name):
        self.name = name
        self.dp = {}
        self.arrow_in = {}
        self.arrow_out = {}
        self.trap_in = {}
        self.trap_out = {}
        self.trap_status = 0    #1, 2, 4... 로 ^연산으로 최종 스테이터 반영. 일반은 0
    def __repr__(self):
        return repr(self.dp)
        
def solution(n, start, end, roads, traps):
    answer = 0
    ndlist = {i : node(i) for i in range(1,n+1)}
    trap_val = 1
    trap_dict = {}
    for t in traps:
        # trap에 대한 처리.
        trap_dict[t] = trap_val
        ndlist[t].trap_status = trap_val
        trap_val <<= 1
        
    for starts, ends, cost in roads:
        # 노드 사이의 연결관계 처리
        if trap_dict.get(ends,False):
            ndlist[starts].trap_out[ends] = min(cost,ndlist[starts].trap_out.get(ends,99999))
        else:
            ndlist[starts].arrow_out[ends] = min(cost,ndlist[starts].arrow_out.get(ends,99999))
            
        if trap_dict.get(starts,False):
            ndlist[ends].trap_in[starts] = min(cost, ndlist[ends].trap_in.get(starts,99999))
        else:
            ndlist[ends].arrow_in[starts] = min(cost,ndlist[ends].arrow_in.get(starts,99999))
    
    todo = {0 : [(start,0)]}
    ndlist[start].dp[0] = 0
    while True:
        # 너비우선탐색. 각 방에서 할 수 있는 모든 행동을 todo에 cost : [(노드넘버, status), ...] 꼴이 되도록 한다.
        # cost를 최소로 해서 탐색해가며, 해당 노드의 dp[status]를 검사해서 중복을 피한다.
        # 탐색 결과 목적지가 일찍 나올 수 있으나 cost가 적어야 하므로 목적지가 탐색 출발점이 될 때 까지 충분히 탐색해야 한다.
        answer = (min(todo.keys()))
        now = todo[answer]
        for ndnum, status in now:
            if ndlist[ndnum].dp[status] < answer:
                continue
            if ndlist[ndnum].trap_status & status:
                #이번에 출발하려는 곳이 뒤집힘. trap을 밟은 상태이기 때문.
                for ndval, cost in ndlist[ndnum].arrow_in.items():  # 뒤집혔으므로 arrow_out은 상관x.
                    next_time = answer + cost
                    if ndlist[ndval].dp.get(status,next_time + 1) > next_time:
                        ndlist[ndval].dp[status] = next_time
                        try:
                            todo[next_time].append((ndval,status))
                        except:
                            todo[next_time] = [(ndval,status)]
                            
                for ndval, cost in ndlist[ndnum].trap_in.items(): # 트랩과 연결된 경우에는 들어오는 화살표는 상대쪽에 방문으로 뒤집힌 상태가 아니어야만 한다.(이미 뒤집힘)
                    next_time = answer + cost
                    if status & ndlist[ndval].trap_status:
                        continue
                    next_status = ndlist[ndval].trap_status ^ status
                    if ndlist[ndval].dp.get(next_status,next_time + 1) > next_time:
                        ndlist[ndval].dp[next_status] = next_time
                        try:
                            todo[next_time].append((ndval,next_status)) # trap이 발동되었으므로 status -> next_status로 변경된다.
                        except:
                            todo[next_time] = [(ndval,next_status)] # todo에 해당 리스트가 없을경우(defaultdict가 아니라서) 처리해주기 위함.
                            
                for ndval, cost in ndlist[ndnum].trap_out.items():  # 트랩과 연결된 상태인데 원래 나가는 화살표는 두 번 뒤집혀야 사용 가능하다.
                    if status & ndlist[ndval].trap_status:
                        next_time = answer+cost
                        next_status = status ^ ndlist[ndval].trap_status
                        if ndlist[ndval].dp.get(next_status,next_time+1) > next_time:
                            ndlist[ndval].dp[next_status] = next_time
                            try:
                                todo[next_time].append((ndval,next_status))
                            except:
                                todo[next_time] = [(ndval,next_status)]
                            
            else:
                #이번에 출발하려는 곳이 뒤집히지 않음
                for ndval, cost in ndlist[ndnum].arrow_out.items():
                    next_time = answer + cost
                    if ndlist[ndval].dp.get(status,next_time + 1) > next_time:
                        ndlist[ndval].dp[status] = next_time
                        try:
                            todo[next_time].append((ndval,status))
                        except:
                            todo[next_time] = [(ndval,status)]
                    
                for ndval, cost in ndlist[ndnum].trap_out.items():
                    next_time = answer + cost
                    if status & ndlist[ndval].trap_status:
                        continue
                    next_status = ndlist[ndval].trap_status ^ status
                    if ndlist[ndval].dp.get(next_status,next_time + 1) > next_time:
                        ndlist[ndval].dp[next_status] = next_time
                        try:
                            todo[next_time].append((ndval,next_status))
                        except:
                            todo[next_time] = [(ndval,next_status)]
                            
                for ndval, cost in ndlist[ndnum].trap_in.items():
                    if status & ndlist[ndval].trap_status:
                        next_time = answer+cost
                        next_status = status ^ ndlist[ndval].trap_status
                        if ndlist[ndval].dp.get(next_status,next_time+1) > next_time:
                            ndlist[ndval].dp[next_status] = next_time
                            try:
                                todo[next_time].append((ndval,next_status))
                            except:
                                todo[next_time] = [(ndval,next_status)]
        del todo[answer]  #이미 시작점이 된 곳이므로 제거.
        if len(ndlist[end].dp) > 0: # 도착점 dp가 존재. 즉 경로를 찾음
            if min(ndlist[end].dp.values()) <= answer:  # 계속 탐색해서 도착점이 시작점으로 탐색핼 때가 되어서야 반복을 중단해야함.
                break
    return answer
