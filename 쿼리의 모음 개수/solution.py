def get_dict(A,B):
    '''
    같은 숫자들이고 사이에 더 작은 수가 없는 집합에서의 참고할 사전 작성 함수.
    이 경우에는 입력 가능한 쿼리 중 조건을 여럿 만족하는 경우가 존재하기 때문에 따로 작성하였다.
    '''
    N = len(A)
    temp_dp = {}
    for i in range(N):
        a = A[i]
        b = B[i]
        new_var = a*b
        new_dp = {}
        for (x,y),v in temp_dp.items():
            before_y = y + a*B[x]
            new_dp[(x,before_y)] = new_dp.get((x,before_y),0) + v
            new_y = y + new_var
            new_dp[(i,new_y)] = new_dp.get((i,new_y),0) - v
            pass
        new_dp[(i,new_var)] = new_dp.get((i,new_var),0) - 1
        temp_dp = new_dp
    rt = {}
    for (x,y),v in temp_dp.items():
        rt[y] = rt.get(y,0) + v
    return rt

def seung(a,b,c):
    '''
    a ** b % c의 연산을 좀 더 빠르게 해 준다.
    그냥 생으로 하면 시간초과될거같아서 만들었다.
    '''
    dic ={}
    var = a
    t = 1
    dic[t] = var
    while t < b:
        t<<=1
        var *= var
        var %= c
        dic[t] = var
    rt = 1
    while t > 1:
        if t & b:
            rt *= dic[t]
            rt %= c
        t >>= 1
    if t & b:
        rt *= a
    return rt % c

class goodq:
    '''
    조건을 만족하는 쿼리들을 클래스화하였다.
    동일 숫자에 대해서 여러 개의 조건을 만족할 수도 있다.
    '''
    def __init__(self, var, inc):
        self.var = var
        self.inc = [inc]
        self.num = [1]
        self.done = False
    
    def add_inc(self):
        if self.done == True:
            "문제잇음"
        self.num[-1] += 1
    
    def dup_inc(self, inc_num):
        self.inc.append(inc_num)
        self.num.append(1)
            
    def __repr__(self):
        return (f'<{str(self.var)}, {str(self.inc)}, {str(self.num)}>')
            
def solution(q, a):
    answer = 0
    
    dic_possible = {}
    increase_num = {}
    possible_num = 0
    qnumdict = {}       # x : [goodqs,...]
    for n,x in enumerate(a):
        increase_num[x] = increase_num.get(x,0) + 1       # 지금의 쿼리를 기준으로 좌측으로 x보다 작았던 것들은 쿼리가 1씩 연장 가능하다.
        keys = list(increase_num.keys())                  
        for key in keys:
            if key > x:                                   # key가 더 큰 것들은 여기에서 더 뻗을 수 없는 경우이다.
                increase_num[x] += increase_num[key]      # 왼쪽으로는 그래도 이 수만큼 뻗을 수 있으므로 더해준다.
                del increase_num[key]                     # 더 이상 이 key에서는 뻗어나갈 수 없는 갇힌 모양새이므로 없애준다.
                qnumdict[key][-1].done = True             # 만들어둔 오브젝트가 더 확장을 못하도록 done를 참으로 바꾼다.
            elif key < x:                                 # key가 더 작은 것들이다. 계속 확장 가능하다.
                possible_num += key * increase_num[key]   # 모든 입력 가능한 쿼리수는 이렇게 증가한다.
                qnumdict[key][-1].add_inc()               # 가장 최신-즉 활성화된 절편 기준으로 add_inc를 통해서 해준다. key가 생성되는것이 우선이기 때문이다.
        possible_num += x * increase_num[x]
        
        try:
            if qnumdict[x][-1].done == False:                   # 최신 오브젝트가 있을 경우, 그것이 연장 가능하다면
                qnumdict[x][-1].dup_inc(increase_num[x])
            else:                                               # 오브젝트를 추가해야 하는경우
                gen_obj = goodq(x, increase_num[x])
                qnumdict[x].append(gen_obj)
        except:                                                 # 해당 키에 오브젝트가 들어간 적이 없을 경우
            qnumdict[x] = [goodq(x,increase_num[x])]
                
    # 유용한 쿼리에 대해 qnumdict로 작성을 완료했다.
    # qnumdict[x]로 x값을 만족시키는 쿼리에 대한 정보를 불러온다.(리스트)
    # qnumdict[x][i]는 x의 i번째 체인으로 체인 내부에서는 동시만족쿼리가 존재한다.
    # 동시만족 쿼리가 존재하나 셋 이상은 언제나 중간에 존재하는게 존재(2차원적이므로)
    # 체인의 각 원소는 goodq라는 클래스로 정의해 두었으며, num은 만족하는 쿼리 수, dupnum은 리스트 다음 조건도 만족하는 쿼리 수이다.
    
    dp = {}     # 만들 사전.
    for x in qnumdict.keys():
        for chain in qnumdict[x]:                         # 이 절편을 기준으로 사전을 업데이트한다.
            if len(chain.num) > 0:  
                temp_dp = get_dict(chain.num, chain.inc)  # 절편만 조합할 때의 경우의 수 사전
            else:
                continue
            new_dp = {}
            
            
            for temp_key, temp_val in temp_dp.items():                    
                new_dp[temp_key] = new_dp.get(temp_key,0) + temp_val  # 신규 사전값 업데이트. 먼저 온 이유는 이것이 없는 경우 위에서 continue로 빠지니까.
                for org_key, org_val in dp.items():                   # 사전을 이중탐색하며 업데이트
                    gen_key = temp_key + org_key
                    gen_val = temp_val * org_val
                    new_dp[gen_key] = new_dp.get(gen_key,0) + gen_val
            
            for org_key, org_val in dp.items():                       #기존 사전값도 업데이트
                new_dp[org_key] = new_dp.get(org_key,0) + org_val
            
            for key in set(new_dp.keys()):
                if new_dp[key] == 0:
                    del new_dp[key]         #없는 키를 정리해서 시간을 아낀다.
            dp = new_dp

    mod_val = 998244353
    answer = seung(possible_num,q,mod_val)

    for key,val in dp.items():
        delta = val * (seung(possible_num - key, q, mod_val))
        answer += delta
    
    return answer % mod_val
