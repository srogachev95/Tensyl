"""Render the walkthrough's displayed values from its executable source."""

from pathlib import Path
from runpy import run_path


def render_tables() -> dict[str, str]:
    """Return reproducible Markdown tables for the walkthrough."""
    example = run_path(str(Path(__file__).with_name("walkthrough.py")))
    skin = example["skin"]
    result = example["result"]
    stiff = result.stiffness
    comparison = "| Quantity | Skin | Panel | Unit |\n| --- | ---: | ---: | --- |\n"
    for name, before, after, unit in (
        ("A11", skin.A[0, 0] / 1e6, stiff.A[0, 0] / 1e6, "MN/m"),
        ("B11", skin.B[0, 0], stiff.B[0, 0], "N"),
        ("D11", skin.D[0, 0], stiff.D[0, 0], "N m"),
        ("Areal mass", skin.areal_mass, stiff.areal_mass, "kg/m²"),
    ):
        comparison += f"| {name} | {before:,.6g} | {after:,.6g} | {unit} |\n"
    response = "| Response to N11 = 10,000 N/m | Value | Unit |\n| --- | ---: | --- |\n"
    for name, value, unit in (
        ("Reference-surface strain ε11", example["strain"][0], "m/m"),
        ("Curvature κ11", example["strain"][3], "1/m"),
        ("First e1 rib axial force", example["rib_loads"][0].axial_force, "N"),
        ("First e1 rib bending moment", example["rib_loads"][0].bending_moment, "N m"),
    ):
        response += f"| {name} | {value:.6g} | {unit} |\n"
    warnings = "\n".join(f"- `{code}`" for code in result.validity.warnings) + "\n"
    workflow = run_path(str(Path(__file__).with_name("panel_workflows.py")))
    sweep = "| Rib spacing (mm) | A11 (MN/m) | D11 (N m) | Mass (kg/m²) |\n"
    sweep += "| ---: | ---: | ---: | ---: |\n"
    for row in workflow["rows"]:
        sweep += (
            f"| {row['spacing'] * 1000:g} | {row['A11'] / 1e6:.3f} "
            f"| {row['D11']:.2f} | {row['areal_mass']:.2f} |\n"
        )
    return {
        "walkthrough-comparison.md": comparison,
        "walkthrough-response.md": response,
        "walkthrough-warnings.md": warnings,
        "pitch-sweep.md": sweep,
    }


def render_sweep_plot(path: Path) -> None:
    """Plot the same sweep that supplies the handbook table."""
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    rows = run_path(str(Path(__file__).with_name("panel_workflows.py")))["rows"]
    plt.rcParams["svg.hashsalt"] = "tensyl-pitch-sweep"
    fig, axes = plt.subplots(2, 1, figsize=(6.2, 4.8), sharex=True, layout="constrained")
    for ax, name, label in zip(
        axes, ("D11", "areal_mass"), ("D11 (N m)", "Panel mass (kg/m²)"), strict=True
    ):
        ax.plot([row["spacing"] * 1000 for row in rows], [row[name] for row in rows], "o-")
        ax.set_ylabel(label)
        ax.grid(alpha=0.3)
    axes[-1].set_xlabel("Rib spacing (mm)")
    fig.savefig(path, metadata={"Date": None})
    plt.close(fig)


if __name__ == "__main__":
    output = Path(__file__).resolve().parents[2] / "includes"
    output.mkdir(exist_ok=True)
    for filename, text in render_tables().items():
        (output / filename).write_text(text)
    render_sweep_plot(output.parent / "assets/examples/pitch-sweep.svg")
