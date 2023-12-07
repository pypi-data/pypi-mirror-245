import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import griddata

def heatmap(data=None, x=None, y=None, z=None, resolution=300, aspect_ratio=1,
            cmap='jet', ax=None, show_points=True, colorbar=True, cbar_width=0.03,
            cbar_pad=0.01, xlabel=None, ylabel=None, zlabel=None, zlabel_inside=False,
            title=None, vmin=None, vmax=None, imshow_kwargs=None, scatter_kwargs=None):
    """
    Creates a two-dimensional color-coded "heat map" plot on a matplotlib axis from a pandas DataFrame. The API is
    designed to mimic seaborn functions.

    Parameters
    ----------
    data: pandas.Dataframe
        A pandas DataFrame object containing the data for x, y and z parameters.
    x: str
        The name of the column in the 'data' Dataframe containing the x values
    y: str
        The name of the column in the 'data' Dataframe containing the y values
    resolution: int, optional.
        Number of interpolation points in x and y. Defaults to 300.
    aspect_ratio: float, optional
        Aspect ratio of the imshow plot. Defaults to 1.
    cmap: str or matplotlib.colors.Colormap, optional
        The colormap to use for the imshow plot and colorbar. Defaults to 'jet'.
    ax: matplotlib Axes, optional
        Axes object to draw the plot onto, otherwise uses the current Axes.
    show_points: bool, optional
        Specifies whether to show the actual datapoints using a scatterplot.
        Defaults to True.
    colorbar: bool, optional
        Specifiees whether to show a colorbar. Defaults to True.
    cbar_width: float, optional
        Width of the colorbar in axes coordinates. Defaults to 0.03.
    cbar_pad: float, optional
        Space between plot and colorbar. Defualts to 0.01.
    xlabel: str, optional
        Label to show on the x-axis. Defaults to the value of 'x'.
    ylabel: str, optional
        Label to show on the y-axis. Defaults to the value of 'y'.
    zlabel: str, optional
        Label to show on the z-axis. Defaults to the value of 'z'.
    zlabel_inside: bool, optional
        If True, puts the z-label inside the colorbar. If False, puts the zlabel
        outside the colorbar.
    title: str, optional
        Title of the plot. Defualts to None.
    vmin: float, optional
        Defines the minimum of the datarange in the plot. Defaults to the minimum
        of 'z' values.
    vmax: float, optional
        Defines the maximum of the datarange in the plot. Defaults to the maximum
        of 'z' values.
    imshow_kwargs: dict, optional
        Keyword arguments to pass the the imshow function responsible for plotting the
        colorplot. Default values will be overwritten.
    scatter_kwargs: dict, optional
        Keyword arguments to pass the the scatter function responsible for plotting the
        datapoints. Default values will be overwritten.

    Returns
    -------
    ax: matplotlib Axes
        The Axes object containing the plot.
    """

    if data is None:
        raise ValueError('No data specified')
    if x is None:
        raise ValueError('No x value specified')
    if y is None:
        raise ValueError('No y value specified')
    if z is None:
        raise ValueError('No z value specified')

    if xlabel is None:
        xlabel = x
    if ylabel is None:
        ylabel = y
    if zlabel is None:
        zlabel = z

    default_imshow_kwargs = dict()
    default_scatter_kwargs = dict(edgecolor='k', facecolor='w', clip_on=True,
                                  marker='o', s=50, zorder=2)
    if imshow_kwargs is None:
        imshow_kwargs = dict()
    if scatter_kwargs is None:
        scatter_kwargs = dict()
    imshow_kwargs = {**default_imshow_kwargs, **imshow_kwargs}
    scatter_kwargs = {**default_scatter_kwargs, **scatter_kwargs}

    points = data[[x, y]].values
    values = data[z].values
    xmin = points[:, 0].min()
    xmax = points[:, 0].max()
    ymin = points[:, 1].min()
    ymax = points[:, 1].max()
    dx = (xmax - xmin) / (resolution - 1)
    dy = (ymax - ymin) / (resolution - 1)
    grid_x, grid_y = np.mgrid[xmin:xmax:resolution * 1j,
                     ymin:ymax:resolution * 1j]
    z_interp = griddata(points, values, (grid_x, grid_y), method='cubic').T
    extent = (xmin - dx / 2, xmax + dx / 2, ymin - dy / 2, ymax + dy / 2)
    aspect_correction = (xmax - xmin) / (ymax - ymin)
    aspect = aspect_correction * aspect_ratio

    if ax:
        fig = ax.get_figure()
    else:
        fig, ax = plt.subplots()
    im = ax.imshow(z_interp, origin='lower', extent=extent, aspect=aspect,
                   cmap=cmap, vmin=vmin, vmax=vmax, **imshow_kwargs)
    ax.set_xticks(data[x].unique())
    ax.set_yticks(data[y].unique())
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    if show_points:
        ax.scatter(points[:, 0], points[:, 1], **scatter_kwargs)
    if colorbar:
        cax = fig.add_axes([ax.get_position().x1 + cbar_pad, ax.get_position().y0,
                            cbar_width, ax.get_position().height])
        plt.colorbar(im, cax=cax, label=zlabel if not zlabel_inside else None)
        if zlabel_inside:
            cax.text(0.5, 0.5, zlabel, transform=cax.transAxes, rotation=90, va='center', ha='center')
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)

    return ax
