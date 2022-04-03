def solution(a, s):
    def get_b(b):
        '''
        b 배열을 받아서 답, 즉 만들어지는 c의 총 가짓수를 리턴하는 함수.
        '''
        N = len(b)
        i = 1
        ct = 1
        record = [{} for _ in range(N)]
        record[0][b[0]] = (1,None)  #앞의 1은 몇 가지인지를 의미한다. 시작 상태는 한 가지이다. 뒤의 None은 다음 탐색타겟이 없음을 의미한다.
        while i<N:
            record[i][b[i]] = (ct,i-1)  #최초. i번째 세포 포함할 경우 ct만큼 가짓수를 의미. 합쳐질경우 이전 좌표로 돌아간다.
            var = b[i]                  #최신 값. 합쳐지지 않았으므로 b 배열의 값이 그대로이다.
            j = i-1                     #합쳐진다면 직전의 것과 합쳐지므로.
            while record[j].get(var,None)!=None:  # 기록을 조회. j번째에서 합치기 가능한 값이 있는 동안 반복.
                diff = record[j][var]             # 기록 값 조회.
                ct += diff[0]
                var *= 2                          # 합쳐지면 세포 내부 값은 두 배 이다.
                record[i][var] = diff
                j = diff[1]
                if j == None:
                    break
            i+=1
        return ct%(10**9 + 7)
        

    answer = []
    subsum = 0
    for x in s:
        b = a[subsum:subsum+x]
        subsum+=x
        answer.append(get_b(b))
    return answer
