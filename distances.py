import string
from collections import deque

import numpy as np

import utils

import jaro

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
    def _sub(self, w1: list, w2: list, i, j):
        w2 = w2.copy()
        if w1[i] == w2[j]:
            return w1, w2, 0
        else:
            w2[j] = w1[i]
            return w1, w2, 1

    def _ins(self, w1: list, w2: list, i, j):
        w2 = w2.copy()
        w2.insert(j+1, w1[i])
        return w1, w2, 1

    def _del(self, w1: list, w2: list, i, j):
        w2 = w2.copy()
        w2.pop(j)
        return w1, w2, 1

    def solve(self, w1: list, w2: list, i: int, j: int):
        if i == -1:
            if j == -1:
                return 0
            else:
                t1, t2, c = self._del(w1, w2, i, j)
                return self.solve(t1, t2, i, j-1) + c
        else:
            if j == -1:
                t1, t2, c = self._ins(w1, w2, i, j)
                return self.solve(t1, t2, i-1, j) + c
            else:
                t1, t2, c = self._sub(w1, w2, i, j)
                i1 = self.solve(t1, t2, i-1, j-1) + c

                t1, t2, c = self._ins(w1, w2, i, j)
                i2 = self.solve(t1, t2, i-1, j) + c

                t1, t2, c = self._del(w1, w2, i, j)
                i3 = self.solve(t1, t2, i, j-1) + c
                return min(i1, i2, i3)

    def distance(self, w1, w2):
        w1 = list(w1)
        w2 = list(w2)
        return self.solve(w1, w2, len(w1) - 1, len(w2) - 1)


class SoundexDistance(Distance):
    def __init__(self, soundex_file=None, distance_fn=None, *args, **kwargs):
        super(SoundexDistance, self).__init__(*args, **kwargs)

        self.distance_fn = distance_fn
        self.soundex_dict = {}

        if soundex_file is None:
            self.char_to_int = {
                'B': '1',
                'F': '1',
                'P': '1',
                'V': '1',

                'C': '2',
                'G': '2',
                'J': '2',
                'K': '2',
                'Q': '2',
                'S': '2',
                'X': '2',
                'Z': '2',

                'D': '3',
                'T': '3',

                'L': '4',

                'M': '5',
                'N': '5',

                'R': '6'
            }
            self.bad_letters = 'AEIOUHWY'
            for word in self.glossary.keys():
                soundex_code = self.soundex(word)
                if soundex_code in self.soundex_dict:
                    self.soundex_dict[soundex_code].append(word)
                else:
                    self.soundex_dict[soundex_code] = [word]
            utils.save_obj('soundex.code', self.soundex_dict)
        else:
            self.soundex_dict = utils.load_obj(soundex_file)

    def soundex(self, word: str):
        w = word.upper()
        w = [i for i in w if i in string.ascii_uppercase]

        first_letter = w[:1]
        w = w[1:]
        w = [i for i in w if i not in self.bad_letters]

        tmp = []
        prev_i = -1
        for c in w:
            i = self.char_to_int[c]
            if prev_i != i:
                tmp.append(i)
                prev_i = i

        w = first_letter + tmp

        w = w[:4]
        w = ''.join(w)
        w = w.ljust(4, '0')
        return w

    def distance(self, w1, w2):
        code_1 = self.soundex(w1)
        code_2 = self.soundex(w2)

        if self.distance_fn is not None:
            return self.distance_fn(code_1, code_2)
        else:
            if code_1 != code_2:
                return 1
            else:
                return 0

    def propositions(self, w: str or list):
        if self.distance_fn is None:
            if isinstance(w, str):
                code = self.soundex(w)
                return self.soundex_dict[code]
            else:
                return {w0: self.soundex_dict[self.soundex(w0)][:self.max_proposition] for w0 in w}
        else:
            return super(SoundexDistance, self).propositions(w)


class JaroDistance(Distance):
    def __init__(self, winkler=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.winkler = winkler

    def distance(self, w1, w2):
        return 1 - (jaro.jaro_winkler_metric(w1, w2) if self.winkler else jaro.jaro_metric(w1, w2))
