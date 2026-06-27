# Markdown Authoring

Tensyl documentation is written to render in both Obsidian and MkDocs.

## Math

Use dollar-delimited TeX math:

- inline math: `$A_{11}$`
- display math:

```text
$$
\mathbf r=\mathbf C_\text{wall}\boldsymbol\eta
$$
```

Prefer dollar delimiters over `\(...\)` and `\[...\]` in source Markdown. MkDocs
uses PyMdown Arithmatex and MathJax to render this syntax, and Obsidian renders
the same source directly.

For multi-line equations, keep the delimiters on their own lines:

```text
$$
\begin{aligned}
\rho_h &= \frac{h_s}{R_\text{min}}, \\
\rho_p &= \frac{p}{R_\text{min}}.
\end{aligned}
$$
```

Do not put Markdown links, emphasis, or tables inside math blocks. Use
`\text{...}` only for short labels inside equations.

## Tables

Use GitHub-Flavored Markdown pipe tables:

```text
| Quantity | Meaning |
|---|---|
| $A_{11}$ | membrane stiffness term |
```

Keep tables simple:

- include one header separator immediately after the header row;
- put inline math inside table cells with `$...$`;
- escape literal pipe characters in cell text as `\|`;
- use `<br>` only when a source-reference table needs an intentional line break;
- avoid display math inside table cells.

Large source-derived tables under `docs/references/` may preserve upstream PDF
conversion artifacts when exact provenance is more important than table polish.
