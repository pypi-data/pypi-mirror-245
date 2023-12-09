"""
Reading reflecntace / DN from PlanetScope
"""

import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from xml.dom import minidom
from skimage.exposure import equalize_hist

import glob
import pandas as pd
import datetime as dt
import os
import datetime
from os.path import exists
from xml.dom import minidom
import sys
import rasterio

sys.path.append('../')
sys.path.append('../../')

from planetscope import bands


class PlanetScope:
    def __init__(self, input_filename):
        """
        Initialize a PlanetScope object.

        Args:
            input_filename (str): The filename of the PlanetScope image file (e.g., ".tif").

        This constructor sets up the object, extracts relevant information from the input filename, and loads
        coefficients and location data from corresponding XML metadata files.
        """
        self.filename = input_filename
        self.xmlfilename = self.parse_xml_filename()
        print(self.xmlfilename)
        self.coeff = self.get_coeffs(self.xmlfilename)
        print('Coeff', self.coeff)
        self.bb = self.get_location(self.xmlfilename)
        print(self.bb)
        self.extent = get_extent(self.bb)
        if len(list(self.coeff.keys()))==8:
             self.is_8_band = True
        else:
             self.is_8_band = False
       

    def parse_xml_filename(self):
        """
        Parse the XML metadata filename based on the input filename.

        Returns:
            str: The XML metadata filename corresponding to the input filename.

        This private method generates the XML metadata filename based on the input filename. If the input filename
        ends with "_clip.tif," it creates a filename for the clipped image, and if it ends with ".tif," it creates
        a filename for the original image.
        """
        output_xmlfilename = glob.glob('_'.join(self.filename.split('_')[:-3])+'*.xml')
        filtered_xmlfiles = [file for file in output_xmlfilename if 'aux' not in file]

        print(filtered_xmlfiles)
        return filtered_xmlfiles[0]

    def parse_metadata(self):
        """
        Parse the XML metadata and return the parsed XML document.

        Returns:
            xml.dom.minidom.Document or None: The parsed XML document or None if the file is not found.

        This method attempts to parse the XML metadata file specified by 'xmlfilename' and returns the parsed XML
        document. If the file is not found, it prints an error message and returns None.
        """
        try:
            xmldoc = minidom.parse(self.xmlfilename)
            # Add your code to process the XML data here
            return xmldoc
        except FileNotFoundError:
            print(f"XML metadata file not found: {self.xmlfilename}")
            return None


    #def get_location(self):
    def get_location(self, is_8_band=True):
    
        """
        Extract geographic location information from a Planet Labs XML metadata files.

        Parameters:
        - xml_filename (str or Document): The path to the XML file or the parsed XML Document object.

        Returns:
        - pandas.DataFrame: A DataFrame containing the geographic coordinates for the four corners of the image.

        This function parses a Planet Labs XML metadata file to extract geographic location information for the top-left (TL), top-right (TR),
        bottom-left (BL), and bottom-right (BR) corners of the image. The coordinates are stored in a DataFrame with columns 'lon' and 'lat'
        and indexed by corner names (TL, TR, BL, BR).

        Parameters:
        - xml_filename (str or Document): The path to the XML file or the parsed XML Document object.

        Returns:
        - pandas.DataFrame: A DataFrame containing geographic coordinates for the image corners.

        The 'xml_filename' parameter can be either a path to the XML file or a pre-parsed Document object. If it's a path to the file,
        the function will parse the XML file using minidom.

        The XML file is expected to have 'ps:geographicLocation' nodes for each corner of the image. The function extracts longitude and latitude
        coordinates for each corner and stores them in a DataFrame for easy access and analysis.
        """
        # Check if the input is a Document object or a file path, and parse the XML accordingly
        xml_filename = (
            xml_filename if type(self.xmlfilename).__name__ == "Document" else minidom.parse(self.xmlfilename)
        )

        # Extract 'ps:geographicLocation' nodes from the XML
        location = xml_filename.getElementsByTagName("ps:geographicLocation")

        def extract_element(corner):
            # Extract longitude and latitude coordinates for the specified corner
            return [
                location[0]
                .getElementsByTagName("ps:" + corner)[0]
                .getElementsByTagName("ps:" + loc)[0]
                .firstChild.data
                for loc in np.array(("longitude", "latitude"))
            ]

        corners = {"topLeft", "topRight", "bottomLeft", "bottomRight"}
        bounding_boxes = {}
        for corner in corners:
            lon_lat = extract_element(corner)
            bounding_boxes[corner]= (float(lon_lat[0]), float(lon_lat[1]))
        return bounding_boxes



    def get_coeffs(self, is_8_band=True):
        """
        Extract reflectance coefficients from a Planet Labs XML metadata file.

        Parameters:
        - xml_filename (str or Document): The path to the XML file or the parsed XML Document object.

        Returns:
        - dict: A dictionary containing band-specific reflectance coefficients.

        This function parses a Planet Labs XML metadata file to extract reflectance coefficients for specific bands (Blue, Green,
        Red, and NIR). The coefficients are stored in a dictionary and returned as the result.

        Parameters:
        - xml_filename (str or Document): The path to the XML file or the parsed XML Document object.

        Returns:
        - dict: A dictionary containing band-specific reflectance coefficients.

        The 'xml_filename' parameter can be either a path to the XML file or a pre-parsed Document object. If it's a path to the file,
        the function will parse the XML file using minidom.

        The XML file is expected to have 'ps:bandSpecificMetadata' nodes that contain 'ps:bandNumber' and 'ps:reflectanceCoefficient'
        elements. The function extracts coefficients for bands 1, 2, 3, and 4 and stores them in a dictionary with the band number
        as the key and the coefficient as the value.
        """
        # Check if the input is a Document object or a file path, and parse the XML accordingly
        xml_filename = (
            xml_filename if type(self.xmlfilename).__name__ == "Document" else minidom.parse(self.xmlfilename)
        )

        # Find all 'ps:bandSpecificMetadata' nodes in the XML
        nodes = xml_filename.getElementsByTagName("ps:bandSpecificMetadata")

        # Create a dictionary to store the coefficients for specific bands
        coeffs = {}
        band_numbers = [str(num) for num in range(1, 9)] if is_8_band else [str(num) for num in range(1, 5)]


        # Iterate through the nodes and extract coefficients for bands 1, 2, 3, and 4
        for node in nodes:
            bn = node.getElementsByTagName("ps:bandNumber")[0].firstChild.data
            if bn in band_numbers:
                i = int(bn)
                value = node.getElementsByTagName("ps:reflectanceCoefficient")[0].firstChild.data
                coeffs[i] = float(value)

        return coeffs

    def get_DN(filename):
        """
        Retrieve Digital Number (DN) values for the blue, green, red, and near-infrared (NIR) bands from a raster file.

        This function opens the specified raster file and reads the DN values for the blue, green, red, and NIR bands. DN values are the raw, uncalibrated pixel values recorded by a remote sensing instrument, and they are essential for various image processing and analysis tasks in remote sensing and geospatial applications. These values are typically obtained from satellite or aerial imagery and serve as the basis for deriving more meaningful information such as reflectance, vegetation indices, and land cover classification.

        Args:
            filename (str): The path to the raster file.

        Returns:
            dict: A dictionary containing the DN values for the blue, green, red, and NIR bands, with band names as keys. These arrays can be used for a wide range of geospatial analyses and image processing tasks.

        Example:
            The following example demonstrates how to use the `get_DN` function to retrieve DN values from a raster file:

            .. code-block:: python

                filename = "path/to/your/raster.tif"
                band_values = get_DN(filename)

                # You can now work with the DN values for different bands.
                # For example, to access the DN values for the blue band:
                blue_values = band_values["blue"]

            The resulting `band_values` dictionary will contain DN values for the respective bands.

        Note:
            - This function assumes that the raster file is in a format supported by the rasterio library.
            - The bands are typically ordered as blue (Band 1), green (Band 2), red (Band 3), and NIR (Band 4) in remote sensing data.
        """
        band_values = {}
        with rasterio.open(filename) as src:
            band_values["blue"] = src.read(1)
            band_values["green"] = src.read(2)
            band_values["red"] = src.read(3)
            band_values["nir"] = src.read(4)
        return band_values


    def get_reflectance(planet, factor=5, band='Red'):
        """
        Calculate reflectance values from radiance data in a multi-band image file.

        Parameters:
        - filename (str): The path to the multi-band image file.
        - coeff (list or tuple): Coefficients for each band to convert radiance to reflectance.
        - factor (int, optional): Downsampling factor to reduce image resolution (default is 5).

        Returns:
        - tuple: A tuple containing the calculated reflectance values for Blue, Green, Red, and NIR bands.

        The function opens a multi-band image file, extracts radiance data from specific bands, and calculates reflectance values
        for the Blue, Green, Red, and NIR bands using provided coefficients. The reflectance values are computed at a reduced
        resolution if the downsampling factor is specified.
        """
        if isinstance(planet, PlanetScope):
            planet_obj = planet
        else:
            planet_obj = PlanetScope(planet)

        filename = planet_obj.filename
        coeff = planet_obj.coeff
        is_8_band=planet_obj.is_8_band
        bands.check_band_name(band, is_8_band=is_8_band)

        with rasterio.open(filename) as src:
            # Extract radiance data from the input band and apply the coefficient
            band_number = bands.extract_band_number(band, is_8_band=is_8_band)
            band_radiance = src.read(band_number)[::factor, ::factor] * coeff[band_number]
        return band_radiance

    def get_rgb_equalized_factors(filename, factor=5):
        """
        Get equalized factors for creating a true color composite (RGB) from a raster file.

        This function opens the specified raster file and computes equalized factors for the red, green, and blue bands to create a visually balanced true color composite. The equalized factors ensure that the dynamic range of each band is utilized when plotting the composite.

        Args:
            filename (str): The path to the raster file.
            factor (int, optional): The downsampling factor for the data. Defaults to 5, which reduces the data resolution for performance or visualization.

        Returns:
            tuple: A tuple containing three equalized factors for red, green, and blue bands, respectively.

        Example:
            The following example demonstrates how to use the `get_rgb_equalized_factors` function to obtain equalized factors for creating a true color composite:

            .. code-block:: python

                filename = "path/to/your/raster.tif"
                downsampling_factor = 5
                red_factor, green_factor, blue_factor = get_rgb_equalized_factors(filename, factor=downsampling_factor)

                # You can now use these factors for creating a true color composite.

        Note:
            - This function assumes that the raster file is in a format supported by the rasterio library.

        See Also:
            - Documentation for the rasterio library: https://rasterio.readthedocs.io/en/stable/
        """
        with rasterio.open(filename) as src:
            band_red = src.read(3)[::factor, ::factor]
            band_green = src.read(2)[::factor, ::factor]
            band_blue = src.read(1)[::factor, ::factor]

        # Compute equalized factors for red, green, and blue bands
        red_factor = 1.0 / (band_red.max() - band_red.min())
        green_factor = 1.0 / (band_green.max() - band_green.min())
        blue_factor = 1.0 / (band_blue.max() - band_blue.min())

        return red_factor, green_factor, blue_factor



    def get_rgb(self, factor=5):

        """
        Generate an RGB image from reflectance values obtained from Planet Labs image and metadata.
        
        Args:
        - planet: The Planet Labs image data.
        - factor (optional): A scaling factor for reflectance values. Default is 5.
        
        Returns:
        - Tuple: RGB image, reflectance values for each band (blue, green, red), and a mask.

        This function takes reflectance values for blue, green, and red bands, creates an equalized RGB image,
        stores the reflectance values, and generates a mask based on the blue band reflectance.

        Example:
        ```python
        # Assuming 'planet_data' contains the Planet Labs image and metadata
        # Replace 'get_reflectance' and 'get_mask' with actual functions that fetch reflectance and generate masks

        # Generate RGB image, reflectance values, and mask for the 'planet_data' with default factor (5)
        rgb_image, reflectance_values, mask = get_rgb(planet_data)

        # Print the shape of the RGB image
        print("Shape of RGB image:", rgb_image.shape)

        # Print reflectance values for each band
        print("Reflectance Values - Blue:", reflectance_values['blue'])
        print("Reflectance Values - Green:", reflectance_values['green'])
        print("Reflectance Values - Red:", reflectance_values['red'])

        # Assuming 'save_image' is a function that saves the RGB image
        # Save the RGB image
        save_image(rgb_image, 'output_image.jpg')
        ```
        """

        blue = self.get_reflectance(factor=factor, band='Blue')
        green = self.get_reflectance(factor=factor, band='Green')
        red = self.get_reflectance(factor=factor, band='Red')

        # Create an RGB image by stacking equalized Red, Green, and Blue channels
        rgb = np.stack((equalize(red), equalize(green), equalize(blue)), axis=2)

        # Create a dictionary to store the reflectance values for each band
        reflectance = {"blue": blue, "green": green, "red": red}
        mask = get_mask(reflectance['blue'])
        mask_3d = np.stack((mask, mask, mask), 2)

        # Return a tuple containing the RGB image, reflectance values, and location information
        return rgb, reflectance, mask_3d


