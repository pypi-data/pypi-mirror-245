from nptyping import NDArray, Int, Shape
from typing import Any
import matplotlib.pyplot as plt
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from scioptim.utils import normalize

default_plot_kwargs = dict(
    fig=None,
    show=False,
    path=None,
    coninuous=False,
    single_points=True,
    marker_dict=None,
    label=None,
    colorbar_label=None,
    additional_hovertemplate=None,
    customdata=None,
    additional_points=None,
)


def plot_xy_point_list(
    points: NDArray[Shape["*, *"], Any],
    **kwargs,
):
    kwargs = {**default_plot_kwargs, **kwargs}

    if kwargs["fig"] is None:
        kwargs["fig"] = go.Figure()
    if kwargs["marker_dict"] is None:
        kwargs["marker_dict"] = {}

    if kwargs["coninuous"]:
        kwargs["fig"].add_trace(
            go.Line(
                x=points[:, 0],
                y=points[:, 1],
            )
        )
    if kwargs["single_points"]:
        default_marker_dict = dict(size=10)
        kwargs["marker_dict"] = {**default_marker_dict, **kwargs["marker_dict"]}

        kwargs["fig"].add_trace(
            go.Scatter(
                x=points[:, 0],
                y=points[:, 1],
                mode="markers",
                marker=kwargs["marker_dict"],
            )
        )
    if kwargs["show"]:
        kwargs["fig"].show()

    return kwargs["fig"]


def plot_xxy_point_list(points: NDArray[Shape["*, *"], Any], plot_3d=True, **kwargs):
    kwargs = {**default_plot_kwargs, **kwargs}

    if kwargs["fig"] is None:
        kwargs["fig"] = go.Figure()
    if kwargs["marker_dict"] is None:
        kwargs["marker_dict"] = {}

    if kwargs["label"] is None:
        kwargs["label"] = ["x1", "x2", "y"]

    if kwargs["colorbar_label"] is None:
        kwargs["colorbar_label"] = [kwargs["label"][2], kwargs["label"][2]]

    if kwargs["additional_hovertemplate"] is None:
        kwargs["additional_hovertemplate"] = ""

    if kwargs["customdata"] is None:
        kwargs["customdata"] = []

    if kwargs["additional_points"] is None:
        kwargs["additional_points"] = {}

    if kwargs["coninuous"]:
        if plot_3d:
            kwargs["fig"].add_trace(
                go.Mesh3d(
                    x=points[:, 0],
                    y=points[:, 1],
                    z=points[:, 2],
                    intensity=kwargs.get("intensity", points[:, 2]),
                    colorscale="Viridis",
                )
            )
        else:
            kwargs["fig"].add_trace(
                go.Contour(
                    x=points[:, 0],
                    y=points[:, 1],
                    z=points[:, 2],
                    colorscale="Viridis",
                )
            )

    if kwargs["single_points"]:
        fig2 = go.Figure()
        kwargs["fig"].layout.coloraxis2 = fig2.layout.coloraxis

        default_marker_dict = dict(
            size=10,
            color=points[:, 2],
            colorscale="inferno",
            line=dict(width=2, color="white"),
        )
        kwargs["marker_dict"] = {**default_marker_dict, **kwargs["marker_dict"]}

        kwargs["marker_dict"]["coloraxis"] = "coloraxis2"

        hovertemplate = f'{kwargs["label"][0]}: %{{x}}<br>{kwargs["label"][1]}: %{{y}}'
        if plot_3d:
            hovertemplate += f'<br>{kwargs["label"][2]}: %{{z}}'
        hovertemplate += kwargs["additional_hovertemplate"]

        if plot_3d:
            fig2.add_trace(
                go.Scatter3d(
                    x=points[:, 0],
                    y=points[:, 1],
                    z=points[:, 2],
                    mode="markers",
                    marker=kwargs["marker_dict"],
                    hovertemplate=hovertemplate,
                    customdata=kwargs["customdata"],
                )
            )
        else:
            fig2.add_trace(
                go.Scatter(
                    x=points[:, 0],
                    y=points[:, 1],
                    mode="markers",
                    marker=kwargs["marker_dict"],
                    hovertemplate=hovertemplate,
                    customdata=kwargs["customdata"],
                )
            )

        kwargs["fig"].add_trace(fig2.data[0])

        kwargs["fig"].layout.coloraxis2.colorbar.x = 1.1
        kwargs["fig"].layout.coloraxis2.colorbar.title = kwargs["colorbar_label"][1]

    kwargs["fig"].layout.coloraxis.colorbar.title = kwargs["colorbar_label"][0]

    kwargs["fig"].layout.scene.xaxis.title.text = kwargs["label"][0]
    kwargs["fig"].layout.scene.yaxis.title.text = kwargs["label"][1]

    for key, data in kwargs["additional_points"].items():
        sf = plot_xxy_point_list(
            data,
            **{
                **kwargs,
                **dict(
                    show=False,
                    plot_3d=plot_3d,
                    additional_points={},
                    single_points=True,
                    coninuous=False,
                ),
            },
        )
        # print(sf)

    if plot_3d:
        kwargs["fig"].layout.scene.zaxis.title.text = kwargs["label"][2]

    if kwargs["show"]:
        kwargs["fig"].show()

    return kwargs["fig"]


