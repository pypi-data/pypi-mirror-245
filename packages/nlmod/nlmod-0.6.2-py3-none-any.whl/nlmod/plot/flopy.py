import os
from functools import partial

import flopy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from matplotlib.animation import FFMpegWriter, FuncAnimation
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable

from .plotutil import add_background_map, get_figsize, get_map, title_inside


def _get_figure(ax=None, gwf=None, figsize=None):
    # figure
    if ax is not None:
        f = ax.figure
    else:
        if figsize is None:
            figsize = get_figsize(gwf.modelgrid.extent)
            # try to ensure pixel size is divisible by 2
            figsize = (figsize[0], np.round(figsize[1] / 0.02, 0) * 0.02)

        base = 10 ** int(np.log10(gwf.modelgrid.extent[1] - gwf.modelgrid.extent[0]))
        f, ax = get_map(
            gwf.modelgrid.extent, base=base, figsize=figsize, tight_layout=False
        )
        ax.set_aspect("equal", adjustable="box")
    return f, ax


def map_array(
    arr,
    gwf,
    ilay=0,
    iper=0,
    extent=None,
    ax=None,
    title="",
    xlabel="X [km RD]",
    ylabel="Y [km RD]",
    norm=None,
    vmin=None,
    vmax=None,
    levels=None,
    cmap="viridis",
    alpha=1.0,
    colorbar=True,
    colorbar_label="",
    plot_grid=True,
    add_to_plot=None,
    backgroundmap=False,
    figsize=None,
    animate=False,
):
    # get data
    if isinstance(arr, xr.DataArray):
        arr = arr.values

    # get correct timestep and layer if need be
    if len(arr.shape) == 4:
        arr = arr[iper]
    if len(arr.shape) == 3:
        arr = arr[ilay]

    # get figure
    f, ax = _get_figure(ax=ax, gwf=gwf, figsize=figsize)

    # get normalization if vmin/vmax are passed
    if vmin is not None or vmax is not None:
        norm = Normalize(vmin=vmin, vmax=vmax)

    # get plot obj
    pmv = flopy.plot.PlotMapView(gwf, layer=ilay, ax=ax, extent=extent)

    # plot data
    qm = pmv.plot_array(arr, cmap=cmap, norm=norm, alpha=alpha)

    # bgmap
    if backgroundmap:
        add_background_map(ax, map_provider="nlmaps.water", alpha=0.5)

    # add other info to plot
    if add_to_plot is not None:
        for fplot in add_to_plot:
            fplot(ax)

    if plot_grid:
        pmv.plot_grid(lw=0.25, alpha=0.5)

    # axes properties
    axprops = {"xlabel": xlabel, "ylabel": ylabel, "title": title}
    ax.set(**axprops)

    f.tight_layout()

    # colorbar
    divider = make_axes_locatable(ax)
    if colorbar:
        cax = divider.append_axes("right", size="5%", pad=0.1)
        cbar = f.colorbar(qm, cax=cax)
        if levels is not None:
            cbar.set_ticks(levels)
        cbar.set_label(colorbar_label)

    if animate:
        return f, ax, qm
    else:
        return ax


