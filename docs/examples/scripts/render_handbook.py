"""Render the walkthrough's displayed values from its executable source."""

from pathlib import Path
from runpy import run_path


def render_tables() -> dict[str, str]:
    """Return reproducible Markdown tables for the walkthrough."""
    example = run_path(str(Path(__file__).with_name("walkthrough.py")))
    skin = example["skin"]
    result = example["result"]
    stiff = result.stiffness
    comparison = "| Quantity | Skin | Stiffened panel | Unit |\n| --- | ---: | ---: | --- |\n"
    for name, before, after, unit in (
        ("A11", skin.A[0, 0], stiff.A[0, 0], "N/m"),
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
    return {
        "walkthrough-comparison.md": comparison,
        "walkthrough-response.md": response,
        "walkthrough-warnings.md": warnings,
    }


if __name__ == "__main__":
    output = Path(__file__).resolve().parents[2] / "includes"
    output.mkdir(exist_ok=True)
    for filename, text in render_tables().items():
        (output / filename).write_text(text)
