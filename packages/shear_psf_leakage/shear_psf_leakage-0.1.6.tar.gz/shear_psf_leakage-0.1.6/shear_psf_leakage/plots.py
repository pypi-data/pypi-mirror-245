"""PLOTS.

:Name: plots.py

:Description: This script contains methods for plots.

:Author: Martin Kilbinger


"""

import numpy as np
from scipy import stats
from matplotlib import pylab as plt

from shear_psf_leakage import leakage


def equi_num_bins(values, n_bin):
    """Equi Num Bins.

    Return (n_bin+1) equi-numbered bin edges. These define n_bin
    bins, each of which contains an equal number of points of values.

    Parameters
    ----------
    values : list
        input data
    n_bins : int
        number of bins

    Returns
    -------
    numpy.array
        equi-numbered bin array

    """
    xeqn = np.interp(
        np.linspace(0, len(values), n_bin + 1),
        np.arange(len(values)),
        np.sort(values),
    )

    return xeqn


def compute_bins_func_2d(x, y, n_bin, mix, weights=None):
    """Compute Bins Func 2D.

    Compute bins in x, y, err, for 2D model.

    Parameters
    ----------
    x : 2D numpy.ndarray
        x_1, x_2-values
    y : 2D numpy.ndarray
        y_1, y_2-values
    n_bin : int
        number of bins to create
    mix : bool
        mixing of component if True
    weights  : numpy.ndarrayarray of double, optional, default=None
        weights of x points

    Returns
    -------
    numpy.ndarray
        bin centers in x_1, x_2
    numpy.ndarray
        binned values of y_1, y_2 corresponding to x_1, x_2 bins
    numpy.ndarray
        binned errors of y_1, y_2 corresponding to x_1, x_2 bins

    """
    # Compute bins in x

    # Initialise bins and edges for x
    x_bin = np.zeros(shape=(2, n_bin))
    x_edges = np.zeros(shape=(2, n_bin + 1))

    # Loop over both components, compute equi-numbered bins
    for comp in (0, 1):
        xeqn = equi_num_bins(x[comp], n_bin)
        res = stats.binned_statistic(x[comp], x[comp], "mean", bins=xeqn)
        x_bin[comp] = res.statistic
        x_edges[comp] = res.bin_edges

    # Compute bins in y and errors

    # Initialise
    y_bin = np.zeros(shape=(2, 2, n_bin))
    err_bin = np.zeros(shape=(2, 2, n_bin))

    # Loop over both components corresponding to x (comp_x),
    # and y and err (comp_y)
    for comp_x in (0, 1):
        for comp_y in (0, 1):
            # No mixing and different y-/x-component: not used
            if not mix and (comp_x != comp_y):
                continue

            # 1d y bins
            if weights is None:
                y_bin[comp_y][comp_x] = stats.binned_statistic(
                    x[comp_x], y[comp_y], "mean", bins=x_edges[comp_x]
                ).statistic
            else:
                yw = stats.binned_statistic(
                    x[comp_x], y[comp_y] * weights, "sum", bins=x_edges[comp_x]
                ).statistic
                w = stats.binned_statistic(
                    x[comp_x], weights, "sum", bins=x_edges[comp_x]
                ).statistic
                y_bin[comp_y][comp_x] = yw / w

            # 1d numbers
            n = stats.binned_statistic(
                x[comp_x], y[comp_y], "count", bins=x_edges[comp_x]
            ).statistic

            # 1d errors of the mean = standard deviation devided by sqrt
            # of the numbers
            err_bin[comp_y][comp_x] = stats.binned_statistic(
                x[comp_x], y[comp_y], "std", bins=x_edges[comp_x]
            ).statistic / np.sqrt(n)

    return x_bin, y_bin, err_bin


