def solution(arr):
    answer = -1
    maxdic = {}
    maxdic[0] = int(arr[0])     # 괄호 몇개 열렸는지-> 그 때의 최댓값.
    opennum = 0                 # 열린 괄호수
    N = len(arr)
    i = 1
    while i < N-1:              # 반복문 내에서는 연산을 추가하며 괄호-최댓값의 사전을 업데이트한다. +(...)꼴의 괄호는 영향 없으므로 -에만 괄호가 열린다고 생각한다.
        value = int(arr[i+1])   # 모든 괄호를 다 풀어 +/- 반전만 있다고 생각한다면 괄호를 닫는 것과 여는 것은 열린 괄호수의 홀짝을 변화시켜 +/- 반전에 기여한다는 점에서 동등하다.
        nmaxdic = {}            # 따라서 -의 경우에도 괄호를 닫는 것이 가능하나 사실상 여는 것과 똑같기에 더 유연한 괄호를 여는 것으로 대체한다.
        if arr[i] == '+':
            for j in range(opennum + 1):
                if j == 0:
                    nmaxdic[0] = maxdic[0]+value
                else:
                    if j%2 == 0:                                   # 열린 괄호는 다 -뒤에 열리므로 열린 괄호수의 홀짝에 따라 전체적인 +-반전이 이루어진다.
                        nmaxdic[j-1] = max(nmaxdic[j-1],maxdic[j]-value)
                        nmaxdic[j] = maxdic[j] + value
                    else:
                        nmaxdic[j-1] = max(nmaxdic[j-1],maxdic[j]+value)
                        nmaxdic[j] = maxdic[j] - value
        else:
            for j in range(opennum + 1):
                if j == 0:
                    nmaxdic[0] = maxdic[0] - value
                    nmaxdic[1] = maxdic[0] - value
                else:
                    if j%2 == 1:                                    # 열린 괄호는 다 -뒤에 열리므로 열린 괄호수의 홀짝에 따라 전체적인 +-반전이 이루어진다.
                        nmaxdic[j] = max(nmaxdic[j],maxdic[j] - value)
                        nmaxdic[j+1] = maxdic[j] + value
                    else:
                        nmaxdic[j] = max(nmaxdic[j], maxdic[j] + value)
                        nmaxdic[j+1] = maxdic[j] - value
            opennum += 1
        maxdic = nmaxdic
        i+=2
    
    answer = maxdic[0]                                            # 안 닫힌 괄호는 나중에 몰아서 닫으면 된다.
    for n in range(opennum+1):
        if answer < maxdic[n]:
            answer = maxdic[n]

    
    return answer
