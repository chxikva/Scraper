# Custom Browser with Table Extraction

A Python-based GUI application to browse web pages and extract HTML tables. This project allows users to extract tables from a web page, save them as CSV files, and even generate Python scripts to automate table extraction for future use.

---

## Features

- Browse any website using a custom-built web browser.
- Automatically detect and list all HTML tables on a web page.
- Export selected tables to CSV format.
- Generate Python scripts for automated table extraction.
- User-friendly GUI built with PyQt5.
- Real-time HTML parsing using BeautifulSoup and Pandas.

---

## Technologies Used

- **Python**: Core programming language.
- **PyQt5**: For building the graphical user interface.
- **BeautifulSoup**: For parsing HTML and extracting tables.
- **Pandas**: For handling and exporting table data.
- **QtWebEngine**: For embedding a browser within the application.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Virtual environment (optional but recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/chxikva/Scraper.git
   cd Scraper
Create a virtual environment (optional):

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Usage
Run the application:

python main.py
Enter a URL in the browser's address bar and press Enter to load the page.

Click "Extract Tables" to parse the page and detect all HTML tables.

Double-click a table from the list to:

Export it as a CSV file.
Generate a Python script for automated extraction.
Generated Python Script Example
When you extract a table, a Python script is also generated. This script can be reused to extract the same table from the specified webpage. Example script:

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://example.com"

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table")
    table = tables[0]  # Replace 0 with the table index you want to extract
    data = []
    headers = [th.text.strip() for th in table.find_all("th")]
    for row in table.find_all("tr"):
        cells = [td.text.strip() for td in row.find_all("td")]
        if cells:
            data.append(cells)

    df = pd.DataFrame(data, columns=headers if headers else None)
    df.to_csv("output.csv", index=False)
    print("Table data saved to output.csv")
else:
    print("Failed to retrieve the page.")


Project Structure

<project-root>/
│
├── scrape.py               # Functions for table extraction and script generation
├── main.py                 # Main application file
├── requirements.txt        # List of dependencies
└── README.md               # Project documentation
Dependencies
All required dependencies are listed in requirements.txt. To install them, run:

pip install -r requirements.txt

Key dependencies include:
PyQt5
beautifulsoup4
pandas
requests
Contributing
Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

License
This project is licensed under the MIT License. See the LICENSE file for details.
