# Hiwamari 8 clone Images Tool

This tool integrates the satellite image download method officially provided by the [Himawari satellite](http://quicklooks.cr.chiba-u.ac.jp/~himawari_movie/rd_gridded.html). It filters the required latitude and longitude, and downloads the images in batches.

## Features

- Integrates with the Himawari satellite image download service.
- Allows filtering by specific latitude and longitude coordinates.
- Downloads images in batches to manage large data sets efficiently.

## Requirements

- Python 3.6
- ext.01 file (Conversion count value into tbb)  The convert program is available from count2tbb_v101.tgz

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/Alanlee0323/Internal_wave_detection.git
    cd Clone_Hiwamari_Images
    ```
## Usage

1. Run the script to start downloading images:
    ```bash
    python HIwamari_get.py
    ```

### Adjusting Latitude and Longitude

The latitude and longitude adjustments are made within the `process_data` function in the script. Specifically, you need to modify the following variables:

- `start_row`: The starting row index in the data grid. This corresponds to latitude.
- `end_row`: The ending row index in the data grid. This also corresponds to latitude.
- `start_column`: The starting column index in the data grid. This corresponds to longitude.
- `end_column`: The ending column index in the data grid. This also corresponds to longitude.

These adjustments allow you to specify the precise geographical area for data extraction. It's essential to understand the relationship between row and column indices and latitude and longitude coordinates in the data grid.

### Byte Conversion Explanation

The byte conversion process is integral to the script, particularly in the `read_data_range` function. Here's a brief explanation of the byte conversion process:

- The satellite data is stored in a binary format, where each data point (e.g., temperature, humidity) is represented by a certain number of bytes.
- The `read_data_range` function reads the binary data from the satellite files and extracts the relevant data points based on the specified row and column indices.
- The byte conversion process involves reading the bytes corresponding to the selected data points and converting them into a human-readable format (e.g., floating-point numbers representing temperature values).
- By understanding the byte conversion process, you can interpret the extracted data accurately and effectively.

Below are two illustrations to help you understand the latitude and longitude adjustments and the byte conversion process:

**Latitude and Longitude Adjustments:**
![Latitude and Longitude Adjustments](https://github.com/Alanlee0323/Internal_wave_detection/assets/95911604/66bfdbe6-4510-4347-a936-f3a144c359e4/latitude_longitude_adjustments.png)

**Byte Conversion Process:**

See the bands and sampling gradations from [Himawari satellite](http://quicklooks.cr.chiba-u.ac.jp/~himawari_movie/rd_gridded.html) 

These illustrations visually demonstrate how to adjust latitude and longitude indices and the byte conversion process, aiding in your understanding of the script's functionality.


## Contribution

Feel free to fork this repository, make changes, and submit pull requests. Contributions are always welcome.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Thanks to the Himawari satellite team for providing the satellite images.
- This tool utilizes the download methods provided at [Himawari Quick Looks](http://quicklooks.cr.chiba-u.ac.jp/~himawari_movie/rd_gridded.html).
