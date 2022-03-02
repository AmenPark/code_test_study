def get_num(char,n,nowl,minuschecker,countvar, segnum):
    '''
    동일 문자열로 시작하고 끝나는 경우를 계산한다.
    '''
    ori_len = n - nowl
    if ori_len < 0:
        return 0
    # 아래 세 식은 수학식을 통해 계산한 문자열의 아름다움이다.
    rt = (((n * (n+1) * (2*n+1)) // 6) + (n*(n+1)//2))//2
    rt -= (((ori_len * (ori_len+1) * (2*ori_len+1)) // 6) + (ori_len*(ori_len+1)//2))//2
    rt -= (((nowl * (nowl-1) * (2*nowl - 1)) // 6) + (nowl * (nowl - 1) // 2)) // 2
    if minuschecker.get(char,None) != None:
        keys = list(minuschecker[char])
        keys.sort()
        minusvar = 0
        beforekey = 0
        breakcheker = False

        for key in keys:
            diff = key - beforekey          # 항수
            if diff > nowl:
                diff = nowl
                breakcheker = True
            minusvar += (diff * countvar * nowl) - (((diff * (diff-1))//2) * (countvar + segnum * nowl)) + (((diff * (diff-1) * (2*diff-1))//6) * segnum)

            countvar -= segnum * diff
            segnum -= minuschecker[char][key]
            nowl -= diff
            if breakcheker:
                break
            beforekey = key
        rt -= minusvar
    return rt

def solution(s):
    if len(s) == 1:
        return 0
    answer = 0
    minuschecker = {}
    beforechar = s[0]
    lenth = 1
    countdict = {}
    segdict = {}
    # 동일문자열로 연속되는 경우 해당 연속구간을 기록해둔다. 모든 문자가 다 다르다면 n(n-1)/2 꼴이 답이며 동일 문자가 나오면 그에 따라 값이 감소한다.
    for n in range(1,len(s)):
        char = s[n]
        if char == beforechar:
            lenth += 1
        else:
            answer += get_num(beforechar,n-1,lenth,minuschecker,countdict.get(beforechar,0), segdict.get(beforechar,0))
            countdict[beforechar] = countdict.get(beforechar,0)+lenth
            segdict[beforechar] = segdict.get(beforechar,0) + 1
            try:
                minuschecker[beforechar][lenth] = minuschecker[beforechar].get(lenth,0)+1
            except:
                minuschecker[beforechar] = {lenth : 1}
            beforechar = char
            lenth = 1
    answer += get_num(char,n,lenth,minuschecker,countdict.get(char,0), segdict.get(beforechar,0))

    return answer
