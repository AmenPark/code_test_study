def solution(n, weak, dist):
    answer = -1
    # 한 바퀴를 도는 것이기에 중간에 시작해서 한 바퀴 돌아도 문제 없도록 동일 간격으로 두 바퀴째를 생성. 한 바퀴 길이만큼 체크하면 중복되지 않는다.
    weak_round = [weak[i%len(weak)] if i < len(weak) else weak[i-len(weak)]+n  for i in range(2 * len(weak))]
    
    # 0번, 첫 약점부터 해서 마지막 약점까지 첫 시작점으로 잡을 곳을 어디인지 모두 시도한다.
    start_ind = 0
    while start_ind < len(weak):
        start_pos = weak[start_ind]
        now_ind = [start_ind]
        checker = {0 : 1}
        friends = []
        friends.append(0)
        l = 1
        
        # friends에 모든 순서대로 중복 없이 인원을 투입하며, 각 경우 최선의 방법으로 다음 취약점부터 시작해서 최대한 많은 점을 커버하도록 하여 최소 인원 투입을 알아낸다.
        while(l > -1):
            if len(friends) == l:  #길이 늘리기
                now_ind.append(now_ind[-1])
                pos = weak_round[now_ind[-1]] + dist[friends[-1]]
                while weak_round[now_ind[-1]] <= pos:
                    now_ind[-1] += 1
                    if now_ind[-1] == len(weak_round):
                        break
                
                if now_ind[-1] >= start_ind + len(weak):
                    if answer == -1:
                        answer = l
                    else:
                        answer = min(l,answer)
                    l -= 2
                    now_ind.pop()
                    continue
                else:
                    friends.append(0)
            elif len(friends) >= l + 2:    #짧게. 하나 뒤로
                checker[friends.pop()] = 0
                now_ind.pop()
                #now_ind.pop()
                
                if len(friends) == 0:
                    break
                checker[friends[-1]] = 0
                friends[-1] += 1
            elif friends[-1] == len(dist):                   #인덱스 초과
                l -= 1
            elif checker.get(friends[-1],0) == 1:    #이미 있을경우 
                friends[-1] += 1
            else:                                  #없음
                checker[friends[-1]] = 1
                l += 1
            
        start_ind += 1
            
    
    return answer
