def encode(string, a):

    alphabet = list(a)
    occ = {}  # dict w frequencies of every letter's occurrence
    ans = []

    for ltr in string:

        i = alphabet.index(ltr)
        if i in occ:
            occ[i] += 1
        else:
            occ[i] = 1


        ans.append(i)
        alphabet.pop(i)
        alphabet.insert(0, ltr)

    return ans, occ


def decode(string, a):

    alphabet = list(a)
    ans = []

    for i in xrange(len(string)):

        ch = string[i]
        ans.append(alphabet[ch])
        alphabet.pop(ch)
        alphabet.insert(0, ans[i])

    return ''.join(ans)