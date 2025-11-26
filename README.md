# Excel Filter Web Application

A web-based tool to filter Excel files based on service numbers and display the results.

## Features

- Upload Excel files (.xlsx / .xls)
- Supports multiple filter types:
  - NJ600
  - PHL
  - BOS+PVD
  - BDL(CT)
- Filters data based on `service_number`
- Displays only `tno` values on screen
- Shows unique `tno` count
- Allows downloading full filtered rows as an Excel file
- Maximum file size: 100MB
- Automatically deletes uploaded files after processing

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

