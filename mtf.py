def encode(string, alphabet):
    n = len(alphabet)
    occ = {}  # dict w frequencies of every letter's occurrence
    s = float(len(string))
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

    return ans, alphabet, occ