def set_labels(p_dp, order, mix, par_ground_truth=None):
    """Set Labels.

    Set labels for plot of 2D fit.

    Parameters
    ----------
    d_dp : dict
        values with uncertainties of fit parameters
    order : str
        linear ('lin') or quadratic ('quad') model
    mix : bool
        mixing of components if True

    Returns
    -------
    dict
        label strings

    """
    # Affine parameters
    label = {}

    # Linear parameters
    label["A"] = f'$a_{{11}}={p_dp["a11"]: .2ugL}$'
    label["D"] = f'$a_{{22}}={p_dp["a22"]: .2ugL}$'
    if par_ground_truth:
        label["A"] = f"{label['A']} ({par_ground_truth['a11'].value})"
        label["D"] = f"{label['D']} ({par_ground_truth['a22'].value})"
    
    # Constant parameters
    label["A"] = label["A"] + "\n" + f'$c_1={p_dp["c1"]: .2ugL}$'
    label["D"] = label["D"] + "\n" + f'$c_2={p_dp["c2"]: .2ugL}$'
    if par_ground_truth:
        label["A"] = f"{label['A']} ({par_ground_truth['c1'].value})"
        label["D"] = f"{label['D']} ({par_ground_truth['c2'].value})"

    if order == "quad":
        # Add quadratic parameters
        label_q111 = f'$q_{{111}}={p_dp["q111"]: .2ugL}$'
        label_q222 = f'$q_{{222}}={p_dp["q222"]: .2ugL}$'
        if par_ground_truth:
            label_q111 = f"{label_q111} ({par_ground_truth['q111'].value})"
            label_q222 = f"{label_q222} ({par_ground_truth['q222'].value})"
        label["A"] = label_q111 + "\n" + label["A"]
        label["D"] = label_q222 + "\n" + label["D"]
    if mix:
        # Mixed linear parameters
        label["B"] = f'$a_{{12}}={p_dp["a12"]: .2ugL}$'
        label["C"] = f'$a_{{21}}={p_dp["a21"]: .2ugL}$'
        if par_ground_truth:
            label["B"] = f"{label['B']} ({par_ground_truth['a12'].value})"
            label["C"] = f"{label['C']} ({par_ground_truth['a21'].value})"

        # Mixed quadratic parameters
        if order == "quad":
            label_q211 = f'$q_{{211}}={p_dp["q211"]: .2ugL}$'
            label_q212 = f'$q_{{212}}={p_dp["q212"]: .2ugL}$'
            label_q122 = f'$q_{{122}}={p_dp["q122"]: .2ugL}$'
            label_q112 = f'$q_{{112}}={p_dp["q112"]: .2ugL}$'

            if par_ground_truth:
                label_q211 = f"{label_q211} ({par_ground_truth['q211'].value})"
                label_q212 = f"{label_q212} ({par_ground_truth['q212'].value})"
                label_q122 = f"{label_q122} ({par_ground_truth['q122'].value})"
                label_q112 = f"{label_q112} ({par_ground_truth['q112'].value})"

            label["B"] = label_q211 + "\n" + label_q212 + "\n" + label["B"]
            label["C"] = label_q122 + "\n" + label_q112 + "\n" + label["C"]

    return label


def plot_bar_spin(par, s_ground_truth, output_path=None):
    """Plot Bar Spin.

    Create bar plot of spin coefficients.

    Parameters
    ----------
    par : dict of ufloat
        parameter values and standard deviations
    s_ground_truth : dict, optional
        ground truth parameter, for plotting, default is `None`
    output_path : str, optional
        plot output file if not `None` (default)

    """
    # Shift of real and imaginary components
    dx = 0.4

    # Colors of rea and imaginary components
    colors = {"real": "b", "imaginary": "g"}

    # Set data for bar plot
    x = []
    y = []
    dy = []
    col = []
    s = set()
    for key in par:
        z = key[0]
        spin = int(key[1:])
        s.add(spin)
        if z == "x":
            x.append(spin - dx)
            col.append(colors["real"])
        else:
            x.append(spin + dx)
            col.append(colors["imaginary"])

        y.append(par[key].nominal_value)
        dy.append(par[key].std_dev)

    fig, ax = plt.subplots()

    bars = ax.bar(
        x,
        y,
        yerr=dy,
        align="center",
        alpha=0.5,
        ecolor="black",
        capsize=8,
        width=0.7,
        color=col,
    )
    xlim = ax.get_xlim()
    ax.plot(xlim, [0, 0], "k-")
    ax.set_ylabel(r"$z_s = x_s + \mathrm{i} y_s$")
    xl = list(s)
    ax.set_xticks(xl)
    ax.set_xlabel("$s$")

    for comp in colors:
        if colors[comp] in col:
            ax.bar(x, y, width=0, color=colors[comp], label=comp)
    ax.legend()

    x = []
    y = []
    if s_ground_truth:
        for key in s_ground_truth:
            z = key[0]
            spin = int(key[1:])
            if z == "x":
                x.append(spin - dx)
            else:
                x.append(spin + dx)
            y.append(s_ground_truth[key])
        ax.plot(x, y, "ro", markerfacecolor="none")

    plt.tight_layout()

    # Save the figure
    if output_path:
        plt.savefig(output_path)


