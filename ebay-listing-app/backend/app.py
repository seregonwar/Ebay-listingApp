import sys
from flask import Flask, request, jsonify
import csv_parser
 


app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_csv():
    """
    Parses a CSV file provided by the frontend and returns the data as JSON.

    Args:
        None

    Returns:
        dict: JSON dictionary containing the parsed data, or an error message.
    """
    try:
        # Get CSV/XLS data from the frontend
        file_data = request.form.get('fileData')
        if not file_data:
            return jsonify({'error': 'No CSV file provided.'}), 400

        # Define the required columns
        required_columns = [
            'Action(SiteID=US|Country=US|Currency=USD|Version=941)',
            'Category ID',
            'Custom Label (SKU)',
            'Relationship',
            'Relationship details',
            'P:UPC',
            'Quantity',
            'Start Price',
            'Item photo URL.',
            'P:EAN',
            'P:EPID',
        ]

        # Parse the CSV data using the csv_parser function
        parsed_data = csv_parser.parse_csv(file_data, required_columns)
        if 'error' in parsed_data:
            return jsonify({'error': parsed_data['error']}), 400

        return jsonify(parsed_data), 200

    except Exception as e:
        return jsonify({'error': f'Error during parsing: {e}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
