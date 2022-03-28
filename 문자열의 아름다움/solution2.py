def get_num(k, i,  iternum):
    # SUM<(k-ai)**2 - (k-ai)> = k**2 - 2kai + a**2 * i**2 - k + ai for i = 0,...,n-1. iternum = n
    #                       = k**2 - k + a^2 i**2 + a * i(1 - 2k)
    var = (k**2 - k) * iternum
    var += (1 - 2 * k) * (iternum * (iternum-1) // 2) * i
    var += iternum * (iternum - 1) * (2* iternum - 1) // 6 * i * i
    return var // 2       # 나누기 2는 기본으로 했어야 했던 것.

def solutionb(s):
    N = len(s)
    # answer = SUM<N * (N+1) // 2> for N = 1~N
    answer = ((N * (N-1) * (2*N - 1))//6 + N * (N-1) // 2)//2
    dic = {}
    before_chr = s[0]
    chr_num = 1
    ct_chr = {}
    ct_conti = {}
    for i in range(1,N):
        now_chr = s[i]
        if before_chr == now_chr:
            chr_num += 1
        else:
            try:
                dic[before_chr][chr_num] = dic[before_chr].get(chr_num,0) + 1
            except:
                dic[before_chr] = {chr_num : 1}
            ct_chr[before_chr] = ct_chr.get(before_chr,0) + chr_num
            ct_conti[before_chr] = ct_conti.get(before_chr,0) + 1
            chr_num = 1
            before_chr = now_chr
    try:
        dic[before_chr][chr_num] = dic[before_chr].get(chr_num,0) + 1
    except:
        dic[before_chr] = {chr_num : 1}
    ct_chr[before_chr] = ct_chr.get(before_chr,0) + chr_num
    ct_conti[before_chr] = ct_conti.get(before_chr,0) + 1
    
    for c, chr_num in ct_chr.items():
        conti_ctnum = ct_conti[c]
        keys = list(dic[c].keys())
        keys.sort()
        var = 0
        before_key = 0
        for chr_conti in keys:
            conti_num = dic[c][chr_conti]
            deltakey = chr_conti - before_key
            before_key = chr_conti
            # SUM<(k-i)**2 - (k-i) = k**2 - 2ki + i**2 - k + i> for i = 0,...,?
            var += get_num(chr_num,conti_ctnum ,deltakey)            
            chr_num -= conti_ctnum * deltakey
            conti_ctnum -=  conti_num
        answer -= var
    return answer