def plot_corr_2d(
    x,
    y,
    weights,
    res,
    p_dp,
    n_bin,
    order,
    mix,
    xlabel_arr,
    ylabel_arr,
    plot_all_points=False,
    par_ground_truth=None,
    title=None,
    colors=None,
    out_path=None,
):
    """Plot Corr 2D.

    Plot 2D correlation data and fits.

    Parameters
    ----------
    x : array(double)
        input x value
    y : array(m) of double
        input y arrays
    weights  : array of double, optional, default=None
        weights of x points
    res : class lmfit.MinimizerResult
        results of the minization
    n_bin : double, optional, default=30
        number of points onto which data are binned
    p_dp : dict
        Best-fit and std of input parameter
    order : str
        order of fit
    mix : bool
        mixing of components if ``True``
    xlabel_arr, ylabel_arr : list of str
        x-and y-axis labels
    plot_all_points : bool, optional
        plot all individual data points if ``True``; default is ``False``
    par_ground_truth : 2D np.array, optional
        ground truth model values (y1, y2) for plotting, default is ``None``
    title : string, optional, default=''
        plot title
    colors : array(m) of string, optional, default=None
        line colors
    out_path : str, optional, default=None
        output file path, if not given, plot is not saved to file

    """
    if colors is None:
        prop_cycle = plt.rcParams["axes.prop_cycle"]
        colors = prop_cycle.by_key()["color"]

    # Compute binned data for pretty plotting.
    x_bin, y_bin, err_bin = compute_bins_func_2d(
        x, y, n_bin, mix, weights=weights
    )

    # Initialise mosaic figure
    figure_mosaic = """
    AB
    CD
    """
    fig, axes = plt.subplot_mosaic(mosaic=figure_mosaic, figsize=(15, 15))

    # Get best-fit model on 2D binned grid
    y_model_all = np.zeros(shape=(2, n_bin, n_bin))
    y_model_all[0], y_model_all[1] = leakage.func_bias_2d_full(
        res.params, x_bin[0], x_bin[1], order=order, mix=mix
    )

    if par_ground_truth:
        y_gt_all = np.zeros(shape=(2, n_bin, n_bin))
        y_gt_mean = np.zeros(shape=(2, n_bin))
        y_gt_all[0], y_gt_all[1] = leakage.func_bias_2d_full(
            par_ground_truth, x_bin[0], x_bin[1], order=order, mix=mix
        )

    # Compute means and standard deviations
    y_model_mean = np.zeros(shape=(2, n_bin))
    y_model_upper = np.zeros(shape=(2, n_bin))
    y_model_lower = np.zeros(shape=(2, n_bin))
    for comp, ax in zip((0, 1), (1, 0)):
        y_model_mean[comp] = y_model_all[comp].mean(axis=ax)
        std = y_model_all[comp].std(axis=ax)
        y_model_upper[comp] = y_model_mean[comp] + std
        y_model_lower[comp] = y_model_mean[comp] - std

        if par_ground_truth:
            y_gt_mean[comp] = y_gt_all[comp].mean(axis=ax)

    # Set up quantities to plot in each panel
    xb = {}
    yd = {}
    ym = {}
    ymu = {}
    yml = {}
    xgt = {}
    ygt = {}
    dy = {}
    col = {}
    xl = {}
    yl = {}
    yall = {}
    xall = {}

    # Set component for each panel.
    # x: 0 in A, B; 1 in C, D
    # y: 0 in A, C; 1 in B, D
    panel_comp_x = {}
    panel_comp_y = {}
    for p in "A", "B":
        panel_comp_x[p] = 0
    for p in "C", "D":
        panel_comp_x[p] = 1
    for p in "A", "C":
        panel_comp_y[p] = 0
    for p in "B", "D":
        panel_comp_y[p] = 1

    # Assign quantities to plot with corresponding components
    for p in axes:
        xb[p] = x_bin[panel_comp_x[p]]
        xl[p] = xlabel_arr[panel_comp_x[p]]

        ym[p] = y_model_mean[panel_comp_y[p]]
        ymu[p] = y_model_upper[panel_comp_y[p]]
        yml[p] = y_model_lower[panel_comp_y[p]]
        yl[p] = ylabel_arr[panel_comp_y[p]]
        yd[p] = y_bin[panel_comp_y[p]][panel_comp_x[p]]
        dy[p] = err_bin[panel_comp_y[p]][panel_comp_x[p]]
        col[p] = colors[panel_comp_y[p]]

        if par_ground_truth:
            xgt[p] = x_bin[panel_comp_x[p]]
            ygt[p] = y_gt_mean[panel_comp_y[p]]

        if plot_all_points:
            xall[p] = x[panel_comp_x[p]]
            yall[p] = y[panel_comp_y[p]]

    # Set plot labels to parameter best-fit + std
    label = set_labels(p_dp, order, mix, par_ground_truth=par_ground_truth)

    # Loop over panels
    for p in axes:
        # No off-diagonal plots if no mixing
        if not mix and p in ["B", "C"]:
            continue

        # Plot best-fit mean and mean +/- std
        axes[p].plot(xb[p], ym[p], c=col[p], label=label[p])
        axes[p].fill_between(
            xb[p], ymu[p], yml[p], color=col[p], interpolate=True, alpha=0.3
        )

        # Plot ground-truth binned mean if provided
        if par_ground_truth:
            axes[p].plot(xgt[p], ygt[p], ":", c=col[p])

        if plot_all_points:
            axes[p].plot(xall[p], yall[p], ".", c="k", markersize=0.4)

        # Plot binned data with error bars
        axes[p].errorbar(xb[p], yd[p], yerr=dy[p], c=col[p], fmt=".")

        # Set labels
        axes[p].set_xlabel(xl[p])
        axes[p].set_ylabel(yl[p])
        axes[p].legend()

    # Finish figure
    fig.suptitle(title)
    plt.tight_layout()

    # Save figure
    if out_path:
        plt.savefig(f"{out_path}.png", bbox_inches="tight")
