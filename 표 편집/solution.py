def solution(n, k, cmd):
    def makesub(subset,n):
        '''
        데이터 저장 구조를 만들기 위한 함수.
        subset이라고 이름붙였지만 리스트이다.
        리스트는 [n, ...]꼴이다.
        '''
        if n<3: # 데이터 수가 1,2일경우. 1이면 [1,1], 2이면 [2,1,1]꼴로 첫 인자는 데이터 총 수량, 두,세번째 인자는 데이터 존재여부이다.
            subset.append(n)
            subset.append(1)
            if n == 2:
                subset.append(1)
        else: # 3개 이상의 데이터에 대해서는 S = [n, S1, S2]꼴로 인덱스 1,2에 하위 리스트를 포함한다.
            subset.append(n)
            subset.append([])
            subset.append([])
            n2 = n//2
            makesub(subset[1],n2)
            makesub(subset[2],n-n2)
    
    Z_stack = []
    def del_k(dataset,k):
        '''
        k를 받아 지운다. 지운 것은 어디 리스트에서 지운 것인지 알기위해 해당 리스트-dataset을 저장한다. 또한 지워진 데이터의 인덱스도 저장한다.
        차후 복원할때 Z_stack (외부에서 정의된 리스트이다)에서 인덱스와 리스트 주소를 가져와서 복원한다.
        '''
        Z_stack[-1].append(dataset)
        if dataset[1] == 1 or dataset[1] == 0:
            dataset[0] -= 1
            if k == 1:
                dataset[2] = 0
                Z_stack[-1].append(2)
            elif k == 0:
                if dataset[1]:
                    dataset[1] = 0
                    Z_stack[-1].append(1)
                else:
                    dataset[2] = 0
                    Z_stack[-1].append(2)
        else:
            dataset[0] -= 1
            if dataset[1][0] <= k:
                k -= dataset[1][0]
                del_k(dataset[2],k)
            else:
                del_k(dataset[1],k)
                
    def cmd_C(dataset,k):
        '''
        C 명령을 처리한다.
        현재 커서 위치 k에 대해 실행한다.
        커서가 마지막 칸이라면 한칸 앞으로 당긴다.
        '''
        Z_stack.append([])
        Z_stack[-1].append(k)
        del_k(dataset,k)
        if k == dataset[0]:
            k -= 1
        return k
                
    def do_Z(dataset,k):
        '''
        Z 명령을 시행한다. 복원.
        stack에 대해 복원한다. 커서는 바뀌지 않는다.
        Z_stack에는 짝수번-리스트 주소, 홀수번-인덱스 형식으로 저장되어 있다.
        이를 활용해서 해당 주소를 1로 변경한다.
        1이 증가하면 해당 주소의 데이터 총합이 1 증가하므로, 해당 부분에 대해 처리를 해 준다.(while문 참조)
        '''
        Z_var = Z_stack.pop()
        ind = 1
        N = len(Z_var)
        while ind < N-1:
            Z_var[ind][0] += 1
            ind+=1
        
        Z_var[ind-1][Z_var[-1]] = 1
        if Z_var[0] <= k:
            k+=1
        return k
    
    Ans_list = []
    def to_ox(dataset):
        '''
        최종 존재여부를 판단하기 위해 OX로 변환한다.
        데이터셋을 탐색하며 내부의 데이터셋으로 들어가고, 1이면 O, 0이면 X로 바꿔준다.
        '''
        if len(dataset) == 2:
            if dataset[1] == 0:
                Ans_list.append('X')
            else:
                Ans_list.append('O')
            
        else:
            if dataset[1] == 0:
                Ans_list.append('X')
                if dataset[2] == 0:
                    Ans_list.append('X')
                else:
                    Ans_list.append('O')
            elif dataset[1] == 1:
                Ans_list.append('O')
                if dataset[2] == 0:
                    Ans_list.append('X')
                else:
                    Ans_list.append('O')
            else:
                to_ox(dataset[1])
                to_ox(dataset[2])
    
    dataset = []
    makesub(dataset,n)
    ind = k
    for cd in cmd:
        if cd[0] == 'D':
            ind += int(cd[2:])
        elif cd[0] == 'U':
            ind -= int(cd[2:])
        elif cd[0] == 'C':
            ind = cmd_C(dataset,ind)
        else:
            ind = do_Z(dataset,ind)
    to_ox(dataset)
    
    
    answer = ''.join(Ans_list)
    return answer
