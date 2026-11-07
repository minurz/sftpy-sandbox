"""
Test longitude wrapping in interact.collide2.

Builds spot pairs closer than the collision radius, some straddling phi = 0 / 2pi and
identical control pairs away from the seam, runs the real collide2, and reports which
pairs coalesced. Repeats with every phi rotated by pi, which moves the seam: if the
straddling pairs then merge, the miss is caused by the seam alone.
"""
import sys
from pathlib import Path
import numpy as np

SFTPY_ROOT = Path("~/sftpy").expanduser()          # folder containing the sftpy package
sys.path.insert(0, str(SFTPY_ROOT))

from sftpy.interact._collide import collide2
from sftpy.interact.constants import COL_RADIUS, NSKIP
from sftpy.sim.constants import STAR_RADIUS

CRPHI = COL_RADIUS / STAR_RADIUS                    # collision radius (rad), as SchrijverCollide uses
SEP = 0.3 * CRPHI                                   # pair separation: well inside the radius
LATS = [0.0, 30.0, 60.0]                            # deg
FILLER = 60                                         # isolated spots so nflux > NSKIP, like a real step


def make_spots(rotate=0.0):
    phi, theta, flux, tag = [], [], [], []
    for lat in LATS:
        th = np.radians(90 - lat)
        dphi = SEP / np.sin(th)                     # same great-circle separation at every latitude
        for centre, kind in ((0.0, "seam"), (np.pi, "control")):
            phi += [centre - dphi / 2, centre + dphi / 2]
            theta += [th, th]
            flux += [10, -4]                        # opposite signs: merge leaves +6
            tag += [f"{kind:7s} lat {lat:4.0f}"] * 2
    # isolated filler spots far from everything above (|lat| > 75, spaced > CRPHI apart)
    phi += list(np.linspace(0.2, 6.0, FILLER)); theta += [np.radians(10)] * FILLER
    flux += [1] * FILLER; tag += ["filler"] * FILLER
    phi = (np.array(phi) + rotate) % (2 * np.pi)
    return phi, np.array(theta), np.array(flux, np.int64), np.array(tag)


def run(rotate):
    phi, theta, flux, tag = make_spots(rotate)
    n = len(phi)
    nskip = 1 if n <= NSKIP else NSKIP
    keys = {(round(t, 9), round(p, 9)): g for p, t, g in zip(phi, theta, tag)}   # collide2 re-sorts
    order = np.arange(n, dtype=np.int64)
    rvs = np.zeros(n)
    nnew = collide2(phi, theta, flux, n, nskip, CRPHI, order, rvs)
    survivors = [keys[(round(t, 9), round(p, 9))] for p, t in zip(phi[:nnew], theta[:nnew])]
    print(f"\nphi rotated by {rotate:.3f} rad: {n} spots in, {nnew} out")
    for g in dict.fromkeys(t for t in tag if t != "filler"):
        left = survivors.count(g)
        print(f"  {g}: {'MERGED' if left == 1 else 'NOT merged (' + str(left) + ' spots left)'}")


print(f"collision radius {COL_RADIUS:g} km = {CRPHI:.5f} rad; pair separation {SEP:.5f} rad")
run(0.0)          # seam pairs straddle phi = 0
run(np.pi)        # seam moved: former seam pairs now sit at phi = pi