def animate_map(
    arr,
    times,
    gwf,
    ilay=0,
    extent=None,
    ax=None,
    title="",
    xlabel="X [km RD]",
    ylabel="Y [km RD]",
    datefmt="%Y-%m",
    norm=None,
    vmin=None,
    vmax=None,
    levels=None,
    cmap="viridis",
    alpha=1.0,
    colorbar=True,
    colorbar_label="",
    plot_grid=True,
    add_to_plot=None,
    backgroundmap=False,
    figsize=(9.24, 10.042),
    save=False,
    fname=None,
):
    # get data
    if isinstance(arr, xr.DataArray):
        arr = arr.values

    # get correct layer if need be
    if isinstance(arr, list):
        arr = np.stack(arr)
    if len(arr.shape) == 4 and arr.shape[1] > 1:
        arr = arr[:, ilay]
    elif len(arr.shape) < 3:
        raise ValueError("Array has too few dimensions!")

    # plot base image
    f, ax, qm = map_array(
        arr,
        gwf,
        ilay=ilay,
        iper=0,
        extent=extent,
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        norm=norm,
        vmin=vmin,
        vmax=vmax,
        levels=levels,
        cmap=cmap,
        alpha=alpha,
        colorbar=colorbar,
        colorbar_label=colorbar_label,
        plot_grid=plot_grid,
        add_to_plot=add_to_plot,
        backgroundmap=backgroundmap,
        figsize=figsize,
        animate=True,
    )
    # add updating title
    t = pd.Timestamp(times[0])
    title = title_inside(
        f"Layer {ilay}, t = {t.strftime(datefmt)}",
        ax,
        x=0.025,
        bbox={"facecolor": "w"},
        horizontalalignment="left",
    )

    # write update func
    def update(iper, qm, title):
        # select timestep
        ai = arr[iper]

        # update quadmesh
        qm.set_array(ai.ravel())

        # update title
        t = pd.Timestamp(times[iper])
        title.set_text(f"Layer {ilay}, t = {t.strftime(datefmt)}")

        return qm, title

    # create animation
    anim = FuncAnimation(
        f,
        partial(update, qm=qm, title=title),
        frames=len(times),
        blit=False,
        interval=100,
    )

    # save animation as mp4
    if save:
        writer = FFMpegWriter(
            fps=10,
            bitrate=-1,
            extra_args=["-pix_fmt", "yuv420p"],
            codec="libx264",
        )
        anim.save(fname, writer=writer)

    return f, anim


def facet_plot(
    gwf,
    arr,
    lbl="",
    plot_dim="layer",
    layer=None,
    period=None,
    cmap="viridis",
    scale_cbar=True,
    vmin=None,
    vmax=None,
    norm=None,
    xlim=None,
    ylim=None,
    grid=False,
    figsize=(10, 8),
    plot_bc=None,
    plot_grid=False,
):
    if arr.ndim == 4 and plot_dim == "layer":
        nplots = arr.shape[1]
    elif arr.ndim == 4 and plot_dim == "time":
        nplots = arr.shape[0]
    elif arr.ndim == 3:
        nplots = arr.shape[0]
    else:
        raise ValueError("Array must have at least 3 dimensions.")

    plots_per_row = int(np.ceil(np.sqrt(nplots)))
    plots_per_col = nplots // plots_per_row + 1

    fig, axes = plt.subplots(
        plots_per_col,
        plots_per_row,
        figsize=figsize,
        sharex=True,
        sharey=True,
        constrained_layout=True,
    )

    if scale_cbar:
        vmin = np.nanmin(arr)
        vmax = np.nanmax(arr)

    for i in range(nplots):
        iax = axes.flat[i]
        iax.set_aspect("equal")
        if plot_dim == "layer":
            ilay = i
            iper = period
            if arr.ndim == 4:
                if iper is None:
                    raise ValueError("Pass 'period' to select timestep to plot.")
                a = arr[iper]
        elif plot_dim == "time":
            ilay = layer
            iper = i
            if arr.ndim == 4:
                if ilay is None:
                    raise ValueError("Pass 'layer' to select layer to plot.")
                a = arr[iper]
        else:
            raise ValueError("'plot_dim' must be one of ['layer', 'time']")

        mp = flopy.plot.PlotMapView(model=gwf, layer=ilay, ax=iax)
        qm = mp.plot_array(a, cmap=cmap, vmin=vmin, vmax=vmax, norm=norm)

        mp.plot_ibound(color_vpt="darkgray")

        if plot_grid:
            mp.plot_grid(lw=0.25, color="k")

        if plot_bc is not None:
            for bc, bc_kwargs in plot_bc.items():
                mp.plot_bc(bc, **bc_kwargs)

        iax.grid(grid)
        iax.set_xticklabels([])
        iax.set_yticklabels([])

        if plot_dim == "layer":
            iax.set_title(f"Layer {ilay}", fontsize=6)
        elif plot_dim == "time":
            iax.set_title(f"Timestep {iper}", fontsize=6)

        if xlim is not None:
            iax.set_xlim(xlim)
        if ylim is not None:
            iax.set_ylim(ylim)

    for iax in axes.ravel()[nplots:]:
        iax.set_visible(False)

    cb = fig.colorbar(qm, ax=axes, shrink=1.0)
    cb.set_label(lbl)

    return fig, axes
