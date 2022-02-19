def up(board,r,c, ctrl):
    '''
    board : 현재 보드의 상황
    r : 열 위치
    c : 행 위치
    ctrl : 뛰어넘기 이동 사용여부.
    위로 이동했을 경우의 위치, 또는 뛰어넘기 위로 이동했을 경우의 위치 반환.
    4x4이므로 3을 그대로 사용했다. 확장을 위해서는 이를 바꿀 필요성 존재. 좋은 코드는 아니다.
    '''
    if r == 3:
        return (r,c)
    else:
        if ctrl == True:
            r+=1
            while(board[r][c]== 0 and r < 3):
                r+=1
            return (r,c)
        else:
            return (r+1,c)
    
def down(board,r,c, ctrl):
    if r == 0:
        return (r,c)
    else:
        if ctrl == True:
            r-=1
            while(board[r][c]== 0 and r > 0):
                r-=1
            return (r,c)
        else:
            return (r-1,c)
    
def right(board,r,c,ctrl):
    if c == 3:
        return r,c
    else:
        if ctrl == True:
            c+=1
            while(board[r][c]== 0 and c < 3):
                c+=1
            return (r,c)
        else:
            return r,c+1

def left(board,r,c, ctrl):
    if c == 0:
        return r,c
    else:
        if ctrl == True:
            c-=1
            while(board[r][c]== 0 and c > 0):
                c-=1
            return (r,c)
        else:
            return r,c-1

def get_rootnum(board,r,c,target):
    '''
    board : 현 상황
    r, c : 현 커서 위치
    target: 커서를 이동하기 위한 위치
    너비우선탐색을 통해 r,c -> target의 최소 입력 수를 반환한다.
    target선택이 존재하므로 이동수치 + 1을 반환.
    '''
    dp = [[-1 for _ in range(4)]for _ in range(4)]  # 탐색을 위한 dp.
    dp[r][c] = 0                                    # 현 위치는 0번이동.
    func = [up,down,left,right]                     # 각 원소는 위의 함수들이다.
    movenum = 0                                     # 현재 이동입력수
    now = [(r,c)]                                   # 현재 살필 위치
    targetr, targetc = target                       # 목표 위치
    while dp[targetr][targetc] == -1:               # 목표값이 -1에서 갱신이 될 때까지 반복
        next_now = []                               # 이번 반복에서 갱신될 좌표를 넣기 위한 리스트
        movenum += 1                                # 이번 반복에서 이동입력수는 1 증가한다.
        for posr, posc in now:                                  # 현재 가능한 위치들에 대해서
            for fun in func:                                    # 각각 가능한 이동방법에 대해서
                for tf in [True,False]:                         # 뛰어넘기 이동여부 인자도 모두 포함
                    nextr, nextc = fun(board,posr,posc,tf)      # 이동 행동의 결과물을 받음
                    if dp[nextr][nextc] == -1:                  # dp에 기록되지 않았다면
                        next_now.append((nextr,nextc))          # 다음에 이동의 시작점이 된다.
                        dp[nextr][nextc] = movenum              # dp에 기록해서 중복을 피한다.
        now = next_now                              # 현재 위치를 갱신한다.
    return dp[targetr][targetc] + 1                 # 목표 위치까지 이동 수 + 선택 입력(1)을 반환.
        
