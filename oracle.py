#!/usr/bin/env python3
# Sheet Fit oracle - mirrors engine.js with Fractions; the count along each axis comes from a binary search on whether n pieces and n-1 gaps fit, not from division.
import json, re, random
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP

def dec(t, name, zero_ok=False):
    t = t.strip() if isinstance(t, str) else ""
    m = re.fullmatch(r"([0-9]{1,4})(?:\.([0-9]{1,2}))?", t)
    err = f"the {name} must be a number {'from 0' if zero_ok else 'above 0'} and up to 9999.99, with at most 2 decimals"
    if not m: raise ValueError(err)
    v = Fraction(int(m.group(1))) + Fraction(int((m.group(2) or "0").ljust(2, "0")), 100)
    if v == 0 and not zero_ok: raise ValueError(err)
    return v
def num(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,6}", t) or not lo <= int(t) <= hi: raise ValueError(err)
    return int(t)
def fmt(fr):
    s = format((Decimal(fr.numerator) / Decimal(fr.denominator)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), "f")
    return s.rstrip("0").rstrip(".") if "." in s else s
def tenths(fr):
    s = format((Decimal(fr.numerator) / Decimal(fr.denominator)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP), "f")
    return s[:-2] if s.endswith(".0") else s
def pl(n, a, b): return f"{n} {a if n == 1 else b}"

def count(room, piece, gap):
    # binary search the largest n whose row (n pieces, n-1 gaps) still fits
    lo, hi = 0, 2000000
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid * piece + (mid - 1) * gap <= room: lo = mid
        else: hi = mid - 1
    return lo
def read(a):
    sw, sh, pw, ph = (dec(a[0], "sheet width"), dec(a[1], "sheet height"), dec(a[2], "piece width"), dec(a[3], "piece height"))
    g = dec(a[4], "gap", True); m = dec(a[5], "margin", True)
    return sw, sh, pw, ph, g, m
def layout(sw, sh, pw, ph, g, m):
    rw = sw - 2 * m; rh = sh - 2 * m
    if rw <= 0 or rh <= 0: raise ValueError("the margins leave no room on the sheet")
    A = count(rw, pw, g); B = count(rh, ph, g); C = count(rw, ph, g); D = count(rh, pw, g)
    return A, B, C, D
def head(sw, sh, pw, ph, g, m): return f"Sheet {fmt(sw)} by {fmt(sh)}, margin {fmt(m)}, gap {fmt(g)}, pieces {fmt(pw)} by {fmt(ph)}"

def grid(*a):
    sw, sh, pw, ph, g, m = read(a); A, B, C, D = layout(sw, sh, pw, ph, g, m)
    up, tu = A * B, C * D
    s = head(sw, sh, pw, ph, g, m) + f": upright gives {A} across by {B} down, {pl(up,'piece','pieces')}; turned gives {C} across by {D} down, {pl(tu,'piece','pieces')}. "
    if up == 0 and tu == 0: return s + "No piece fits on the sheet."
    if up == tu: return s + f"Both give {pl(up,'piece','pieces')}."
    return s + f"Best is {'upright' if up > tu else 'turned'} with {pl(max(up,tu),'piece','pieces')}."
