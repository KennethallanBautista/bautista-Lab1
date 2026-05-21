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


File Structure
project-folder/
│
├── extract_starlink_usage.py
├── requirements.txt
├── data_usage.csv
└── your_starlink_page.html
How to Use
Save the Starlink webpage as an .html file in the same folder as the script.
Open a terminal or command prompt in that folder.
Run the script:
python extract_starlink_usage.py
Choose:
a specific file to scrape, or
0 to process all HTML files in the folder
The extracted data will be saved automatically as:
data_usage.csv
Output Format

The CSV file contains:

Date
Data Usage (GB)

Example:

Date,Data Usage (GB)
04/17/2024,12.45
04/18/2024,10.87
04/19/2024,15.02
Notes
The script uses BeautifulSoup to read and parse the HTML content.
It looks for the total usage text and chart bars in the webpage.
If multiple HTML files are processed, duplicate dates are combined automatically.
Make sure the HTML file is closed before running the script to avoid file access issues.
