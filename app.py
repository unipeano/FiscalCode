"""
Italian Fiscal Code Calculator - Modern Web Application
A Flask-based web app with a modern, minimal design.
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
from fiscalcode import FiscalCodeGenerator, parse_date
import json

app = Flask(__name__)


@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate():
    """API endpoint to generate fiscal code."""
    try:
        data = request.json
        
        # Extract data
        surname = data.get('surname', '').strip()
        name = data.get('name', '').strip()
        date_str = data.get('birthDate', '').strip()
        gender = data.get('gender', 'M').upper()
        municipality = data.get('municipality', '').strip()
        
        # Validate
        if not surname or not name:
            return jsonify({'error': 'Surname and name are required'}), 400
        
        if not date_str:
            return jsonify({'error': 'Date of birth is required'}), 400
        
        if not municipality:
            return jsonify({'error': 'Municipality code is required'}), 400
        
        if len(municipality) != 4:
            return jsonify({'error': 'Municipality code must be 4 characters'}), 400
        
        # Parse date
        try:
            birth_date = parse_date(date_str)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        # Generate code
        fiscal_code = FiscalCodeGenerator.generate(
            surname, name, birth_date, gender, municipality
        )
        
        # Prepare response
        response = {
            'fiscalCode': fiscal_code,
            'breakdown': {
                'surname': fiscal_code[0:3],
                'name': fiscal_code[3:6],
                'year': fiscal_code[6:8],
                'month': fiscal_code[8],
                'day': fiscal_code[9:11],
                'municipality': fiscal_code[11:15],
                'checkDigit': fiscal_code[15]
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/demo', methods=['GET'])
def demo_data():
    """Get demo data for preview."""
    return jsonify({
        'surname': 'Rossi',
        'name': 'Mario',
        'birthDate': '01/01/1980',
        'gender': 'M',
        'municipality': 'H501'
    })


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
