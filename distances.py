import numpy as np
from collections import deque


class Distance:
    def __init__(self, glossary: dict, max_proposition):
        self.glossary = glossary
        self.max_proposition = max_proposition
        pass

    def distance(self, w1, w2):
        raise NotImplementedError()

    def _select_1(self, w):
        props = deque([], maxlen=self.max_proposition)
        min_dist = np.inf
        for word in self.glossary.keys():
            dist = self.distance(w, word)
            if dist <= min_dist:
                props.appendleft(word)
        return list(props)

    def _select_2(self, w):
        props = deque([], maxlen=self.max_proposition)
        dists = deque([], maxlen=self.max_proposition)

        for word in self.glossary.keys():
            dist = self.distance(w, word)
            min_dist = np.inf if len(dists) == 0 else dists[0]
            if dist <= min_dist:
                props.appendleft(word)
                dists.appendleft(dist)
            elif dist <= np.mean(dists):
                props.insert(1, word)
                dists.insert(1, dist)
        return list(props)

    def _select_3(self, w):
        props = {}
        chosen_props = []
        for word in self.glossary.keys():
            dist = self.distance(w, word)
            props[word] = dist

        for i in range(self.max_proposition):
            word = list(props.keys())[np.argmax(props.values())]
            chosen_props.append(word)
            props.pop(word)
        return chosen_props

    def propositions(self, w: str or list):
        if isinstance(w, str):
            if w in self.glossary:
                return [w]
            else:
                return self._select_3(w)
        elif isinstance(w, list):
            return {w0: self.propositions(w0) for w0 in w}


class NullDistance(Distance):
    def __init__(self, glossary, max_proposition=10):
        super(NullDistance, self).__init__(glossary, max_proposition)

    def distance(self, w1, w2):
        return 0


class HammingDistance(Distance):
    def __init__(self, glossary, max_proposition=10):
        super(HammingDistance, self).__init__(glossary, max_proposition)


