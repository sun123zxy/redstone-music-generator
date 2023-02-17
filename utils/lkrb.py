from math import floor, ceil


def force2str(force: int) -> str:
        if force == 0 : return "ppp"
        elif force == 1: return "pp"
        elif force == 2: return "p"
        elif force == 3: return "mp"
        elif force == 4: return "mf"
        elif force == 5: return "f"
        elif force == 6: return "ff"
        elif force == 7: return "fff"
        else: return None
def velocity2force(velocity: int) -> int:
        return floor(velocity / 16)
def force2velocity(force: int) -> int:
        return force * 16 + 8