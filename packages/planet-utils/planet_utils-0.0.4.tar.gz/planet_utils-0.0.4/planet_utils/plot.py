"""
Plotting reflectance / true color composite from PlanetScope
"""


import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs

import cartopy.feature as cfeature
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import sys
sys.path.append('../')
sys.path.append('../../')

from planetscope import read

def plot_coast(axes: cartopy.mpl.geoaxes.GeoAxes, color='black', linewidth=2, gridlines_alpha=0.5) -> None:
    """
    Plot natural features and gridlines on a map using Cartopy.

    Parameters
    ----------
    axes : cartopy.mpl.geoaxes.GeoAxes
        The axes object to plot on, typically created with `plt.axes(projection=...)`.

    color : str, optional
        The color for drawing coastlines and gridlines. Default is 'black'.

    linewidth : int, optional
        The linewidth for coastlines and gridlines. Default is 2.

    gridlines_alpha : float, optional
        The alpha (transparency) value for gridlines. Default is 0.5.

    Returns
    -------
    None

    Examples
    --------
    ```python
    # Import necessary libraries and create a GeoAxes object
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

    # Call the plot_coast function to plot coastlines and gridlines
    plot_coast(ax, color='blue', linewidth=1, gridlines_alpha=0.3)

    # Display the plot
    plt.show()
    ```
    """

    countries = cfeature.NaturalEarthFeature(
        scale="10m", category="cultural", name="admin_0_countries", facecolor="none"
    )
    states = cfeature.NaturalEarthFeature(
        scale="10m",
        category="cultural",
        name="admin_1_states_provinces_lines",
        facecolor="none",
    )
    axes.add_feature(countries, edgecolor=color, linewidth=linewidth)
    axes.add_feature(states, edgecolor=color, linewidth=linewidth)
    gl = axes.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        linewidth=2,
        color="gray",
        alpha=gridlines_alpha,
        linestyle="--",
    )
    gl.top_labels = False
    gl.bottom_labels = True
    gl.left_labels = True
    gl.right_labels = False
    gl.xlines = True
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER



def true_color_composite(planet, factor=100):
    """
    Generates and displays a true color composite image using a Planet object.

    This function takes a `Planet` object as input and creates a true color composite image using the provided reflectance data. It applies the RGB composition and masks the image with cloud and shadow information to enhance the visual representation. The resulting image is displayed on a map with coastlines. This function is useful for visualizing PlanetScope data in a true color representation.

    Parameters:
        planet (Planet): A Planet object containing the reflectance data.

        factor (int, optional): A scaling factor to adjust the brightness of the image. Default is 100.

    Returns:
        fig (matplotlib.figure.Figure): The matplotlib figure containing the true color composite image.

    Examples:
    --------
    ```python
    # Import necessary libraries and create a Planet object
    from your_module import Planet  # Replace 'your_module' with the actual module name
    import matplotlib.pyplot as plt

    # Initialize the Planet object with reflectance data
    planet = Planet(reflectance_data)  # Replace 'reflectance_data' with your data

    # Generate and display the true color composite image
    fig = true_color_composite(planet, factor=150)

    # Show the figure
    plt.show()
    ```
    """

    # Generate the true color composite (RGB) and apply the mask
    rgb, _, mask = planet.get_rgb(factor=factor)

    # Create a figure and subplot with PlateCarree projection
    fig, ax = plt.subplots(1, 1, figsize=(10, 5), subplot_kw={"projection": ccrs.PlateCarree()})

    # Plot coastlines on the map
    plot_coast(ax)

    # Display the true color composite with the mask applied
    cont = ax.imshow(rgb * mask, extent=planet.extent)

    # Adjust the layout for better visualization
    plt.tight_layout(pad=1.3)
    plt.title(planet.filename.split('/')[-1].split('.')[0])
    return fig

