import random
class nd:
    __slots__ = ['conn', 'anc', 'var', 'num', 'w']

    def __init__(self, var, num):
        self.conn = []
        self.anc = None
        self.var = var  # 값
        self.num = num  # 번호
        self.w = 1

    def set_chain(self, nd2posdic, anc=None):
        self.anc = anc
        chains = []
        max_chain = None
        chain_w = 0
        for nd in self.conn:
            if nd != self.anc:
                w, chain = nd.set_chain(nd2posdic, self)
                chains.append(chain)
                if w > chain_w:
                    chain_w = w
                    max_chain = chain
        if max_chain == None:
            new_nd = treap_nd(self.var, self.num)
            new_chain = treap(new_nd)
            nd2posdic[self.num] = new_chain
            return 1, new_chain
        else:
            max_chain.seg.append(0)
            for chain in chains:
                if chain == max_chain:
                    continue
                chain.anc = max_chain
                chain.anc_pos = max_chain.w
                max_chain.seg[chain.anc_pos] += chain.sum
                max_chain.sum += chain.sum
            new_nd = treap_nd(self.var, self.num)
            max_chain.push_new(new_nd)
            nd2posdic[self.num] = max_chain
            return max_chain.w, max_chain


class treap_nd:
    __slots__ = ['var', 'ran', 'sum', 'w', 'anc', 'left', 'right', 'num']

    def __init__(self, var, num):
        self.var = var
        self.ran = random.random()
        self.sum = var
        self.w = 1
        self.anc = None
        self.left = None
        self.right = None
        self.num = num

    def printf(self, tnum=0):
        taps = '   ' * tnum
        print(f'{taps}값:{self.var}, 합:{self.sum}, W: {self.w}, 부모:{None if self.anc == None else self.anc.var}')
        print(taps + "LLLLLLLLLLLLLLLL")
        if self.left:
            self.left.printf(tnum + 1)
        else:
            print(taps + "left NONE")
        print(taps + "RRRRRRRRRRRRRRRR")
        if self.right:
            self.right.printf(tnum + 1)
        else:
            print(taps + "right NONE")


class treap:
    __slots__ = ['num2pos', 'root', 'seg', 'anc', 'anc_pos', 'sum', 'w']

    def __init__(self, nd: treap_nd):
        self.root = nd
        self.sum = nd.sum
        self.num2pos = {nd.num: 0}
        self.seg = [0]
        self.anc = None
        self.anc_pos = None
        self.w = 1

    def push_new(self, nd):
        self.num2pos[nd.num] = 1
        self.push(nd)
        self.w += 1

    def push(self, nd: treap_nd):
        self.sum += nd.var
        if nd.ran > self.root.ran:
            nd.left = self.root
            nd.sum += self.root.sum
            nd.w += self.root.w
            self.root.anc = nd
            self.root = nd
        else:
            now_nd = self.root
            while (True):
                now_nd.w += 1
                now_nd.sum += nd.sum
                if now_nd.right:
                    if now_nd.right.ran > nd.ran:
                        now_nd = now_nd.right
                    else:
                        nd.left = now_nd.right
                        nd.left.anc = nd
                        nd.sum += nd.left.sum
                        nd.w += nd.left.w
                        nd.anc = now_nd
                        now_nd.right = nd
                        break
                else:
                    now_nd.right = nd
                    nd.anc = now_nd
                    break

    def getsum(self, pos):
        nd = self.root
        rt = nd.sum
        while True:
            if nd.w == pos:
                return rt
            else:
                if nd.left:
                    if nd.left.w >= pos:
                        rt -= nd.sum
                        nd = nd.left
                        rt += nd.sum
                        continue
                    else:
                        pos -= nd.left.w
                        if pos == 1:
                            rt -= nd.right.sum
                            return rt
                        else:
                            pos -= 1
                            nd = nd.right
                else:
                    nd = nd.right
                    pos -= 1

    def find_nd(self, pos):
        check = pos - 1
        nd = self.root
        while True:
            if self.left:
                left_var = self.left.w
            else:
                left_var = 0
            if left_var <= check:
                if left_var == check:
                    return nd
                nd = nd.right
                check -= left_var + 1
            else:
                nd = nd.left

    def delete(self, nd):
        self.sum -= nd.var
        anc = nd.anc
        while (anc != None):
            anc.w -= 1
            anc.sum -= nd.var
            anc = anc.anc
        anc = nd.anc
        if nd.left:
            left_ran = nd.left.ran
        else:
            left_ran = -1
        if nd.right:
            right_ran = nd.right.ran
        else:
            right_ran = -1
        try:
            if anc.right is nd:
                isleft = False
            else:
                isleft = True
        except:
            pass

        if left_ran > right_ran:
            next_nd = nd.left
            another_nd = nd.right
            left_up = True
        else:
            next_nd = nd.right
            another_nd = nd.left
            left_up = False
            if right_ran == -1:
                if isleft:
                    anc.left = None
                else:
                    anc.right = None
                return 0
        if anc:
            if isleft:
                anc.left = next_nd
            else:
                anc.right = next_nd
        else:
            self.root = next_nd
        next_nd.anc = anc
        if another_nd:
            next_nd.w += another_nd.w
            next_nd.sum += another_nd.sum
        else:
            return 0
        anc = next_nd
        if left_up:
            comp_small = next_nd.right
            comp_large = another_nd
        else:
            comp_large = next_nd.left
            comp_small = another_nd

        while (True):
            if comp_small:
                left_ran = comp_small.ran
            else:
                left_ran = -1
            if comp_large:
                right_ran = comp_large.ran
            else:
                right_ran = -1

            if left_ran >= right_ran:
                if left_ran == -1:
                    return None
                else:
                    next_nd = comp_small
                    another_nd = comp_large
                    small_up = True
            else:
                next_nd = comp_large
                another_nd = comp_small
                small_up = False
            next_nd.anc = anc
            if left_up:
                anc.right = next_nd
            else:
                anc.left = next_nd

            if another_nd:
                next_nd.sum += another_nd.sum
                next_nd.w = another_nd.w
            else:
                break

            if small_up:
                comp_large = another_nd
                comp_small = next_nd.right
                left_up = True
            else:
                comp_small = another_nd
                comp_large = next_nd.left
                left_up = False  # 오른쪽이 최초 올라간다면?
            anc = next_nd

    def printf(self):
        # print(self.sum)
        self.root.printf()


def make_fenwick(datalist):
    L = len(datalist)
    w = L & (-L)
    L -= 1
    p = 1
    w -= 1
    while p <= w:
        # print(p,w)
        datalist[-1] += datalist[L - p]
        p <<= 1


def get_fenwick(datalist, pos):
    pos += 1
    rt = datalist[pos - 1]
    while pos:
        w = pos & (-pos)
        pos -= w
        if pos == 0:
            break
        rt += datalist[pos - 1]
    return rt


def add_fenwick(datalist, pos, delta):
    pos += 1
    while True:
        try:
            datalist[pos - 1] += delta
            w = pos & (-pos)
            pos += w
        except:
            break
