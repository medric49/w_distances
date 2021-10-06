def separate(word) -> set:
    w = set()
    n = 2
    for i in range(len(word) - n + 1):
        w.add(word[i:i+n])
    return w


def distance(w1, w2):
    w1 = separate(w1)
    w2 = separate(w2)

    union = w1.union(w2)
    intersection = w1.intersection(w2)
    jaccard_index = len(intersection)/len(union)

    return 1 - jaccard_index

if __name__ == '__main__':
    print(distance('aaa', 'aaabd'))