def plot_xxxy_point_list(points: NDArray[Shape["*, *"], Any], type=None, **kwargs):
    if type is None:
        type = {"base": "3dscatter"}

    kwargs = {**default_plot_kwargs, **kwargs}

    if kwargs["label"] is None:
        kwargs["label"] = ["x1", "x2", "x3", "y"]
    if kwargs["additional_hovertemplate"] is None:
        kwargs["additional_hovertemplate"] = ""

    if kwargs["marker_dict"] is None:
        kwargs["marker_dict"] = {}

    if kwargs["customdata"] is None:
        kwargs["customdata"] = np.zeros((points.shape[0], 0))

    kwargs["customdata"] = np.hstack(
        (points[:, 3].reshape(-1, 1), kwargs["customdata"])
    )
    kwargs["additional_hovertemplate"] = (
        f'<br>{kwargs["label"][3]}: %{{customdata[0]}}'
        + kwargs.get("additional_hovertemplate", "")
    )

    plotter = None
    if type["base"] == "3dscatter":
        if type.get("detailed") is None:
            type["detailed"] = ["color"]
        kwargs["coninuous"] = False
        kwargs["plot_3d"] = True
        default_marker_dict = dict(opacity=0.8, color=None)
        kwargs["marker_dict"] = {**default_marker_dict, **kwargs.get("marker_dict", {})}

        plotter = lambda points, kwargs: plot_xxy_point_list(points[:, 0:3], **kwargs)

        if "color" in type["detailed"]:
            kwargs["marker_dict"]["color"] = points[:, 3]
            if kwargs["colorbar_label"] is None:
                kwargs["colorbar_label"] = [kwargs.get("label", ["y"])[3]] * 2

        if "size" in type["detailed"]:
            minsize = kwargs.get("minsize", 3)
            maxsize = kwargs.get("maxsize", 20)
            assert (
                maxsize > minsize
            ), f"maxsize ({maxsize}) must be greater than minsize ({minsize})"
            kwargs["marker_dict"]["size"] = (
                normalize(points[:, 3]) * (maxsize - minsize) + minsize
            ).astype(int)

        return plotter(points, kwargs)

    if type["base"] == "3dscroll":
        uniques_3dimensions = np.unique(points[:, 2], axis=0)
        surface_plotter = lambda p, kwargs: plot_xxy_point_list(
            p, **{**kwargs, **dict(coninuous=True, single_points=False, plot_3d=True)}
        )
        point_plotter = lambda p, kwargs: plot_xxy_point_list(
            p, **{**kwargs, **dict(coninuous=False, single_points=True, plot_3d=True)}
        )
        show = kwargs.get("show", False)
        kwargs["show"] = False

        cmax = kwargs.get("cmax", points[:, 3].max())
        cmin = kwargs.get("cmin", points[:, 3].min())
        zmax = points[:, 2].max()
        zmin = points[:, 2].min()
        ymin = points[:, 1].min()
        ymax = points[:, 1].max()
        xmin = points[:, 0].min()
        xmax = points[:, 0].max()

        fig = make_subplots(
            rows=1,
            cols=2,
            subplot_titles=("Data Slice", "Slice plot"),
            specs=[[{"type": "surface"}, {"type": "surface"}]],
        )

        nep = points[points[:, 2] == uniques_3dimensions[0]][:, [0, 1, 3]]
        nep[:, 2] = uniques_3dimensions[0]
        nf = surface_plotter(nep, {**kwargs, **dict(intensity=nep[:, 2].copy())})
        nf.data[0].cmin = cmin
        nf.data[0].cmax = cmax
        fig.add_trace(nf.data[0], row=1, col=1)

        nep = points[points[:, 2] == uniques_3dimensions[0]][:, [0, 1, 3]]
        nf = surface_plotter(nep, {**kwargs, **dict(intensity=nep[:, 2].copy())})
        nf.data[0].cmin = cmin
        nf.data[0].cmax = cmax
        fig.add_trace(nf.data[0], row=1, col=2)

        for key, data in kwargs["additional_points"].items():
            nep = data[:, [0, 1, 2]]
            nf = point_plotter(nep, kwargs)
            fig.add_trace(
                go.Scatter3d(
                    x=nep[:, 0],
                    y=nep[:, 1],
                    z=nep[:, 2],
                    mode="markers",
                    marker=kwargs["marker_dict"],
                    hovertemplate=f'{kwargs["label"][0]}: %{{x}}<br>{kwargs["label"][1]}: %{{y}}<br>{kwargs["label"][2]}: %{{z}}<br>{kwargs["label"][3]}: %{{customdata[0]}}',
                    customdata=data[:, [3]],
                    name=key,
                ),
                row=1,
                col=1,
            )

        frames = []

        for uniques_3dimension in uniques_3dimensions[:]:
            nep = points[points[:, 2] == uniques_3dimension][:, [0, 1, 3]]
            kwargs["intensity"] = nep[:, 2].copy()
            nep[:, 2] = uniques_3dimension
            _nf1 = surface_plotter(nep, kwargs)
            _nf1.data[0].cmin = cmin
            _nf1.data[0].cmax = cmax

            nep = points[points[:, 2] == uniques_3dimension][:, [0, 1, 3]]
            kwargs["intensity"] = nep[:, 2].copy()
            _nf2 = surface_plotter(nep, kwargs)
            _nf2.data[0].cmin = cmin
            _nf2.data[0].cmax = cmax

            frame = dict(
                data=[_nf1.data[0], _nf2.data[0]],
                name=str(uniques_3dimension),
                traces=[0, 1],
            )
            frames.append(frame)

        fig.update(frames=frames)

        def frame_args(duration):
            return {
                "frame": {"duration": duration},
                "mode": "immediate",
                "fromcurrent": True,
                "transition": {"duration": duration, "easing": "linear"},
            }

        sliders = [
            {
                "pad": {"b": 10, "t": 60},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [[f.name], frame_args(0)],
                        "label": f"{float(f.name):.2E}",
                        "method": "animate",
                    }
                    for k, f in enumerate(fig.frames)
                ],
            }
        ]

        fig.update_layout(
            #  title='Slices in volumetric data',
            # width=IMAGE_W,
            # height=IMAGE_H,
            # showlegend=False,
            scene=dict(
                xaxis=dict(range=[xmin, xmax], autorange=False),
                yaxis=dict(range=[ymin, ymax], autorange=False),
                zaxis=dict(range=[zmin, zmax], autorange=False),
                #    aspectratio=dict(x=1, y=1, z=1),
                xaxis_title=kwargs["label"][0],
                yaxis_title=kwargs["label"][1],
                zaxis_title=kwargs["label"][2],
            ),
            scene2=dict(
                xaxis=dict(range=[xmin, xmax], autorange=False),
                yaxis=dict(range=[ymin, ymax], autorange=False),
                zaxis=dict(range=[cmin, cmax], autorange=False),
                #    aspectratio=dict(x=1, y=1, z=1),
                xaxis_title=kwargs["label"][0],
                yaxis_title=kwargs["label"][1],
                zaxis_title=kwargs["label"][3],
            ),
            updatemenus=[
                {
                    "buttons": [
                        {
                            "args": [None, frame_args(50)],
                            "label": "&#9654;",  # play symbol
                            "method": "animate",
                        },
                        {
                            "args": [[None], frame_args(0)],
                            "label": "&#9724;",  # pause symbol
                            "method": "animate",
                        },
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 70},
                    "type": "buttons",
                    "x": 0.1,
                    "y": 0,
                }
            ],
            sliders=sliders,
        )

        if show:
            fig.show()
        return fig

    if plotter is None:
        raise ValueError(f"plotter for type {type} not implemented")

    return plotter(points, kwargs)


