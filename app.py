from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.exceptions import RequestEntityTooLarge
import pandas as pd
import numpy as np
import os
import io
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_filter_mask(df, filter_type):
    """Get filter mask based on filter type"""
    if filter_type == 'NJ600':
        # NJ600: filter 180992, 180993, 181011-181068
        mask = (
            (df['service_number'] == 180992) |
            (df['service_number'] == 180993) |
            ((df['service_number'] >= 181011) & (df['service_number'] <= 181068))
        )
    elif filter_type == 'PHL':
        # PHL: filter 250001-250029, 250032-250049, 250990-250999
        mask = (
            ((df['service_number'] >= 250001) & (df['service_number'] <= 250029)) |
            ((df['service_number'] >= 250032) & (df['service_number'] <= 250049)) |
            ((df['service_number'] >= 250990) & (df['service_number'] <= 250999))
        )
    elif filter_type == 'BOS+PVD':
        # BOS+PVD: filter specific service numbers
        bos_pvd_numbers = [
            390001, 390002, 390003, 390005, 390006, 390008, 390009, 390010,
            390012, 390013, 390014, 390015, 390016, 390018, 390019, 390022,
            390025, 390026, 390029, 390030, 390036, 390038, 390991, 390994,
            390995, 390998, 390061, 390063, 390064, 390066, 390070, 390071,
            390073, 390074, 390075
        ]
        mask = df['service_number'].isin(bos_pvd_numbers)
    elif filter_type == 'BDL(CT)':
        # BDL(CT): filter 181070-181099
        mask = ((df['service_number'] >= 181070) & (df['service_number'] <= 181099))
    else:
        raise ValueError(f"Unknown filter type: {filter_type}")
    
    return mask

def filter_excel_data(file_path, filter_type='NJ600'):
    """Filter Excel data based on service_number criteria"""
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        # Get filter mask based on filter type
        mask = get_filter_mask(df, filter_type)
        filtered_df = df[mask].copy()
        
        # Extract column B "tno" from filtered data for display
        tno_column = filtered_df['tno']
        
        # Create output DataFrame with filter name for display
        display_df = pd.DataFrame({
            filter_type: tno_column.values
        })
        
        # Replace NaN values with None for JSON serialization
        # Convert to dict first, then clean NaN values
        data_dict = display_df.to_dict('records')
        full_data_dict = filtered_df.to_dict('records')
        
        # Clean any NaN/NaT values that aren't JSON serializable
        def clean_dict(d):
            """Recursively clean NaN, NaT, and other non-JSON-serializable values"""
            if isinstance(d, dict):
                return {k: clean_dict(v) for k, v in d.items()}
            elif isinstance(d, list):
                return [clean_dict(item) for item in d]
            elif d is None:
                return None
            elif isinstance(d, float):
                # Check for NaN
                if np.isnan(d):
                    return None
                return d
            else:
                # Try to check if it's a pandas NA value
                try:
                    if pd.isna(d):
                        return None
                except (TypeError, ValueError):
                    pass
                # Handle datetime objects
                if hasattr(d, 'isoformat'):
                    return d.isoformat()
                return d
        
        # Clean the dictionaries
        data_dict = clean_dict(data_dict)
        full_data_dict = clean_dict(full_data_dict)
        
        # Calculate unique tno count (Actual Quantity)
        unique_tno_count = filtered_df['tno'].nunique()
        
        # Store full filtered data as JSON-serializable format
        result = {
            'total_rows': len(filtered_df),
            'unique_tno_count': int(unique_tno_count),  # Actual Quantity - unique tno count
            'data': data_dict,  # Only tno for display
            'full_data': full_data_dict,  # All columns for download
            'filter_type': filter_type,
            'success': True
        }
        
        return result
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    return jsonify({'success': False, 'error': 'File is too large. Maximum file size is 100MB.'}), 413

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        filter_type = request.form.get('filter_type', 'NJ600')  # Default to NJ600
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process the file with the specified filter type
            result = filter_excel_data(file_path, filter_type)
            
            # Clean up uploaded file
            try:
                os.remove(file_path)
            except:
                pass
            
            return jsonify(result)
        else:
            return jsonify({'success': False, 'error': 'Invalid file type. Please upload .xlsx or .xls file'}), 400
    except Exception as e:
        # Ensure we always return JSON, even on unexpected errors
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500

@app.route('/download', methods=['POST'])
def download_file():
    """Download filtered data as Excel file with all columns"""
    try:
        data = request.get_json()
        if not data or 'full_data' not in data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Create DataFrame from the full filtered data (all columns)
        df = pd.DataFrame(data['full_data'])
        
        # Define the column order as shown in the image
        column_order = [
            'order_id',
            'tno',
            'warehouse',
            'state',
            'reference',
            'sub_reference',
            'bag_no',
            'internal_account_number',
            'service_number',
            'consignee',
            'address',
            'city',
            '190_pathtime',
            '199_pathtime'
        ]
        
        # Reorder columns - only include columns that exist in the DataFrame
        existing_columns = [col for col in column_order if col in df.columns]
        # Add any remaining columns that weren't in the specified order
        remaining_columns = [col for col in df.columns if col not in column_order]
        final_column_order = existing_columns + remaining_columns
        
        # Reorder the DataFrame
        df = df[final_column_order]
        
        # Get filter type and today's date
        filter_type = data.get('filter_type', 'NJ600')
        today = datetime.now()
        date_str = today.strftime('%m/%d/%y')
        
        # Create filename: "FilterType MM/DD/YY.xlsx"
        filename = f'{filter_type} {date_str}.xlsx'
        
        # Create Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Filtered Data')
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

