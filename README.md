# Copart Image Scraper

This project is a web scraper built using Python and Selenium to automate the process of extracting images and metadata (title and VIN) from a list of Copart URLs. The extracted images are saved in organized folders based on the title and VIN of each vehicle.

## Features
- Scrapes data (title and VIN) from provided Copart URLs.
- Downloads all images in high-definition from each webpage.
- Automatically organizes the images into directories named after the corresponding vehicle's title and VIN.
- Handles errors gracefully, ensuring smooth execution even if a webpage or image fails to load.

---

## Prerequisites

### 1. Python
Ensure you have Python 3.8 or later installed. You can download it from [Python's official website](https://www.python.org/).

### 2. Required Python Packages
Install the necessary packages using the following command:
```bash
pip install selenium pandas requests openpyxl

