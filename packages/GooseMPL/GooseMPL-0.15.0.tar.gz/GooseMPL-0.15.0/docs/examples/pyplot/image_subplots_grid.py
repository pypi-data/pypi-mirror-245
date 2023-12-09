import matplotlib.pyplot as plt
import numpy as np

plt.style.use(["goose", "goose-latex"])

fig, axes = plt.subplots(figsize=(8, 8), ncols=2, nrows=2, constrained_layout=True)

for ax in axes.ravel():
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

data = np.random.random([10, 10])
mappable = np.empty(axes.shape, dtype=object)

for row in range(axes.shape[0]):
    for col in range(axes.shape[1]):
        mappable[row, col] = axes[row, col].imshow(data, cmap="jet", clim=(0, 1))

cbar = fig.colorbar(mappable[-1, 0], ax=axes[-1, :], orientation="horizontal")
cbar.set_label(r"$v$")

axes[0, 0].set_title(r"first")
axes[0, 1].set_title(r"second")

fig.savefig("image_subplots_grid.svg")
plt.close(fig)
