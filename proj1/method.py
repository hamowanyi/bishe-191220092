import re
import string
'''
def get_lcp(sa, text):
    n = len(text)
    rank = [0] * n
    lcp = [0] * n

    for i in range(n):
        rank[sa[i]] = i

    k = 0
    for i in range(n):
        if rank[i] == n - 1:
            k = 0
            continue
        j = sa[rank[i] + 1]
        while i + k < n and j + k < n and text[i + k] == text[j + k]:
            k += 1
        lcp[rank[i]] = k
        if k > 0:
            k -= 1

    return lcp
def get_sa_lcp(text):
    n = len(text)
    sa = sorted(range(n), key=lambda i: text[i:])
    lcp = get_lcp(sa, text)

    return sa, lcp
def get_repeat_substring(text):
    sa, lcp = get_sa_lcp(text)
    max_len, max_idx = max((lcp[i], i) for i in range(len(lcp)))
    return text[sa[max_idx]:sa[max_idx] + max_len]
def dedup(text):
    text=text[::-1]
    pretext = text
    text = get_repeat_substring(text)
    while text.find(' ')!=-1:
        pretext = text
        text = get_repeat_substring(text)
    pretext=pretext[::-1]
    return pretext

def string_split(str):
    return re.split("[,*#'./\"\n(){}+-=_@!><&]",str)
'''

class Methodtest():
    def all_block(self, str, c=' '):
        if len(str) >= 2:
            str = str[1:len(str)]
        else:
            return True
        for i in range(len(str)):
            if str[i] != c:
                return False
        return True

    def find_all(self, string, sub, beg=0, end=0):
        if end == 0:
            end = len(string)
        string = string[beg:end]
        start = 0
        pos = []
        while True:
            start = string.find(sub, start)
            if start == -1:
                return pos
            pos.append(start)
            start += len(sub)

    def string_split(self, str):
        return re.split("[,:;*#'./\"\n(){}+-=_@!><&]", str)

    def get_first_char(self, str):
        for i in range(len(str)):
            if str[i] != ' ':
                if str[i] in string.ascii_uppercase:
                    return True, False
                elif str[i] in string.ascii_lowercase:
                    return False, True
        return False, False

    def judge_end(self, str, i):
        if i < len(str) - 1:
            if str[i + 1] in string.ascii_lowercase:
                return False
            else:
                return True
        else:
            return True

    def check_useful(self, str):
        text = ''':;*#'/\"\n(){}-!><&'''
        for c in text:
            if c in str:
                return False
        return True

    def ref_preprocess(self, ref):
        sList = ref.split('\n')
        res = ''
        if len(sList) > 1:
            i0 = 0
            while i0 < len(sList):
                if not self.check_useful(sList[i0]):
                    print(1)
                    i0 = i0 + 1
                    continue
                if len(sList[i0]) == 0:
                    print(2)
                    i0 = i0 + 1
                    continue
                is_upper, is_lower = self.get_first_char(sList[i0])
                if is_lower and not is_upper:
                    print(3)
                    i1 = sList[i0].find('.')
                    if i1 != -1 and self.judge_end(sList[i0], i1):
                        print(4)
                        res = res + sList[i0][:i1 + 1]
                        break
                    else:
                        print(5)
                        res = res + sList[i0]
                    i0 = i0 + 1
                elif is_upper and not is_lower:
                    print(6)
                    if len(res) > 0:
                        print(7)
                        break
                    else:
                        print(8)
                        i2 = sList[i0].find('.')
                        if i2 == -1:
                            res = res + sList[i0]
                        else:
                            if self.judge_end(sList[i0], i2):
                                res = res + sList[i0][:i2 + 1]
                                break
                        i0 = i0 + 1
                else:
                    i0 = i0 + 1
                    continue

        if len(res) == 0:
            return ref
        # clear blocks
        i2 = 0
        while i2 < len(res):
            if res[i2] != ' ':
                break
            else:
                i2 = i2 + 1
        res = res[i2:]
        return res


sum_symbol = '''Iterate over an Array or an Object invoking a function for each item.

If `obj` is an Array callback will be called passing
the value, index, and complete array for each item.

If 'obj' is an Object callback will be called passing
the value, key, and complete object for each property.

@param {Object|Array} obj The object to iterate
@param {Function} fn The callback to invoke for each item'''
print(Methodtest().ref_preprocess(sum_symbol))