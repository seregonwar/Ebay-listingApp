import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_csv():
    try:
        # Get CSV/XLS data from the frontend
        file_data = request.form.get('fileData')
        if not file_data:
            return jsonify({'error': 'No CSV file provided.'}), 400

        # Parse the file using Pandas
        df = pd.read_excel(file_data)

        # Get column names from the DataFrame
        column_names = df.columns.tolist()

        # Controlla se le colonne richieste sono presenti
        required_columns = ['Action(SiteID=US|Country=US|Currency=USD|Version=941)', 'Category ID', 'Custom Label (SKU)', 'Relationship', 'Relationship details', 'P:UPC', 'Quantity', 'Start Price', 'Item photo URL.', 'P:EAN', 'P:EPID']
        missing_columns = set(required_columns) - set(column_names)
        if missing_columns:
            return jsonify({'error': f'Missing columns: {", ".join(missing_columns)}'}), 400

        # Extract the desired columns
        data = {
            'action': df['Action(SiteID=US|Country=US|Currency=USD|Version=941)'].tolist(),
            'category_id': df['Category ID'].tolist(),
            'custom_label': df['Custom Label (SKU)'].tolist(),
            'relationship': df['Relationship'].tolist(),
            'relationship_details': df['Relationship details'].tolist(),
            'upc': df['P:UPC'].tolist(),
            'quantity': df['Quantity'].tolist(),
            'start_price': df['Start Price'].tolist(),
            'item_photo_url': df['Item photo URL.'].tolist(),
            'ean': df['P:EAN'].tolist(),
            'epid': df['P:EPID'].tolist(),
        }

        # Return the data as JSON
        return jsonify(data), 200

    except FileNotFoundError:
        return jsonify({'error': 'CSV file not found.'}), 404
    except pd.errors.EmptyDataError:
        return jsonify({'error': 'CSV file is empty.'}), 400
    except KeyError as e:
        return jsonify({'error': f'Column not found: {e}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error during parsing: {e}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
