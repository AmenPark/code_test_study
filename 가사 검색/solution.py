import sys
sys.setrecursionlimit(100000)

def solution(words, queries):
    answer = []
    dic = {}
    def input_dic_front(dic, wd,i):           # 앞 글자부터 사전 작성.
        dic[wd[i]] = dic.get(wd[i],{0:0})     # dic은 키가 0일때는 사전 항목 수이며, 키가 문자일 경우는 다음 글자가 해당 문자인 것들의 사전을 가져온다.
        dic[wd[i]][0] += 1
        if i != len(wd) - 1:
            d = dic[wd[i]]
            input_dic_front(d,wd,i+1)
    
    def input_dic_back(dic,wd,i):             # 뒷 글자부터 사전 작성
        dic[wd[i]] = dic.get(wd[i],{0:0})     
        dic[wd[i]][0] += 1                    # dic은 키가 0일때는 사전 항목 수이며, 키가 문자일 경우는 다음 글자가 해당 문자인 것들의 사전을 가져온다.
        if i != 1:
            d = dic[wd[i]]
            input_dic_back(d,wd,i-1)
    
    def input_dic(dic,wd):                    # 사전 작성.
        l = len(wd)
        try:
            dic[l][0] +=1
        except:
            dic[l] = {0:1}
            dic[l][1] = {}
            dic[l][-1] = {}
        input_dic_front(dic[l][1],wd,0)
        input_dic_back(dic[l][-1],wd,l-1)
    
    def get_back(dic,q,i):                    # 사전 검색-뒤부터
        if q[i-1] != '?':   
            return get_back(dic[q[i]],q,i-1)
        else:
            return dic[q[i]][0]
        
    def get_front(dic,q,i):                   # 사전 검색-앞부터
        if q[i+1] != '?':
            return get_front(dic[q[i]],q,i+1)
        else:
            return dic[q[i]][0]
        
    def get_num(dic,q):
        try:
            l = len(q)
            if q[0] == '?':       
                if q[-1] == '?':        # 뒤가 ?일 경우엔 0번부터.
                    return dic[l][0]
                else:
                    return get_back(dic[l][-1],q,l-1)
            else:                       # 0번이 ?가 아니라면 앞부터 탐색.
                return get_front(dic[l][1],q,0)
        except:
            return 0
    
    for wd in words:
        input_dic(dic,wd)
        
    for q in queries:
        answer.append(get_num(dic,q))
        
    
    return answer
