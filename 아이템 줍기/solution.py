def solution(rectangle, characterX, characterY, itemX, itemY):
    answer = 0
    N = 51
    S = [[9 for i in range(N)]for j in range(N)]
    for x1,y1,x2,y2 in rectangle:
        for x in range(x1,x2):
            if S[x][y1] == 9 or S[x][y1] == 3:
                S[x][y1] = 0                      # 0 우 1 하 2 좌 3 상으로 표현. 외곽 순회 방향을 표시.
        for y in range(y1,y2):
            if S[x2][y] == 9 or S[x2][y] == 2:
                S[x2][y] = 3
        for x in range(x1+1,x2+1):
            if S[x][y2] == 9 or S[x][y2] == 1:
                S[x][y2] = 2
        for y in range(y1+1,y2+1):
            if S[x1][y] == 9 or S[x1][y] == 0:
                S[x1][y] = 1

    x,y = characterX,characterY
    answer = 0
    while x!=itemX or y!=itemY:
        answer += 1
        if S[x][y] == 0:
            x+=1
        elif S[x][y] == 1:
            y-=1
        elif S[x][y] == 2:
            x-=1
        elif S[x][y] == 3:
            y+=1
        else:
            return ('e')
    
    temp = 0
    while x!=characterX or y!=characterY:
        temp += 1
        if S[x][y] == 0:
            x+=1
        elif S[x][y] == 1:
            y-=1
        elif S[x][y] == 2:
            x-=1
        elif S[x][y] == 3:
            y+=1
        else:
            return ('e')
    
    answer = min(answer,temp)
    return answer
