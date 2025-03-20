from flask import Flask, request, jsonify
import os
from urllib.parse import quote

app = Flask(__name__)

@app.route('/')
def home():
    return "Middleware API is running!"

@app.route('/process', methods=['POST'])
def process_files():
    data = request.json

    # Extract URLs and encode them
    file_1 = data.get("file_1", "")
    file_2 = data.get("file_2", "")

    encoded_file_1 = quote(file_1, safe=":/")
    encoded_file_2 = quote(file_2, safe=":/")

    # Extract filenames for easier identification
    filename_1 = os.path.basename(encoded_file_1)
    filename_2 = os.path.basename(encoded_file_2)

    # Identify which file is ProCare and which is FrankCrum
    if "timecard" in filename_1.lower():  # ProCare file
        procare_url = encoded_file_1
        frankcrum_url = encoded_file_2
    else:  # Swap if first file is FrankCrum
        procare_url = encoded_file_2
        frankcrum_url = encoded_file_1

    # Log for debugging
    print(f"Detected ProCare File: {procare_url}")
    print(f"Detected FrankCrum File: {frankcrum_url}")

    return jsonify({
        "message": "Payroll files processed successfully",
        "procare_file": procare_url,
        "frankcrum_file": frankcrum_url
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