def used(*a):
    sw, sh, pw, ph, g, m = read(a); A, B, C, D = layout(sw, sh, pw, ph, g, m)
    n = max(A * B, C * D)
    frac = Fraction(n) * pw * ph / (sw * sh) * 100
    u = tenths(frac)
    ut = int((Fraction(n) * pw * ph / (sw * sh) * 1000 + Fraction(1, 2)) // 1)
    left = tenths(Fraction(1000 - ut, 10))
    return head(sw, sh, pw, ph, g, m) + f": the best layout puts {pl(n,'piece','pieces')} on the sheet, covering {u}% of it and leaving {left}% for margins, gaps and offcuts."
def sheets(p, per, sp):
    n = num(p, "the number of pieces must be a whole number from 1 to 100000", 1, 100000)
    q = num(per, "the pieces per sheet must be a whole number from 1 to 10000", 1, 10000)
    r = num(sp, "the spare sheets must be a whole number from 0 to 1000", 0, 1000)
    s = 0; held = 0
    while held < n: s += 1; held += q
    room = held - n
    return f"{pl(n,'piece','pieces')} at {q} per sheet need {pl(s,'sheet','sheets')}, with room for {pl(room,'more piece','more pieces')} on the last sheet. With {pl(r,'spare sheet','spare sheets')} that is {pl(s+r,'sheet','sheets')} to buy."

FNS = {"gridTruth": grid, "usedTruth": used, "sheetsTruth": sheets}

def cases():
    c = []; rnd = random.Random(699)
    G = [["8.5","11","3.5","2","0","0"],["8.5","11","3.5","2","0.1","0.25"],["8.5","11","3.5","2","0.125","0.25"],["8.5","11","4.25","5.5","0","0"],["8.5","11","5","5","0","0"],["8.5","11","8.5","11","0","0"],["8.5","11","8.51","11","0","0"],["8.5","11","8.5","11","0","0.01"],["8.5","11","12","1","0","0"],["8.5","11","1","12","0","0"],
         ["8.5","11","12","13","0","0"],["10","10","4.99","4.99","0.02","0"],["10","10","5","5","0","0"],["10","10","5","5","0.01","0"],["10","10","5","3","0","0"],["10","6","3","5","0","0"],["10","10","1","1","0","4.99"],["10","10","1","1","0","5"],["10","10","1","1","0","6"],["0.01","0.01","0.01","0.01","0","0"],
         ["9999.99","9999.99","0.01","0.01","0","0"],["9999.99","9999.99","0.01","0.01","0.01","0"],["9999.99","9999.99","9999.99","9999.99","0","0"],["100","100","30","40","0","0"],["100","100","40","30","10","0"],
         ["0","11","3","2","0","0"],["8.5","0","3","2","0","0"],["8.5","11","0","2","0","0"],["8.5","11","3","0","0","0"],["8.5","11","3","2","-1","0"],["8.5","11","3","2","0","x"],["8.5","11","3","2","","0"],["8.5","11","3","2.001","0","0"],["10000","11","3","2","0","0"],[" 8.5 "," 11 "," 3.5 "," 2 "," 0.1 "," 0.25 "]]
    for a in G: c.append(("gridTruth", a))
    def rnd_args():
        sw = rnd.randint(100, 5000)/100; sh = rnd.randint(100, 5000)/100
        pw = rnd.randint(50, 2500)/100; ph = rnd.randint(50, 2500)/100
        g = rnd.choice([0, 0, 0.05, 0.1, 0.25, 0.5]); m = rnd.choice([0, 0, 0.1, 0.25, 0.5, 1])
        return [f"{sw:.2f}", f"{sh:.2f}", f"{pw:.2f}", f"{ph:.2f}", f"{g:.2f}", f"{m:.2f}"]
    for _ in range(40): c.append(("gridTruth", rnd_args()))
    for a in G[:25]: c.append(("usedTruth", a))
    for a in G[25:30]: c.append(("usedTruth", a))
    for _ in range(40): c.append(("usedTruth", rnd_args()))
    for a in [["100","10","0"],["101","10","0"],["99","10","0"],["1","1","0"],["1","1","5"],["100000","10000","1000"],["100001","1","0"],["0","10","0"],["10","0","0"],["10","10","1001"],["10","10001","0"],["x","10","0"],["10","10",""],["10","10","-1"],["10.5","10","0"],[" 25 "," 8 "," 2 "],["10","10","1"],["11","10","0"],["20","10","0"],["21","10","0"]]:
        c.append(("sheetsTruth", a))
    for _ in range(25): c.append(("sheetsTruth", [str(rnd.randint(1, 5000)), str(rnd.randint(1, 60)), str(rnd.randint(0, 20))]))
    return c

out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1); f.write("\n")
print(len(out), "cases written")
