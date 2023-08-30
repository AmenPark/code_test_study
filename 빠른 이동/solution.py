def solution(n, roads):
    answer = 0
    conns=[set() for _ in range(n+1)]           #어디로 갈 수 있는가
    reprValue=[i for i in range(n+1)]           #사이클의 대표값
    def getRepr(i):                             #대표값 구하기
        if i==reprValue[i]:
            return i
        else:
            reprValue[i]=getRepr(reprValue[i])
            return reprValue[i]
    def updateRepr(i,b):                        #대표값 업데이트하기
        i = getRepr(i)
        reprValue[i] = getRepr(b)
        
    for a,b in roads:                           #연결 채우고
        conns[a].add(b)                          
    status=[0]*(n+1)                            #깊이우선탐색에 쓰는 변수. 전-0, 중-1, 후-2
    idx=[0]*(n+1)                               #몇번째 깊이에 있는가
    
    def getCycleToOne(now, stack=[]):
        status[now]=1
        idx[now]=len(stack)
        nowDepth=len(stack)
        stack.append(now)
        for tg in list(conns[now]):
            tg=getRepr(tg)
            if status[tg]==0:
                nowDepth= min(getCycleToOne(tg, stack),nowDepth)
            elif status[tg]==2:
                continue
            else:
                if nowDepth>idx[tg]:
                    nowDepth=idx[tg]
        status[now]=2
        if nowDepth<idx[now]:
            updateRepr(now, stack[nowDepth])
            conns[stack[nowDepth]].update(conns[now])
        stack.pop()
        return nowDepth
    getCycleToOne(1)
    del(status)
    del(idx)
    
    nds = []                              #대표만 모아둠. 사이클은 하나의 노드로.
    for i in range(1,n+1):
        if getRepr(i)!=i:
            continue
        nds.append(i)
        conns[i]=[getRepr(x) for x in conns[i] if getRepr(x)!=i]
        
    froms = {nd:[] for nd in nds}           #어디에서 오는가? conns의 역전.
    for nd in nds:
        for target in conns[nd]:
            froms[target].append(nd)
    
    uppers={nd:None for nd in nds}        #node in getUpper(nd)-> nd의 조상중 node가 있는가
    def getUppers(nd):
        if uppers[nd]!=None:
            return uppers[nd]
        else:
            rt=set()
            for upNode in froms[nd]:
                rt.add(upNode)
                rt.update(getUppers(upNode))

            uppers[nd]=rt
            return rt
    for nd in nds:
        getUppers(nd)
    
    visited={i:0 for i in nds}              #탐색중 방문 체크용
    select={i:0 for i in nds}               #뭘 골랐는가?
    selectedBy={i:0 for i in nds}           #누가 골랐는가?
    conns = {nd:[i for i in nds if i in getUppers(nd)] for nd in nds}
    def b_match(nd):
        for nextNd in conns[nd]:
            if visited[nextNd]:
                continue
            visited[nextNd]=1
            if selectedBy[nextNd]==0 or b_match(selectedBy[nextNd]):
                select[nd]=nextNd
                selectedBy[nextNd]=nd
                return True
        return False
    cnt=0
    for nd in nds:
        if(b_match(nd)):
            cnt+=1
        visited={i:0 for i in nds}
    return len(conns)-cnt-1
