import numpy as np
from collections import deque


class Distance:
    def __init__(self, glossary: dict, max_proposition):
        self.glossary = glossary
        self.max_proposition = max_proposition
        pass

    def distance(self, w1, w2):
        raise NotImplementedError()

    def propositions(self, w: str or list):
        if isinstance(w, str):
            if w in self.glossary:
                return [w]
            else:
                props = {}
                chosen_props = []
                for o_word in self.glossary.keys():
                    dist = self.distance(w, o_word)
                    props[o_word] = dist

                for i in range(self.max_proposition):
                    o_word = list(props.keys())[np.argmax(props.values())]
                    chosen_props.append(o_word)
                    props.pop(o_word)

                return chosen_props
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


