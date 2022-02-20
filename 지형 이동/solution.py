def alreadyconn(connected,i,j):
    '''
    connected - dict로 key-value쌍이 연결되어 있음을 기록한 지표.
    connected[i] = j 일 경우 둘은 연결되어 있음을 표시한다.
    connected는 언제나 작거나 같은 방향으로 이동시켜주며, i,j의 최종 도착지를 반환하는 함수.
    '''
    while i != connected[i] :
        i = connected[i] 
    while j != connected[j] :
        j = connected[j] 
    return i,j
  
def get_same_land(land, height, dic, i, j, mark_num, dic2, ladderdic):
    '''
    같은 땅인지를 체크하는 함수.
    land : 땅 정보
    height : 높이 제한
    dic : 위치좌표- 영역 쌍의 사전.
    i, j: 정수. 위치정보
    mark_num : 마킹넘버. 이번에 마킹하는 영역에 부여되는 고유 넘버
    dic2 : dic의 역 사전. 영역(mark_num)을 넣으면 위치좌표의 리스트가 나온다.
    ladderdic: 영역 a,b쌍을 키로, 두 영역을 직접 연결하는 최소비용을 값으로 하는 사전.
    리턴은 없는 함수로 각 인자로 받은 사전에 영역을 추가하거나 수정하는 작업이다. 특히 ladderdic을 완성하기 위함.
    '''
    stack = [(i,j)]
    N = len(land)
    while stack:    # 탐색을 통해서 영역의 구성을 탐색하는 방식이다.
        x,y = stack[-1]
        if dic.get((x,y),0) == 0:
            dic[(x,y)] = -1
            if x+1 < N :
                if dic.get((x+1,y),0) == 0:
                    if abs(land[x][y]-land[x+1][y]) <= height:
                        x+=1
                        stack.append((x,y))
                elif dic[(x+1,y)] != mark_num and dic[(x+1,y)]>0:
                    mark_num2 = dic[(x+1,y)]
                    small, high = min(mark_num,mark_num2), max(mark_num,mark_num2)
                    ladderdic[(small,high)] = min(abs(land[x][y]-land[x+1][y]),ladderdic.get((small,high),10000))
                    
        elif dic.get((x,y),0) == -1:
            dic[(x,y)] -= 1
            if y+1 < N :
                if dic.get((x,y+1),0) == 0:
                    if abs(land[x][y]-land[x][y+1]) <= height:
                        y+=1
                        stack.append((x,y))
                elif dic[(x,y+1)] != mark_num and dic[(x,y+1)]>0:
                    mark_num2 = dic[(x,y+1)]
                    small, high = min(mark_num,mark_num2), max(mark_num,mark_num2)
                    ladderdic[(small,high)] = min(abs(land[x][y]-land[x][y+1]),ladderdic.get((small,high),10000))
        elif dic.get((x,y),0) == -2:
            dic[(x,y)] -= 1
            if x>0 :
                if dic.get((x-1,y),0) == 0:
                    if abs(land[x][y]-land[x-1][y]) <= height:
                        x-=1
                        stack.append((x,y))
                elif dic[(x-1,y)] != mark_num and dic[(x-1,y)]>0:
                    mark_num2 = dic[(x-1,y)]
                    small, high = min(mark_num,mark_num2), max(mark_num,mark_num2)
                    ladderdic[(small,high)] = min(abs(land[x][y]-land[x-1][y]),ladderdic.get((small,high),10000))
        elif dic.get((x,y),0) == -3:
            dic[(x,y)] -= 1
            if y>0 :
                if dic.get((x,y-1),0) == 0:
                    if abs(land[x][y]-land[x][y-1]) <= height:
                        y-=1
                        stack.append((x,y))
                elif dic[(x,y-1)] != mark_num and dic[(x,y-1)]>0:
                    mark_num2 = dic[(x,y-1)]
                    small, high = min(mark_num,mark_num2), max(mark_num,mark_num2)
                    ladderdic[(small,high)] = min(abs(land[x][y]-land[x][y-1]),ladderdic.get((small,high),10000))
        elif dic.get((x,y),0) == -4:
            dic[(x,y)] = mark_num
            temp = dic2.get(mark_num,[])
            temp.append((x,y))
            dic2[mark_num] = temp
            stack.pop()


def solution(land, height):
    answer = 0
    landmark = {}       #(i,j) -> number.
    N = len(land)
    mark_num = 0
    marktoland = {}     #number -> list of (i,j) with color number
    dic_ladder_cost = {} #(marki,markj) -> mincost for i->j
    # 주어진 정보를 가공하는 과정이다. 영역을 찾고 영역별 연결비용을 구한다.
    for i in range(N):
        for j in range(N):
            if landmark.get((i,j),0) == 0:
                mark_num += 1
                get_same_land(land,height,landmark,i,j,mark_num, marktoland, dic_ladder_cost)
            else:
                continue
    
    # 영역-영역 : 연결비용의 dic을 뒤집는다. 직접 생성하지 않는 이유는 추가 영역이 오픈되면서 연결비용 감소될 가능성이 있기 때문이다. key 업데이트는 value 업데이트보다 복잡하다.
    dic_cost_to_ij = {}
    for i,j in dic_ladder_cost.keys():
        temp = dic_cost_to_ij.get(dic_ladder_cost[(i,j)],[])
        temp.append((i,j))
        dic_cost_to_ij[dic_ladder_cost[(i,j)]] = temp
    
    idx = 0
    conn = mark_num - 1
    
    k = list(dic_cost_to_ij.keys())
    k.sort()
    connected = [i for i in range(mark_num+1)]
    # 최소연결비용을 찾는다. 코스트를 작은 것 부터 선회하며 이미 연결된 것인지만 체크하면서 N개의 영역이면 N-1개의 연결을 하면 된다.
    for key in k:
        to_check = dic_cost_to_ij[key]
        for a1,b1 in to_check:
            i,j = alreadyconn(connected,a1,b1)
            if i == j:
                continue
            else:
                answer += key
                idx += 1
                connected[max(i,j)] = min(i,j)
                if idx == conn:    
                    break
    return answer