# calls one of the three above
def plot_xny_point_list(points: NDArray[Shape["*, *"], Any], *args, **kwargs):
    assert (
        points.ndim == 2
    ), f"points must be 2D List of n points with m x and  1 y values (points.shape = (n, m+1)) but has shape {points.shape}"
    if points.shape[1] == 2:
        return plot_xy_point_list(points, **kwargs)
    elif points.shape[1] == 3:
        return plot_xxy_point_list(points, **kwargs)
    elif points.shape[1] == 4:
        return plot_xxxy_point_list(points, **kwargs)
    else:
        raise NotImplementedError(
            f"plotting for {points.shape[1]}D points not implemented"
        )


def slice_grid(x, axis=0, n=10, return_boarders=False):
    boarders = np.linspace(x[..., axis].min(), x[..., axis].max(), n + 1)
    slices = []
    # unique values on axis
    uniques, indices, inv = np.unique(
        x[..., axis], return_index=True, return_inverse=True
    )
    inv_reshaped = inv.reshape(x.shape[:-1])

    for b in range(n):
        target_indices = np.arange(len(uniques))[
            (uniques >= boarders[b]) & (uniques <= boarders[b + 1])
        ]
        compa = np.isin(inv, target_indices)

        mask = (
            np.moveaxis(compa.reshape(x.shape[:-1]), 1, axis)
            .reshape(x.shape[axis], -1)
            .any(-1)
        )
        subslice = np.take(x, np.arange(x.shape[axis])[mask], axis=axis)
        subslice = np.delete(
            np.stack(
                [subslice[..., d].mean(axis=0) for d in range(subslice.shape[-1])],
                axis=-1,
            ),
            1,
            axis=-1,
        )

        slices.append(subslice)

    returner = [slices]
    if return_boarders:
        returner.append(boarders)
    if len(returner) == 1:
        return returner[0]

    return tuple(returner)


