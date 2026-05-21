# bautista-Lab1


# Starlink Data Usage Web Scraper

This project is a basic web scraping lab that extracts **daily data usage values** from a Starlink usage page saved as an HTML file.  
The script reads the webpage content, detects the usage bars, converts the values into GB, and exports the result into a `.csv` file for data analysis.

## Features

- Reads local Starlink HTML files
- Extracts total data usage
- Detects daily usage bars from the chart
- Automatically maps dates for each bar
- Exports the extracted data into `data_usage.csv`
- Supports processing one file or all HTML files in the folder

## Requirements

Install the required Python package:

```bash
pip install beautifulsoup4