def get_best(copyboard, r, c, status, cardnum, posdic, statusdic):
    '''
    copyboard : 현 보드의 상황. 코드상에서는 원본을 복원하기에 그대로 사용한다.
    r,c : 현 커서의 위치
    status : 2진수로 나타낼 경우 제거되지 않은 카드의 상태. 1101이면 카드 네 장중 2번카드가 제거된 상태.
    cardnum : 남은 카드의 수. status와 상관관계가 있다.
    posdic : 카드의 위치를 담은 dict. {1:[(x1,y1),(x2,y2)], ...}와 같은 형식. key는 1,2,4,8,...로 주어지며 이는 status와 연계하기 위함이다.
    statusdic : status, r,c에 의해 문제가 해결되는 방식이므로 이전의 상황이 달라도 이 셋이 같다면 이후의 계산은 동일하다.
               이 반복을 피하기 위해 dp를 사용하기 위한 장치.
    '''
    dccode = bin(status) + '.' + str(r) + '.' + str(c)  # 현 board, r,c를 문자열로 변환한다. dp를 위한 장치.
    if statusdic.get(dccode,-1) > 0:    # 이전에 최소방법을 계산했다면 다시 계산할 필요가 없다.
        return statusdic[dccode]
    if cardnum == 1:                    # 하나의 카드만 뒤집으면 끝인 경우이다.
        targeta, targetb = posdic[status]
        ar, ac = targeta
        br, bc = targetb
        rt1 = get_rootnum(copyboard,r,c,targeta) + get_rootnum(copyboard,ar,ac, targetb)
        rt2 = get_rootnum(copyboard,r,c,targetb) + get_rootnum(copyboard,br,bc, targeta)
        statusdic[dccode] = min(rt1,rt2)
        return min(rt1,rt2)
    else:
        trynum = 0
        targetnum = 1   
        min_var = 999999        # 답은 이것보다 작은 수임을 알기에 이 수를 넣었다. 확장성을 생각한다면 좋은 방법은 아니다. 다른 방법으로 충분히 대체 가능하다.
        while trynum < cardnum:             # 카드가 4쌍 남아있다면 4가지 선택 가능성이 생긴다.
            if targetnum & status == 0:     # 카드가 이미 뒤집혔는지를 체크한다.
                targetnum <<= 1
            else:
                trynum += 1
                targeta, targetb = posdic[targetnum]    #target이 되는 카드는 한 쌍이므로 두 개의 좌표쌍이 나온다.
                ar,ac = targeta
                br,bc = targetb
                
                # a,b쌍 카드를 없애는 방법은 현 커서위치에서 a로 이동(+선택) 이후 b로 이동(+선택)의 최소값. 혹은 그 반대.
                rt1 = get_rootnum(copyboard,r,c,targeta) + get_rootnum(copyboard,ar,ac, targetb)
                rt2 = get_rootnum(copyboard,r,c,targetb) + get_rootnum(copyboard,br,bc,targeta)
                
                # 해당 카드를 0으로 없앤 뒤 다음 함수에 전달한다. 카드를 제거했으므로 xor연산을 통해 status를 갱신하여 넘겨줘야 한다.
                deleted = copyboard[ar][ac]
                copyboard[ar][ac] = 0
                copyboard[br][bc] = 0
                next_status = targetnum^status
                
                # 동일 형태이므로 재귀가 가능.
                rt1 += get_best(copyboard,br,bc,next_status,cardnum-1,posdic, statusdic)
                rt2 += get_best(copyboard,ar,ac,next_status,cardnum-1,posdic, statusdic)
                
                # board를 수정 사용했으므로 복원한다.
                copyboard[br][bc] = deleted
                copyboard[ar][ac] = deleted
                
                min_var = min(min_var,rt1,rt2)
                targetnum<<=1
                
        # 최소가 되는 경우의 수를 statusdic에 기록하며, 이 때의 값을 반환한다.
        statusdic[dccode] = min_var
        return min_var
               

def solution(board, r, c):
    posdic = {}
    cardnum = 0
    statusdic = {}
    for i, line in enumerate(board):
        for j, var in enumerate(line):
            if var > 0:
                try:
                    posdic[1<<(var-1)].append((i,j))
                except:
                    posdic[1<<(var-1)] = [(i,j)]
                    cardnum += 1
    status = (1<<cardnum) - 1
    answer = get_best(board,r,c,status,cardnum, posdic, statusdic)
    
    return answer