def scinot_if_need(x, **kwargs):
    absx = np.abs(x)
    if absx >= 100 or absx <= 0.01:
        s = np.format_float_scientific(x, **kwargs)
    else:
        s = f"{x:.2f}"
    # if s.endswith('.00'):
    #    s = s[:-1]
    return s


def plot2Dgrid(
    gridpoints: NDArray[Shape["*, 2"], Any],
    show=False,
    path=None,
    figkwargs=None,
    plotkwargs=None,
    closefig=True,
):
    if figkwargs is None:
        figkwargs = {}
    if plotkwargs is None:
        plotkwargs = {
            "linestyle": "-",
        }
    fig = plt.figure(**figkwargs)
    ax = fig.add_subplot(111)
    ax.plot(gridpoints[:, 0], gridpoints[:, 1], **plotkwargs)
    if show:
        # show figure
        plt.show()
    if path is not None:
        plt.savefig(path, dpi=fig.dpi)
    if closefig:
        plt.close()
    return fig


def plot3Dgrid_map(
    gridpoints: NDArray[Shape["*, 3"], Any],
    show=False,
    path=None,
    figkwargs=None,
    plotkwargs=None,
    closefig=True,
):
    if figkwargs is None:
        figkwargs = {}

    fig = plt.figure(**figkwargs)
    ax = fig.add_subplot(111)
    if plotkwargs is None:
        plotkwargs = {}

    mesh = ax.pcolormesh(
        gridpoints[:, :, 0], gridpoints[:, :, 1], gridpoints[:, :, 2], **plotkwargs
    )
    plt.colorbar(mesh)
    if show:
        plt.show()
    if path is not None:
        plt.savefig(path, dpi=fig.dpi)
    if closefig:
        plt.close()
    return fig


def plot3Dgrid_sliced_2D(
    gridpoints: NDArray[Shape["*, 3"], Any],
    n=10,
    axis=0,
    show=False,
    path=None,
    figkwargs=None,
    plotkwargs=None,
    closefig=True,
):
    if figkwargs is None:
        figkwargs = {}

    slices, boarders = slice_grid(gridpoints, axis=axis, n=n, return_boarders=True)

    fig = plt.figure(**figkwargs)
    ax = fig.add_subplot(111)

    for i, subslice in enumerate(slices):
        ax.plot(
            subslice[..., 0],
            subslice[..., 1],
            label=f"{scinot_if_need(boarders[i])}-{scinot_if_need(boarders[i+1])}",
        )

    ax.legend()
    if show:
        plt.show()
    if path is not None:
        plt.savefig(path, dpi=fig.dpi)
    if closefig:
        plt.close()
    return fig


def plot4Dgrid_sliced_3D(
    gridpoints: NDArray[Shape["*, 4"], Any],
    n=10,
    axis=0,
    show=False,
    path=None,
    figkwargs=None,
    plotkwargs=None,
    closefig=True,
):
    if figkwargs is None:
        figkwargs = {}

    slices, boarders = slice_grid(gridpoints, axis=axis, n=n, return_boarders=True)

    # create figure with n subplots, and same number of rows and columns
    cols = int(np.sqrt(n))
    rows = int(np.ceil(n / cols))
    if "figsize" not in figkwargs:
        figkwargs["figsize"] = (cols * 3, rows * 3)

    fig = plt.figure(**figkwargs)
    axes = []
    clims = gridpoints[..., -1].min(), gridpoints[..., -1].max()
    for i, subslice in enumerate(slices):
        axi = fig.add_subplot(rows, cols, i + 1)

        mesh = axi.pcolormesh(
            subslice[:, :, 0], subslice[:, :, 1], subslice[:, :, 2], shading="auto"
        )
        mesh.set_clim(*clims)
        axi.set_title(
            f"{scinot_if_need(boarders[i],precision=2)} to {scinot_if_need(boarders[i+1],precision=2)}"
        )
        axes.append(axi)

    plt.tight_layout()
    fig.colorbar(mesh, ax=axes)
    if show:
        plt.show()
    if path is not None:
        plt.savefig(path, dpi=fig.dpi)
    if closefig:
        plt.close()
    return fig
