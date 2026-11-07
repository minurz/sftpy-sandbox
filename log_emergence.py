"""
Run simulate.py's setup_sim() and log what every region emerges each step:
nnew (bipoles per step) and each bipole's phi, theta, flux.

Hooks each region's fill_new_spots, so positions are AFTER nesting (what actually emerges).
Nothing in sftpy is modified, and the random stream is untouched.

Output (npz): for each region label L
  L/nnew   int32 [nsteps]      bipoles emerged at each step (0 when the region was skipped)
  L/step   int32 [nbipoles]    step of each logged bipole
  L/phi, L/theta  float32      bipole centre (rad)
  L/flux   int32               bipole flux (BINFLUX units, 1e18 Mx)
"""
import importlib.util
import sys
from pathlib import Path
import numpy as np

SFTPY_ROOT = Path("~/sftpy").expanduser()     # folder containing simulate.py and sftpy/
NSTEPS = None                                 # None = full timeline; or e.g. 2000
OUT = Path("runs/emergence_log.npz")
SPOTS_FOR = ("SchrijverBipole",)              # classes whose individual bipoles are logged
                                              # (nnew is logged for every region; ephemerals add ~3000/day)
PROGRESS_EVERY = 250

sys.path.insert(0, str(SFTPY_ROOT))
from sftpy.emerge import SchrijverEmerge

spec = importlib.util.spec_from_file_location("sft_simulate", SFTPY_ROOT / "simulate.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
sim = mod.setup_sim()
time = sim._time
nsteps = time.nstep - time.step if NSTEPS is None else NSTEPS

emerge = next(a for a in sim._sequence if isinstance(a, SchrijverEmerge))
acts = list(dict.fromkeys(id(r.activity) for r in emerge.regions))
log = {}

def hook(region):
    label = f"{type(region).__name__}_cycle{acts.index(id(region.activity)) + 1}"
    rec = log[label] = dict(nnew=np.zeros(nsteps, np.int32), step=[], phi=[], theta=[], flux=[])
    keep = type(region).__name__ in SPOTS_FOR
    orig = region.fill_new_spots
    def wrapped(data):
        n, k = data.nflux, time.step - start
        if 0 <= k < nsteps:
            rec["nnew"][k] = n
            if keep and n:
                rec["step"].append(np.full(n, time.step, np.int32))
                rec["phi"].append(data.phi[:n].astype(np.float32))
                rec["theta"].append(data.theta[:n].astype(np.float32))
                rec["flux"].append(data.flux[:n].astype(np.int32))
        return orig(data)
    region.fill_new_spots = wrapped

start = time.step
for r in emerge.regions:
    hook(r)

def save():
    out = {}
    for label, rec in log.items():
        out[f"{label}/nnew"] = rec["nnew"]
        for key in ("step", "phi", "theta", "flux"):
            out[f"{label}/{key}"] = np.concatenate(rec[key]) if rec[key] else np.array([])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(OUT, **out)
    print("saved", OUT)

try:
    for i in range(1, nsteps + 1):
        for a in sim._sequence:          # same loop as Simulation.run
            a.simulate()
        if PROGRESS_EVERY and i % PROGRESS_EVERY == 0:
            print(f"step {i}/{nsteps}")
finally:
    save()                               # also saves what was logged if interrupted
    if getattr(sim, "_pool", None) is not None:
        sim._pool.terminate()

# reading it back:
#   d = np.load("runs/emergence_log.npz")
#   d["SchrijverBipole_cycle1/nnew"], d["SchrijverBipole_cycle1/phi"], ...
