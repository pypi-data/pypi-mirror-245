"""
Metadata about reflectance bands, including band names and wavelengths

"""
import pandas as pd
import numpy as np

class ReflectanceBands:
    """
    A class to store and retrieve information about reflectance bands, including band names, wavelengths, and interoperability with Sentinel-2.

    Attributes:
        bands (dict): A dictionary containing information about different reflectance bands.

    Methods:
        get_band_info(band_number): Get information about a specific reflectance band.
        get_band_wavelength(band_number): Get the wavelength information for a specific reflectance band.
    """

    def __init__(self):
        # Initialize a dictionary to store band information
        self.bands = {
            1: {
                "Name": "Coastal Blue",
                "Wavelength": "443 (20)",
                "Interoperable with Sentinel-2": "Yes - with Sentinel-2 band 1",
            },
            2: {
                "Name": "Blue",
                "Wavelength": "490 (50)",
                "Interoperable with Sentinel-2": "Yes - with Sentinel-2 band 2",
            },
            3: {
                "Name": "Green I",
                "Wavelength": "531 (36)",
                "Interoperable with Sentinel-2": "No equivalent with Sentinel-2",
            },
            4: {
                "Name": "Green",
                "Wavelength": "565 (36)",
                "Interoperable with Sentinel-2": "Yes - with Sentinel-2 band 3",
            },
            5: {
                "Name": "Yellow",
                "Wavelength": "610 (20)",
                "Interoperable with Sentinel-2": "No equivalent with Sentinel-2",
            },
            6: {
                "Name": "Red",
                "Wavelength": "665 (31)",
                "Interoperable with Sentinel-2": "Yes - with Sentinel-2 band 4",
            },
            7: {
                "Name": "Red Edge",
                "Wavelength": "705 (15)",
                "Interoperable with Sentinel-2": "Yes - with Sentinel-2 band 5",
            },
            8: {
                "Name": "NIR",
                "Wavelength": "865 (40)",
                "Interoperable with Sentinel-2": "Yes - with Sentinel-2 band 8a",
            },
        }

    def get_band_info(self, band_number):
        """
        Get information about a specific reflectance band.

        Args:
            band_number (int): The number of the reflectance band (1 to 8).

        Returns:
            dict: A dictionary containing information about the band, including name, wavelength, and interoperability with Sentinel-2.
        """
        return self.bands.get(band_number, {})


    def get_band_wavelength(self, band_number):
        """
        Get the wavelength information for a specific reflectance band.

        Args:
            band_number (int): The number of the reflectance band (1 to 8).

        Returns:
            str: The wavelength information for the specified band.

        Example:
            The following example demonstrates how to use the `get_band_wavelength` method to retrieve the wavelength information for a specific reflectance band:

            .. code-block:: python

                reflectance_bands = ReflectanceBands()
                band_number = 4  # Replace with the desired band number
                wavelength = reflectance_bands.get_band_wavelength(band_number)

                if wavelength:
                    print(f"Wavelength for Band {band_number}: {wavelength}")
                else:
                    print(f"Wavelength information not available for Band {band_number}.")
        """
        band_info = self.get_band_info(band_number)
        return band_info.get("Wavelength", "Not found")

    def get_srf(file_path='spectral_response.txt'):
        """
        Read the content of a text file and create a Pandas DataFrame.

        This function reads the content of a text file located at the specified 'file_path' and creates a Pandas DataFrame from it. The text file should be formatted with comma-separated values (CSV format) for proper conversion to a DataFrame.

        Args:
            file_path (str): The path to the text file to be read.

        Returns:
            pandas.DataFrame or None: A Pandas DataFrame containing the data from the text file. If an error occurs during reading or formatting, it returns None.

        Example:
            The following example demonstrates how to use the `read_text_file_to_dataframe` function to read a text file and create a Pandas DataFrame:

            .. code-block:: python

                file_path = 'your_file.txt'  # Replace with the actual file path
                data_frame = get_srf(file_path)

                if data_frame is not None:
                    # Display the DataFrame
                    print(data_frame)
                else:
                    print("Failed to read the text file.")
        """
        try:
            # Read the text file into a Pandas DataFrame
            df = pd.read_csv(file_path, header=0)
            return df
        except Exception as e:
            print(f"Error: {e}")
            return None


def extract_band_number(band_name, is_8_band=True):
    """
    Extract the band number from a given band name for either 4 bands or 8 bands.

    Parameters:
    - band_name (str): The name of the band.
    - is_8_band (bool, optional): True if working with 8 bands (default), False if working with 4 bands.

    Returns:
    - int: The band number (1 to 8 for 8 bands, 1 to 4 for 4 bands) if a valid band name is provided, or None if the band name is not recognized.

    This function takes a band name as input and returns the corresponding band number. It can work for either a set
    of eight bands (Band 1 to Band 8) or four bands (Blue, Green, Red, Near-infrared). If the input band name is not recognized,
    the function returns None.

    Parameters:
    - band_name (str): The name of the band.
    - is_8_band (bool, optional): True if working with 8 bands (default), False if working with 4 bands.

    Returns:
    - int: The band number (1 to 8 for 8 bands, 1 to 4 for 4 bands) if a valid band name is provided, or None if the band name is not recognized.
    """
    if is_8_band:
        # Define a dictionary for 8 bands
        band_mapping = {
            "Coastal Blue": 1,
            "Blue": 2,
            "Green I": 3,
            "Green": 4,
            "Yellow": 5,
            "Red": 6,
            "Red Edge": 7,
            "Near-infrared": 8,
        }
    else:
        # Define a dictionary for 4 bands
        band_mapping = {"Blue": 1, "Green": 2, "Red": 3, "Near-infrared": 4}

    # Use the dictionary to extract the band number
    return band_mapping.get(band_name)


def check_band_name(band_name, is_8_band=True):
    """
    Check if a given band name is valid based on the number of bands.

    Parameters:
    - band_name (str): The name of the band to be checked.
    - is_8_band (bool, optional): True if working with 8 bands (default), False if working with 4 bands.

    Raises:
    - ValueError: If the provided band name is not valid.

    Example:
    ```python
    # Example usage:
    band_name = "Blue"  # Replace with the band name you want to check
    is_8_band = True  # Set to False if working with 4 bands

    try:
        check_band_name(band_name, is_8_band)
        print(f"'{band_name}' is a valid band name.")
    except ValueError as e:
        print(e)
    ```
    """
    if is_8_band:
        valid_band_names = [
            "Coastal Blue",
            "Blue",
            "Green I",
            "Green",
            "Yellow",
            "Red",
            "Red Edge",
            "Near-infrared",
        ]
    else:
        valid_band_names = ["Blue", "Green", "Red", "Near-infrared"]

    if band_name not in valid_band_names:
        raise ValueError(
            f"Invalid band name: '{band_name}'. Valid band names for {'' if is_8_band else '4 '}bands are: {', '.join(valid_band_names)}"
        )
