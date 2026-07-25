import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # PRISM claim-by-claim reproduction

        <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:8px">
          <div style="padding:12px;background:#0f766e;color:white;border-radius:8px"><b>1</b><br>VERIFIED<br>HIGH</div>
          <div style="padding:12px;background:#b45309;color:white;border-radius:8px"><b>2</b><br>FALSIFIED<br>HIGH</div>
          <div style="padding:12px;background:#b45309;color:white;border-radius:8px"><b>3</b><br>FALSIFIED<br>HIGH</div>
          <div style="padding:12px;background:#475569;color:white;border-radius:8px"><b>4</b><br>BLOCKED<br>LOW</div>
          <div style="padding:12px;background:#475569;color:white;border-radius:8px"><b>5</b><br>BLOCKED<br>LOW</div>
          <div style="padding:12px;background:#475569;color:white;border-radius:8px"><b>6</b><br>BLOCKED<br>LOW</div>
        </div>

        **Live judge score: 5/12. Conservative forecast: 5–8/12.**
        The forecast is not a judge result.
        """
    )
    return


@app.cell
def _():
    claim_rows = [
        {
            "claim": 1,
            "status": "VERIFIED",
            "confidence": "HIGH",
            "paper": "Adaptive residual-polynomial fit without explicit spectral bounds",
            "observed": "52 identifiable dense comparisons; max alpha discrepancy 1.81e-8",
        },
        {
            "claim": 2,
            "status": "FALSIFIED",
            "confidence": "HIGH",
            "paper": "Printed quadratic bound for every stated-domain matrix",
            "observed": "Exact residual 50 versus bound 2 at k=2",
        },
        {
            "claim": 3,
            "status": "FALSIFIED",
            "confidence": "HIGH",
            "paper": "Sketched bound with probability at least 1-delta",
            "observed": "Same exact violation with probability one",
        },
        {
            "claim": 4,
            "status": "BLOCKED",
            "confidence": "LOW",
            "paper": "Shampoo/ResNet first-50-epoch timing",
            "observed": "Four routes; exact integration and timing protocol unavailable",
        },
        {
            "claim": 5,
            "status": "BLOCKED",
            "confidence": "LOW",
            "paper": "Validation losses 5.0251 / 5.4523 / 6.8689",
            "observed": "Four routes; exact model, data order, and checkpoints unavailable",
        },
        {
            "claim": 6,
            "status": "BLOCKED",
            "confidence": "LOW",
            "paper": "Stable convergence over six Gaussian/HTMP settings",
            "observed": "Four routes; unpublished draw and protocol prevent exact comparison",
        },
    ]
    return (claim_rows,)


@app.cell
def _(claim_rows, mo):
    claim_picker = mo.ui.dropdown(
        options={f"Claim {row['claim']}": row["claim"] for row in claim_rows},
        value="Claim 1",
        label="Inspect a claim",
    )
    claim_picker
    return (claim_picker,)


@app.cell
def _(claim_picker, claim_rows, mo):
    selected_row = next(
        row for row in claim_rows if row["claim"] == claim_picker.value
    )
    mo.md(
        f"""
        ## Claim {selected_row['claim']}: {selected_row['status']}

        **Paper statement.** {selected_row['paper']}

        **Observed evidence.** {selected_row['observed']}

        **Confidence.** {selected_row['confidence']}
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The adaptive mechanism

        For the degree-5 polar iteration, the tested update is

        \[
        R=I-X^\top X,\quad
        g_2(R;\alpha)=I+\tfrac12R+\alpha R^2,\quad
        X_+=Xg_2(R;\alpha).
        \]

        The primary implementation minimizes the next dense residual directly.
        An independent route derives the quartic loss from the eigenvalues of
        \(R\). Across 52 identifiable states the fitted coefficients differ by
        at most \(1.81\times10^{-8}\), and next residuals differ by at most
        \(8.88\times10^{-16}\). A constant-alpha mutation collapses nine
        adaptive profiles to one and exits nonzero.
        """
    )
    return


@app.cell
def _():
    theorem_series = {
        "iteration": [0, 1, 2, 3],
        "residual": [2, 5, 50, 33125],
        "bound_iteration": [2, 3],
        "bound": [2, 4],
    }
    return (theorem_series,)


@app.cell
def _(theorem_series):
    import matplotlib.pyplot as plt

    theorem_figure, theorem_axis = plt.subplots(figsize=(8, 4.2))
    theorem_axis.semilogy(
        theorem_series["iteration"],
        theorem_series["residual"],
        marker="o",
        linewidth=2.5,
        label="exact residual",
    )
    theorem_axis.semilogy(
        theorem_series["bound_iteration"],
        theorem_series["bound"],
        marker="o",
        linestyle="--",
        linewidth=2.5,
        label="printed bound",
    )
    theorem_axis.set(
        title="Exact stated-domain counterexample",
        xlabel="iteration k",
        ylabel="spectral residual / bound",
        xticks=[0, 1, 2, 3],
    )
    theorem_axis.grid(alpha=0.25)
    theorem_axis.legend()
    theorem_figure
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        The matrix \(A=\begin{bmatrix}0&-1\\1&0\end{bmatrix}\) is real,
        has \(\lVert A\rVert_2=1\), and has symmetric \(A^2=-I\). Exact
        rational iteration violates Theorem 1. Its residual is always a scalar
        multiple of identity, so Gaussian sketching rescales—but cannot change—
        the alpha objective. Theorem 2 therefore fails with probability one on
        the same printed domain.

        ## Why the other claims remain blocked

        Claims 4–6 each received three materially different verification routes
        plus a mandatory falsification route. The available substitutes violate
        the exact unpublished model, data-draw, seed, or timing assumptions.
        Missing evidence and downscaled CPU feasibility checks are never treated
        as falsification.

        One important correction: the paper appendix says **PRISM5 used three
        matrix iterations** in the GPT experiment, not five.

        ## Reproducibility

        Fixed command:

        ```text
        uv run --frozen --python 3.11 python repro/src/run_reproduction.py
        ```

        Cumulative run: Hugging Face `cpu-upgrade`, six workers estimated,
        64 logical CPUs visible, 248.763 seconds runner time. The notebook embeds
        the released evidence; rerunning the expensive verifier is optional.
        """
    )
    return


if __name__ == "__main__":
    app.run()
