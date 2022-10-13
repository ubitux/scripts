import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def mix(a, b, x): return (1 - x) * a + b * x
def linear(a, b, x): return (x - a) / (b - a)
def remap(a, b, c, d, x): return mix(c, d, linear(a, b, x))

def bezier1(p0, p1, t): return mix(p0, p1, t)
def bezier2(p0, p1, p2, t): return bezier1(mix(p0, p1, t), mix(p1, p2, t), t)
def bezier3(p0, p1, p2, p3, t): return bezier2(mix(p0, p1, t), mix(p1, p2, t), mix(p2, p3, t), t)

def _main():
    pad = 0.05
    bmin, bmax = -1, 1
    x_color, y_color, xy_color = "#ff4444", "#44ff44", "#ffdd00"

    np.random.seed(0)
    r0, r1 = np.random.uniform(-1, 1, (2, 4))
    r2, r3 = np.random.uniform(0, 2 * np.pi, (2, 4))

    cfg = {
        "axes.facecolor": "333333",
        "figure.facecolor": "111111",
        "font.family": "monospace",
        "font.size": 9,
        "grid.color": "666666",
    }
    plt.style.use("dark_background")
    with plt.rc_context(cfg):
        fig = plt.figure(figsize=[8, 4.5])
        gs = fig.add_gridspec(nrows=2, ncols=3)

        ax_x = fig.add_subplot(gs[0, 0])
        ax_x.grid(True)
        for i in range(4):
            ax_x.axvline(x=i / 3, linestyle="--", alpha=0.5)
        ax_x.axhline(y=0, alpha=0.5)
        ax_x.set_xlabel("t")
        ax_x.set_ylabel("x", rotation=0, color=x_color)
        ax_x.set_xlim(0 - pad, 1 + pad)
        ax_x.set_ylim(bmin - pad, bmax + pad)
        (x_plt,) = ax_x.plot([], [], "-", color=x_color)
        (x_plt_c0,) = ax_x.plot([], [], "o:", color=x_color)
        (x_plt_c1,) = ax_x.plot([], [], "o:", color=x_color)

        ax_y = fig.add_subplot(gs[1, 0])
        ax_y.grid(True)
        for i in range(4):
            ax_y.axvline(x=i / 3, linestyle="--", alpha=0.5)
        ax_y.axhline(y=0, alpha=0.5)
        ax_y.set_xlabel("t")
        ax_y.set_ylabel("y", rotation=0, color=y_color)
        ax_y.set_xlim(0 - pad, 1 + pad)
        ax_y.set_ylim(bmin - pad, bmax + pad)
        (y_plt,) = ax_y.plot([], [], "-", color=y_color)
        (y_plt_c0,) = ax_y.plot([], [], "o:", color=y_color)
        (y_plt_c1,) = ax_y.plot([], [], "o:", color=y_color)

        ax_xy = fig.add_subplot(gs[0:2, 1:3])
        ax_xy.grid(True)
        ax_xy.axvline(x=0, alpha=0.8)
        ax_xy.axhline(y=0, alpha=0.8)
        ax_xy.set_aspect("equal", "box")
        ax_xy.set_xlabel("x", color=x_color)
        ax_xy.set_ylabel("y", rotation=0, color=y_color)
        ax_xy.set_xlim(bmin - pad, bmax + pad)
        ax_xy.set_ylim(bmin - pad, bmax + pad)
        (xy_plt,) = ax_xy.plot([], [], "-", color=xy_color)
        (xy_plt_c0,) = ax_xy.plot([], [], "o:", color=xy_color)
        (xy_plt_c1,) = ax_xy.plot([], [], "o:", color=xy_color)

        fig.tight_layout()

        def update(frame):
            px = remap(-1, 1, bmin, bmax, np.sin(r0 * frame + r2))
            py = remap(-1, 1, bmin, bmax, np.sin(r1 * frame + r3))
            t = np.linspace(0, 1)
            x = bezier3(px[0], px[1], px[2], px[3], t)
            y = bezier3(py[0], py[1], py[2], py[3], t)

            x_plt.set_data(t, x)
            x_plt_c0.set_data((0, 1 / 3), (px[0], px[1]))
            x_plt_c1.set_data((2 / 3, 1), (px[2], px[3]))

            y_plt.set_data(t, y)
            y_plt_c0.set_data((0, 1 / 3), (py[0], py[1]))
            y_plt_c1.set_data((2 / 3, 1), (py[2], py[3]))

            xy_plt.set_data(x, y)
            xy_plt_c0.set_data((px[0], px[1]), (py[0], py[1]))
            xy_plt_c1.set_data((px[2], px[3]), (py[2], py[3]))

        duration, fps, speed = 15, 60, 3
        frames = np.linspace(0, duration * speed, duration * fps)
        anim = FuncAnimation(fig, update, frames=frames)
        anim.save("/tmp/bezier.webm", fps=fps, codec="vp9", extra_args=["-preset", "veryslow", "-tune-content", "screen"])


if __name__ == "__main__":
    _main()
