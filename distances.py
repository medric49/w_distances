import numpy as np
from collections import deque


class Distance:
    def __init__(self, glossary: dict = None, max_proposition=5, select_fn=1):
        self.glossary = glossary
        self.max_proposition = max_proposition
        self.select_fn = select_fn

    def __call__(self, w1, w2):
        return self.distance(w1, w2)

    def distance(self, w1, w2):
        raise NotImplementedError()

    def _select_0(self, w):
        props = deque([], maxlen=self.max_proposition)
        min_dist = np.inf
        for word in self.glossary.keys():
            dist = self.distance(w, word)
            if dist <= min_dist:
                props.appendleft(word)
                min_dist = dist
        return list(props)

    def _select_1(self, w):
        props = deque([], maxlen=self.max_proposition)
        dists = deque([], maxlen=self.max_proposition)

        for word in self.glossary.keys():
            dist = self.distance(w, word)
            min_dist = np.inf if len(dists) == 0 else dists[0]
            if dist <= min_dist:
                props.appendleft(word)
                dists.appendleft(dist)
            elif dist <= np.mean(dists):
                if len(props) == props.maxlen:
                    props.pop()
                    dists.pop()
                props.insert(1, word)
                dists.insert(1, dist)
        return list(props)

    def _select_2(self, w):
        props = {}
        chosen_props = []
        for word in self.glossary.keys():
            dist = self.distance(w, word)
            props[word] = dist

        for i in range(self.max_proposition):
            word = list(props.keys())[np.argmin(list(props.values()))]
            chosen_props.append(word)
            props.pop(word)
        return chosen_props

    def select(self, w):
        if self.select_fn == 0:
            return self._select_0(w)
        elif self.select_fn == 1:
            return self._select_1(w)
        elif self.select_fn == 2:
            return self._select_2(w)

    def propositions(self, w: str or list):
        if isinstance(w, str):
            if w in self.glossary:
                return [w]
            else:
                return self.select(w)
        elif isinstance(w, list):
            return {w0: self.propositions(w0) for w0 in w}


class NullDistance(Distance):
    def distance(self, w1, w2):
        return 0


class HammingDistance(Distance):
    def distance(self, w1, w2):
        min_length = min(len(w1), len(w2))
        diff = 0
        for i in range(min_length):
            if w1[i] != w2[i]:
                diff += 1
        diff += abs(len(w1) - len(w2))
        return diff


class JaccardDistance(Distance):
    def __init__(self, nb_char=2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nb_char = nb_char

    def _separate(self, word) -> set:
        w = set()
        for i in range(len(word)-self.nb_char+1):
            w.add(word[i:i+self.nb_char])
        return w

    def distance(self, w1, w2):
        w1 = self._separate(w1)
        w2 = self._separate(w2)

        union = w1.union(w2)
        intersection = w1.intersection(w2)
        jaccard_index = len(intersection)/len(union)

        return 1 - jaccard_index


class LevenshteinDistance(Distance):
    def _sub(self, w1: str, w2: str):
        if w1[-1] == w2[-1]:
            return w1, w2, 0
        w2 = w2[:-1] + w1[-1:]
        return w1, w2, 1

    def _ins(self, w1: str, w2: str):
        w2 = w2 + w1[-1:]
        return w1, w2, 1

    def _del(self, w1: str, w2: str):
        w2 = w2[:-1]
        return w1, w2, 1

    def distance(self, w1, w2, i=None, j=None):
        if i is None:
            i = len(w1) - 1
        if j is None:
            j = len(w2) - 1

        if w1 == w2:
            return 0

        if i == 0:
            if j == 0:
                return 0
            else:
                t1, t2, c = self._del(w1, w2)
                return self.distance(t1, t2, i, j-1) + c
        else:
            if j == 0:
                t1, t2, c = self._ins(w1, w2)

                return self.distance(t1, t2, i-1, j) + c
            else:
                t1, t2, c = self._sub(w1, w2)
                i1 = self.distance(t1, t2, i-1, j-1) + c

                t1, t2, c = self._ins(w1, w2)
                i2 = self.distance(t1, t2, i-1, j) + c

                t1, t2, c = self._del(w1, w2)
                i3 = self.distance(t1, t2, i, j-1) + c
                return min(i1, i2, i3)
