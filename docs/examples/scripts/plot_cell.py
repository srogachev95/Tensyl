"""Draw two repeats of the handbook's custom orthogrid, in SI units."""

from pathlib import Path
from runpy import run_path

# --8<-- [start:plot]
from matplotlib import pyplot as plt


def plot_cell(cell, *, repeat_a=2, repeat_b=2):
    geometry = cell.geometry
    if geometry is None:
        raise ValueError("Supply a cell with drawable geometry.")
    _, axes = plt.subplots()
    for segment in geometry.segments(repeat_a=repeat_a, repeat_b=repeat_b):
        axes.plot(
            [segment.start_e1, segment.end_e1],
            [segment.start_e2, segment.end_e2],
            color="#176b87",
        )
    axes.set_aspect("equal")
    axes.set_xlabel("e1 (m)")
    axes.set_ylabel("e2 (m)")
    return axes


# --8<-- [end:plot]

if __name__ == "__main__":
    cell = run_path(str(Path(__file__).with_name("panel_workflows.py")))["custom_cell"]
    axes = plot_cell(cell)
    axes.figure.savefig("cell.png", bbox_inches="tight")
    plt.close(axes.figure)
