def link_dict(edges):
    '''
    노드 연결정보를 기록.
    findanc에는 부모 노드와의 관계를 기록한다.
    dic에는 자식 노드의 리스트를 기록한다.
    '''
    dic = {}
    findanc = {}
    for edge in edges:
        anc, son = edge
        findanc[son] = anc
        try:
            dic[anc].append(son)
        except:
            dic[anc] = [son]
    return dic, findanc

def get_sheep(now, possible_node, node_dict, checker, sheeps, wolves, info):
    '''
    주어진 상황이 같다면 결과가 변하지 않는다는 점에서 착안한 재귀 형태의 반복문의 함수형태.
    now - 현 상황. 각 노드를 이진수열로 하여 방문한 노드는 1, 아닌 노드는 0으로 표현.
    possible_node - 현 상황에서 방문 가능한 노드 리스트. 방문했던 노드와 인접한 모든 노드가 여기에 포함된다.
    node_dict - 노드에 대한 자식 노드 리스트의 사전.
    checker - 노드에 대한 방문기록.
    sheeps - 모은 양의 숫자
    wolves - 모은 늑대 숫자
    info - 문제에 주어진 그대로의 리스트. 노드에 있는 것이 늑대인가 양인가에 대한 정보..
    '''
    if len(possible_node) == 0 or wolves >= sheeps: # 늑대 수가 양 이상이거나 모든 노드 방문된 상태라면 그냥 반환
        return sheeps
    max_sheeps = sheeps
    for next_node in possible_node:  # 방문 가능한 모든 노드에 대해 탐색.
        next_node_bin = 1<<next_node  # now관련 연산을 위한 이진표현
        next_now = now | next_node_bin  # 비트연산을 통해서 방문상태를 표현하기 위함
        if checker.get(next_now,None) != None:
            continue
        else:
            checker[next_now] = True
            next_possible_node = [node for node in possible_node if node != next_node]
            next_possible_node.extend(node_dict.get(next_node,[]))
            if info[next_node] == 0:  # 다음 노드가 양이라면 양 수가 1 증가.
                max_sheeps = max(max_sheeps, get_sheep(next_now, next_possible_node, node_dict,
                                                  checker, sheeps+1, wolves, info))
            else:                     # 다음 노드가 늑대라면 늑대 수가 1 증가
                max_sheeps = max(max_sheeps, get_sheep(next_now, next_possible_node, node_dict,
                                                  checker, sheeps, wolves+1, info))
    return max_sheeps
            
            

def solution(info, edges):
    answer = 1
    node_dict, anc_dic = link_dict(edges)
    
    possible_node = node_dict[0][:]
    sheeps = 1
    wolves = 0
    now = 1
    checker = {0:True}
    
    return get_sheep(now, possible_node, node_dict, checker, sheeps, wolves, info)
