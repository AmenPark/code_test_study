def solution(n, s, a, b, fares):
    def get_kdic(dic,k,maxfee):
        '''
        노드 k를 중심으로 다른 노드들에 대한 도달 비용의 사전을 반환한다.
        각 값은 최대비용을 넘을 수 없다.
        '''
        rt = {k : 0}
        to_do = {(k,nd) for nd in dic[k].keys()}
        while len(to_do):
            next_do = set()
            for bef,aft in to_do:
                newfee = rt[bef] + dic[bef][aft]
                if rt.get(aft,maxfee) > newfee:
                    rt[aft] = newfee
                    next_do = next_do.union({(aft,nd)for nd in dic[aft].keys()})
            to_do = next_do
        return rt
                
    faredic = {}
    maxfee = 0
    for x,y,fee in fares:
        maxfee += fee   #모든 노선비용의 합산을 최대비용이라 하면 노드간 거리는 이 비용을 넘을 수 없다.
        try:                      #x노드에서 y, y노드에서 x로의 이동에 대한 비용 fee를 처리해준다.
            faredic[x][y] = fee
        except:
            faredic[x] = {y:fee}
        try:
            faredic[y][x] = fee
        except:
            faredic[y] = {x : fee}
    adic = get_kdic(faredic,a,maxfee)     # a를 기준으로 탐색. 노드별 도달비용을 구한다.
    bdic = get_kdic(faredic,b,maxfee)     # b를 기준으로 탐색.
    sdic = get_kdic(faredic,s,maxfee)     # s를 기준으로 탐색.
    answer = maxfee
    for k in range(1,n+1):                # 각 노드를 기준으로 세 노드까지의 길이합이 가장 작은 것을 고른다.
        a = adic.get(k,None)
        b = bdic.get(k,None)
        c = sdic.get(k,None)
        try:
            ksum = a+b+c
            answer = min(answer,ksum)
        except:
            continue
            
    return answer
