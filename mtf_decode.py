def decode(string, a):

    alphabet = list(a)
    ans = []

    for i in xrange(len(string)):

        ch = string[i]
        ans.append(alphabet[ch])
        alphabet.pop(ch)
        alphabet.insert(0, ans[i])

    return ''.join(ans)