def get_mask(input_ref):
        """
        Generate a binary mask based on a reference image, typically representing a Red band.

        Parameters:
        - input_ref (numpy.ndarray): A reference image band, typically representing the Red band, with values.

        Returns:
        - numpy.ndarray: A binary mask image where non-zero values represent valid data, and zeros represent masked areas.

        This function generates a binary mask based on a reference image, which is typically the Red band of an image. The mask
        is created by identifying non-zero values in the reference image and mapping them to 255 (valid data), while zero values
        are mapped to 1 (masked areas). The resulting binary mask is a NumPy array.

        Parameters:
        - input_ref (numpy.ndarray): A reference image band, typically representing the Red band, with values.

        Returns:
        - numpy.ndarray: A binary mask image where non-zero values represent valid data, and zeros represent masked areas.
        """
        # Create an initial binary mask where non-zero values are set to 255 (valid data)
        S1_mask_step0 = ((input_ref == 0) + 0 == 1) + 0
        S1_mask_step0[S1_mask_step0 == 1] = 255

        # Set zero values to 1 to represent masked areas
        S1_mask_step0[S1_mask_step0 == 0] = 1

        # Stack the binary mask into a 3-channel image for RGB representation
        #S1_mask_rgb = np.stack((S1_mask_step0, S1_mask_step0, S1_mask_step0), 2)

        return S1_mask_step0




