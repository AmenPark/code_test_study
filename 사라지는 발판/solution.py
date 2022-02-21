def solution(board,aloc,bloc):
    '''
    board : game board. 1 available, 0 no
    aloc : a's start location
    bloc : b's start location
    return : # of playing game turn
    '''
    stack = [[aloc],[bloc]]             #stack: 0 for a, 1 for b. player's location
    stack_best = [[None,None],[None]]   #stack_best: 0,1 for player. record the best case
    turn = 0#선수 - a가 움직일 차례        #turn: 0 or 1. which means player
    N = len(board)
    M = len(board[0])
    recorder = [[1],[]]                 #recorder: for each Players, check what to do next
    while True:
        pt_x,pt_y = stack[turn][-1]
        if recorder[turn][-1] == 5 or board[pt_x][pt_y] == 0:   #check for backtracking
            now_best = stack_best[turn][-1]
            before_best = stack_best[1-turn][-1]                #get the best case info
            if now_best == None:
                now_best = (0,0)
            if before_best == None:
                stack_best[1-turn][-1] = (1-now_best[0],now_best[1]+1)
            else:
                if before_best[0] == 0:
                    if now_best[0] == 0:
                        stack_best[1-turn][-1] = (1,now_best[1]+1)
                    else:
                        stack_best[1-turn][-1] = (0,max(now_best[1]+1,before_best[1]))
                else:
                    if now_best[0] == 0:
                        stack_best[1-turn][-1] = (1,min(before_best[1],now_best[1]+1))

            stack_best[turn].pop()
            stack[1-turn].pop()
            recorder[turn].pop()
            try:
                pt_x,pt_y = stack[1-turn][-1]   #stack[1] would be [] in endings
            except:
                break
            board[pt_x][pt_y] = 1
        else:
            if recorder[turn][-1] == 1:             #1-> move right
                next_x , next_y = pt_x+1 , pt_y
                if next_x ==N:
                    recorder[turn][-1] += 1
                    continue
            elif recorder[turn][-1] == 2:           #2 move down
                next_x , next_y = pt_x , pt_y+1
                if next_y == M:
                    recorder[turn][-1] += 1
                    continue
            elif recorder[turn][-1] == 3:           #3 move left
                next_x , next_y = pt_x-1 , pt_y
                if next_x == -1:
                    recorder[turn][-1] += 1
                    continue
            elif recorder[turn][-1] == 4:           #4 move up
                next_x , next_y = pt_x , pt_y-1
                if next_y == -1:
                    recorder[turn][-1] += 1
                    continue
            if board[next_x][next_y] == 0:          #if next pos has no board,
                recorder[turn][-1] += 1             #just do the next action
                continue
            recorder[turn][-1] += 1                 #check after you do under-process
            stack[turn].append([next_x,next_y])
            board[pt_x][pt_y] = 0
            stack_best[1-turn].append(None)
            recorder[1-turn].append(1)
        turn = 1-turn


    return stack_best[1][0][1] - 1  # -1 because we should check all of the a's move
                                    #after checks it all, b-t process.
                                    #with length +1, it would record in stack_best[1][0]
