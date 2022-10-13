from math import sqrt, ceil
from matplotlib.gridspec import GridSpec

def axgen(fig, n):
    rows = round(sqrt(n))
    cols = ceil(n / rows)
    gs = GridSpec(rows, cols, figure=fig)
    for i in range(n):
        yield fig.add_subplot(gs[i])
