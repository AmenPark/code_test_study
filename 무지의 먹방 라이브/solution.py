def solution(food_times, k):
    answer = 0
    foodnum = {} 
    foodsum = 0   
    N = 0
    for i in food_times:
        if i>0:
            foodnum[i] = foodnum.get(i,0) + 1 #음식이 i개인 접시의 갯수를 표시
            foodsum += i                      #음식의 총 수
            N += 1                            #그릇의 총 수
    if foodsum <= k:                          #음식을 다 먹었을 경우
        return -1
    foodmin = 1
    foods = list(foodnum.keys())
    foods.sort()
    var = 0
    for f in foods:                           # 그릇의 수만큼이 한 바퀴가 되며 k번째 작은 그릇과 k+1번째 작은 그릇의 음식 차이 만큼 변동 없음.
        if k//N >= (f - var):                 # 주어진 번호가 충분히 음식을 먹어 그릇을 추가로 비워내는가 체크
            k -= (f-var) * N                  # 그릇이 비워지는 사이클까지를 빼줌
            N -= foodnum[f]                   # 몇 그릇이 비워지는지 빼줌
            var = f
        else:
            k %= N
            break
            
    
    for n,foo in enumerate(food_times):     # 이후 남은 숫자만큼 반복하며 해당 바퀴수 기준 음식이 남아있는 그릇만 체크하면 
        if foo >= f:
            if k == 0:
                return n+1
            k-=1
