
from app.config.settings import REGION_ID

class LWWRefCRDT:

    @staticmethod
    def merge(a, b):
        # merge vector clocks
        merged_clock = {}
        keys = set(a["clock"]).union(set(b["clock"]))
        for k in keys:
            merged_clock[k] = max(a["clock"].get(k, 0), b["clock"].get(k, 0))

        # choose value based on clock dominance
        def dominates(x, y):
            greater = False
            for k in merged_clock:
                xv = x["clock"].get(k, 0)
                yv = y["clock"].get(k, 0)
                if xv < yv:
                    return False
                if xv > yv:
                    greater = True
            return greater

        if dominates(a, b):
            value = a["value"]
        elif dominates(b, a):
            value = b["value"]
        else:
            # deterministic tie-breaker
            value = max(a["value"], b["value"])

        return {"value": value, "clock": merged_clock}

    @staticmethod
    def increment_clock(clock):
        clock = dict(clock)
        clock[REGION_ID] = clock.get(REGION_ID, 0) + 1
        return clock
