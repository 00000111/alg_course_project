import BWT_forward


def reverse_BWT(string):

    a = BWT_forward.alphbt(string)
    k = [0]* len(a)  # an array to store number of occurrences of each symbol
    m = {}  # a dict to store the starting pos of each symbol in the first column
    length = len(string)
    c = [0] * length  # an array to store ranks of each symbol
    start = 0

    for i in xrange(length):

        if string[i] == '$':
            start = i

        c[i] = k[a.index(string[i])]
        k[a.index(string[i])] += 1

    count = 0
    for i in xrange(len(a)):
        m[a[i]] = count
        count += k[i]

    q = [0] * len(string)

    for j in xrange(len(string) - 1, -1, -1):
        q[j] = string[start]
        start = c[start] + m[string[start]]

    return ''.join(q)


if __name__ == '__main__':
    print reverse_BWT('annb$aa')
    print reverse_BWT('w$wwdd__nnoooaattTmmmrrrrrrooo__ooo')



