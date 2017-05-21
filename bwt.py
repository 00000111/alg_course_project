def alphbt(string):
    return sorted(set(string))


def suffix_sort(string):

    string = ''.join((string, '$'))
    n = len(string)
    count = [0] * 128
    # count = [0] * ord('z')  # array cor counting the number of appearances of each symbol in string
    positions = [0] * n  # holds the current positions of suffices in the suffix array
    classes = [0] * n  # holds the classes of equivalence each suffix belongs to
    alphabet = alphbt(string)  # holds alphabet, needed for array c = compact representation of F column
    c = []

    # count the number of times each symbol appears in a string
    for i in xrange(n):
        count[ord(string[i])] += 1

    # modify the array so that each index i contains the order of ith element in the array
    for i in xrange(1, ord('z')):
        count[i] += count[i - 1]

    # construct array c: for each letter ltr, add the the number of symbols smaller than ltr in the string
    for ltr in alphabet:
        c.append(count[ord(ltr) - 1])

    # construct dictionary c: for each letter ltr, add the the number of symbols smaller than ltr in the string
    # for ltr in alphabet:
    #     c[ltr] = count[ord(ltr) - 1]

    # sort the positions array according to count
    for i in xrange(n - 1, -1, -1):
        idx = count[ord(string[i])]  # check how many elements are in the sorted array before teh i-th element
        positions[idx - 1] = i  # place the ith element in pos = idx - 1 (because zero indexing lol)
        count[ord(string[i])] -= 1  # decrease the number of elements in idx

    # construct classes of equivalence based on the first element of each suffix
    cl = 0
    for i in range(1, n):
        # if the compared symbols are different
        if string[positions[i]] != string[positions[i - 1]]:
            # increase the number of class of equivalence
            cl += 1
        # assign the numbers of class ner prefix
        classes[positions[i]] = cl
    prefix_len = 1  # the sorted suffixes are lf len = 2 * prefix_len on every iteration
    while prefix_len <= n:
        aux_positions = [0] * n  # holds the positions second digits of ranking pairs
        aux_classes = [0] * n  # holds the classes of equivalence for current step
        count = [0] * (cl + 1)

        #  sorting ranking pairs by second digit
        for i in xrange(n):
            #  positions of second digits of ranking pairs are determined by
            # their previous position - number of rows they're shifted up, i.e. previous position - prefix_len
            aux_positions[i] = (positions[i] + n - prefix_len) % n

        # sort ranking pairs by the first digit: count the number of items in each class
        for i in xrange(n):
            count[classes[aux_positions[i]]] += 1

        for i in xrange(1, cl + 1):
            count[i] += count[i - 1]

        # move positions of elements according to their class
        for i in xrange(n - 1, -1, -1):
            positions[count[classes[aux_positions[i]]] - 1] = aux_positions[i]
            count[classes[aux_positions[i]]] -= 1

        cl = 0
        for i in range(1, n):
            first_median = (positions[i] + prefix_len) % n  # middle of the first interval compared
            second_median = (positions[i - 1] + prefix_len) % n  # middle of the second interval compared
            # if the values in the beginning or in the middle of the interval are not the same ->
            # suffixes are not the same
            if (classes[positions[i]] != classes[positions[i - 1]]) or \
                    (classes[first_median] != classes[second_median]):
                # -> increase equivalence class number
                cl += 1
            aux_classes[positions[i]] = cl

        # move info from auxiliary array to the main one
        for i in xrange(n):
            classes[i] = aux_classes[i]

        # each step the prefix length is doubled
        prefix_len *= 2

    return positions, c


def bwt(string):

    suff_arr = suffix_sort(string)[0]
    bw = []

    for i in suff_arr:
        if i == 0:
            bw.append('$')
        else:
            bw.append(string[i - 1])

    return ''.join(bw)


if __name__ == '__main__':
    s = 'abacabadabacabaeabacabadabacabafabacabadabacabaeabacabadabacabagabacabadabacabaeabacabadabacabafabacabadabacab' \
    'aeabacabadabacabahabacabadabacabaeabacabadabacabafabacabadabacabaeabacabadabacabagabacabadabacabaeabacabadabacabaf' \
    'abacabadabacabaeabacabadabacabaiabacabadabacabaeabacabadabacabafabacabadabacabaeabacabadabacabagabacabadabacaba' \
    'eabacabadabacabafabacabadabacabaeabacabadabacabahabacabadabacabaeabacabadabacabafabacabadabacabaeabacabadabacab' \
    'agabacabadabacabaeabacabadabacabafabacabadabacabaeabacabadabacabajabacabadabacabaeabacabadabacabafabacabadabacab' \
    'aeabacabadabacabagabacabadabacabaeabacabadabacabafabacabadabacabaeabacabadabacabahabacabadabacabaeabacabadabacab' \
    'afabacabadabacabaeabacabadabacabagabacabadabacabaeabacabadabacabafabacabadabacabaeabacabadabacabaia'

    DICT = ['$'] + alphbt(s)
    
    s1 = bwt(s)
    print s1