def get_extent(planet_dict):
    """
    Calculate the extent of the given planet dictionary containing coordinates.

    Args:
    - planet_dict (dict): Dictionary containing coordinates of the planet with keys:
        'topRight', 'topLeft', 'bottomRight', 'bottomLeft', each with (lon, lat) tuples.

    Returns:
    - np.array: Array containing the extent as [lon_start, lon_end, lat_start, lat_end].

    Example:
    >>> planet = {
    ...    'topRight': (-120.4478185853, 35.2788690179),
    ...    'topLeft': (-120.86651114, 35.2788690179),
    ...    'bottomRight': (-120.4478185853, 35.0324055948),
    ...    'bottomLeft': (-120.86651114, 35.0324055948)
    ... }
    >>> extent = get_extent(planet)
    >>> print(extent)
    Output: [-120.86651114 -120.44781859  35.03240559  35.27886902]
    """
    lon_start = min(planet_dict['topRight'][0], planet_dict['topLeft'][0])
    lon_end = max(planet_dict['bottomRight'][0], planet_dict['bottomLeft'][0])
    lat_start = min(planet_dict['topRight'][1], planet_dict['bottomRight'][1])
    lat_end = max(planet_dict['topLeft'][1], planet_dict['bottomLeft'][1])
    
    return np.array([lon_start, lon_end, lat_start, lat_end])


def equalize(band):
        """
        Apply histogram equalization to enhance the contrast of an image band.

        Parameters:
        - band (numpy.ndarray): An image band as a NumPy array with values in the range [0, 1].

        Returns:
        - numpy.ndarray: The equalized image band with enhanced contrast.

        This function takes an image band represented as a NumPy array and enhances its contrast by applying histogram equalization.
        It maps the input values to the range [0, 255], performs histogram equalization, and returns the enhanced band.

        Parameters:
        - band (numpy.ndarray): An image band as a NumPy array with values in the range [0, 1].

        Returns:
        - numpy.ndarray: The equalized image band with enhanced contrast.
        """
        # Map the input values to the range [0, 255] and convert to integers
        band_mapped = np.interp(band, (0, 1), (0, 255)).astype(int)

        # Apply histogram equalization to the mapped band
        equalized_band = equalize_hist(band_mapped)

        # Return the equalized band with enhanced contrast
        return equalized_band