import re
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

