# Excel Filter Web Application

A web-based tool to filter Excel files based on service numbers and display the results.

## Features

- Upload Excel files (.xlsx, .xls)
- Filter data where service_number is:
  - 180992
  - 180993
  - Between 181011 and 181068 (inclusive)
- Display filtered "tno" column values in a table
- Download results as CSV
- Modern, responsive UI with drag-and-drop support

## Requirements

- Python 3.x
- pandas
- openpyxl
- Flask

## Installation

Install the required packages:

```bash
python -m pip install pandas openpyxl flask
```

## Usage

1. Start the web server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Select an Excel file using the file picker or drag and drop

4. Click "Process File" to filter the data

5. View the filtered results in the table

6. Optionally download the results as CSV

## File Structure

- `app.py` - Flask backend server
- `templates/index.html` - Web interface
- `filter_excel.py` - Standalone script version (for command-line use)

