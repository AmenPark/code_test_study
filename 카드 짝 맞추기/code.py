def up(board,r,c, ctrl):
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
    dp = [[-1 for _ in range(4)]for _ in range(4)]
    dp[r][c] = 0
    func = [up,down,left,right]
    movenum = 0
    now = [(r,c)]
    targetr, targetc = target
    while dp[targetr][targetc] == -1:
        next_now = []
        movenum += 1
        for posr, posc in now:
            for fun in func:
                for tf in [True,False]:
                    nextr, nextc = fun(board,posr,posc,tf)
                    if dp[nextr][nextc] == -1:
                        next_now.append((nextr,nextc))
                        dp[nextr][nextc] = movenum
        now = next_now
    return dp[targetr][targetc] + 1
        
def get_best(copyboard, r, c, status, cardnum, posdic, statusdic):
    dccode = bin(status) + '.' + str(r) + '.' + str(c)
    if statusdic.get(dccode,-1) > 0:
        return statusdic[dccode]
    if cardnum == 1:
        targeta, targetb = posdic[status]
        ar, ac = targeta
        br, bc = targetb
        rt1 = get_rootnum(copyboard,r,c,targeta) + get_rootnum(copyboard,ar,ac, targetb)
        rt2 = get_rootnum(copyboard,r,c,targetb) + get_rootnum(copyboard,br,bc,targeta)
        statusdic[dccode] = min(rt1,rt2)
        return min(rt1,rt2)
    else:
        trynum = 0
        targetnum = 1
        min_var = 999999
        while trynum < cardnum:
            if targetnum & status == 0:
                targetnum <<= 1
            else:
                trynum += 1
                targeta, targetb = posdic[targetnum]
                ar,ac = targeta
                br,bc = targetb
                rt1 = get_rootnum(copyboard,r,c,targeta) + get_rootnum(copyboard,ar,ac, targetb)
                rt2 = get_rootnum(copyboard,r,c,targetb) + get_rootnum(copyboard,br,bc,targeta)
                deleted = copyboard[ar][ac]
                copyboard[ar][ac] = 0
                copyboard[br][bc] = 0
                next_status = targetnum^status

                rt1 += get_best(copyboard,br,bc,next_status,cardnum-1,posdic, statusdic)
                rt2 += get_best(copyboard,ar,ac,next_status,cardnum-1,posdic, statusdic)
                copyboard[br][bc] = deleted
                copyboard[ar][ac] = deleted
                min_var = min(min_var,rt1,rt2)
                targetnum<<=1
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
