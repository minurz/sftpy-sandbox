import glob, re
import numpy as np
import matplotlib.pyplot as plt

MAP_DIR = "./runs/nov06run02"   # SaveMap output folder
DT_DAYS = 1.0                   # simulation timestep (days)
CLIM = 6                        # colour limit (1e18 Mx per pixel)

files = sorted(glob.glob(f"{MAP_DIR}/map_*.npy"), key=lambda f: int(re.search(r"map_(\d+)", f)[1]))
steps = np.array([int(re.search(r"map_(\d+)", f)[1]) for f in files])
t = steps * DT_DAYS / 365.25

# SaveMap arrays are [phi, sin(lat)], sin(lat) from -1 (south) to +1 (north); equal-area pixels
bfly = np.stack([np.load(f).mean(axis=0) for f in files], axis=1)    # [sin(lat), time]
sinlat = -1 + (np.arange(bfly.shape[0]) + 0.5) * 2 / bfly.shape[0]
north = bfly[sinlat > 0.9].mean(axis=0)
south = bfly[sinlat < -0.9].mean(axis=0)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True, gridspec_kw=dict(height_ratios=[3, 1]))
im = ax1.imshow(bfly, aspect="auto", origin="lower", cmap="RdBu_r", vmin=-CLIM, vmax=CLIM,
                extent=[t[0], t[-1], -1, 1])
fig.colorbar(im, ax=ax1, pad=0.01, label="longitude-mean flux per pixel (1e18 Mx)")
ax1.set(ylabel="sin(latitude)", title="Magnetic butterfly diagram")

ax2.plot(t, north, color="C3", label="north cap (sin lat > 0.9)")
ax2.plot(t, south, color="C0", label="south cap (sin lat < -0.9)")
ax2.axhline(0, color="0.6", lw=0.8)
ax2.set(xlabel="time (yr)", ylabel="polar flux per pixel")
ax2.legend(frameon=False, fontsize=8)
fig.tight_layout()
plt.show()