def Karp_Rabin(Text: str, Pattern: str, model: int) -> bool :
    if model == 1 :
        return simple_kp(Text, Pattern)
    
    else :
        pass


def simple_kp(Text: str, Pattern: str) -> bool :
    m = len(Pattern)
    n = len(Text)
    if n < m :
        return False
    ph = simple_hash(Pattern)
    th = simple_hash(Text[:m])
    for i in range(n - m + 1) :
        if ph == th :
            if Pattern == Text[i:i + m]:
                return True
        if i < n - m :   
            th = simple_update(Text, th, i, i + m - 1)

    return False

def simple_hash(s: str) -> int :
    r = 256
    q = 10 ** 9 + 7
    m = len(s)
    hash = 0
    for i in range(m) :
        hash = (hash * r + ord(s[i])) % q
    
    return hash

def simple_update(Text: str,hash: int,idx: int,lastidx: int) :
    q = 10 ** 9 + 7
    r = 256
    rm = (r ** (lastidx - idx)) % q
    hash = (hash - ord(Text[idx]) * rm) % q
    hash = (hash * r + ord(Text[lastidx + 1])) % q
    hash = (hash + q) % q
    return hash