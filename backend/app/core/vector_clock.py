
from collections import defaultdict

class VectorClock:

    @staticmethod
    def increment(clock, region):
        clock = dict(clock)
        clock[region] = clock.get(region, 0) + 1
        return clock

    @staticmethod
    def compare(a, b):
        # returns: "gt", "lt", "equal", "concurrent"
        a_keys = set(a.keys())
        b_keys = set(b.keys())
        all_keys = a_keys.union(b_keys)

        greater = False
        less = False

        for k in all_keys:
            av = a.get(k, 0)
            bv = b.get(k, 0)
            if av > bv:
                greater = True
            elif av < bv:
                less = True

        if greater and not less:
            return "gt"
        if less and not greater:
            return "lt"
        if not greater and not less:
            return "equal"
        return "concurrent"
