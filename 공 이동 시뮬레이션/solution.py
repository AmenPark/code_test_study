def solution(n, m, x, y, queries):
    mindic = {'l' : 0,'r' : 0,'u' : 0,'d' : 0}
    maxdic = {'l' : m-1,'r' : m-1,'u': n-1,'d' : n-1}
    inc = {'l' : -1,'r' : 1,'u' : -1,'d' : 1}
    pair = {'l' : 'r','r' : 'l','u': 'd','d' : 'u'}
    var = {'l' : 1,'r':1,'u':1,'d':1}
    pos = {'l' : 0,'r' : m-1,'u' : 0,'d' : n-1}
    cmd = {0 : 'l', 1 : 'r',2 : 'u',3 : 'd'}
    
    # 쿼리 처리.
    for q, n in queries:
        aw = cmd[q]
        opaw = pair[aw]
        pos[opaw] += inc[aw] * n
        pos[aw] += inc[aw] * n
        if pos[opaw] <= mindic[opaw] :
            var[opaw] = maxdic[opaw] + 1
            var[aw] = maxdic[opaw] + 1
            pos[aw] = 0
            pos[opaw] = 0
        elif pos[opaw] >= maxdic[opaw]:
            var[opaw] = maxdic[opaw] + 1
            var[aw] = maxdic[opaw] + 1
            pos[aw] = maxdic[opaw]
            pos[opaw] = maxdic[opaw]
        elif pos[aw] < mindic[aw]:
            var[aw] += mindic[aw] - pos[aw]
            pos[aw] = mindic[aw]
        elif pos[aw] > maxdic[aw]:
            var[aw] += pos[aw] - maxdic[aw]
            pos[aw] = maxdic[aw]
    
    # 해답 구간 계산
    answer = 1        
    if pos['l'] > y or pos['r'] < y:
        return 0
    if pos['u'] > x or pos['d'] < x:
        return 0
    if x == pos['u']:
        answer *= var['u']
    elif x == pos['d']:
        answer *= var['d']
    if y == pos['l']:
        answer *= var['l']
    elif y == pos['r']:
        answer *= var['r']
    return answer
