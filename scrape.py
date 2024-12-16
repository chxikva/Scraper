from bs4 import BeautifulSoup
import pandas as pd


def fetch_tables_from_url(html):
    """
    Parse the HTML content and extract all tables.
    Returns a list of dictionaries containing table content and metadata.
    """
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")

    table_data = []
    for table in tables:
        rows = table.find_all("tr")
        table_data.append({
            "content": table,
            "rows": len(rows)
        })

    return table_data


def extract_table_to_dataframe(table):
    """
    Convert a BeautifulSoup table element into a Pandas DataFrame.
    """
    data = []
    headers = [th.text.strip() for th in table.find_all("th")]
    for row in table.find_all("tr"):
        cells = [td.text.strip() for td in row.find_all("td")]
        if cells:
            data.append(cells)
    return pd.DataFrame(data, columns=headers if headers else None)


def generate_extraction_script(script_path, csv_path, url, table_index):
    """
    Generate a Python script to extract a specific table from a URL.
    """
    script_content = f"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage
url = "{url}"

# Fetch the page content
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table")
    if len(tables) > {table_index}:
        table = tables[{table_index}]
        data = []
        headers = [th.text.strip() for th in table.find_all("th")]
        for row in table.find_all("tr"):
            cells = [td.text.strip() for td in row.find_all("td")]
            if cells:
                data.append(cells)

        # Save to DataFrame
        df = pd.DataFrame(data, columns=headers if headers else None)
        df.to_csv("{csv_path}", index=False)
        print(f"Table data saved to {csv_path}")
    else:
        print("Table not found on the page.")
else:
    print(f"Failed to retrieve the page. Status code: {{response.status_code}}")
"""
    with open(script_path, "w") as file:
        file.write(script_content)
