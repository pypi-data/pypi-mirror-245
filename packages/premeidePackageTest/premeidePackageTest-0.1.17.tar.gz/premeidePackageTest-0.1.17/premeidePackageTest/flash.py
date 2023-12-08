import os
import matplotlib
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for, Response
from premeidePackageTest.classes.File_gen import File_gen
matplotlib.use('agg')

app = Flask(__name__)

### STATICS (and initializaiton): ###
# If static folder not exist --> create (quick fix)
if not os.path.exists('static'):
    os.makedirs('static')

GENERATED_MD_PATH = 'static/generated-md.md'
GENERATED_PDF_PATH = 'static/generated-pdfs.pdf'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADED_JSON_FILE_DIR = os.path.join(BASE_DIR, 'uploaded_file.json')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # Get uploaded JSON file
    uploaded_file = request.files.get('file')

    # If a file is uploaded, save it or process it
    if uploaded_file:
        # Here, save the file or directly process it
        uploaded_file.save(UPLOADED_JSON_FILE_DIR)  # Example: Save the file

    # Get selected checkboxes
    selected_options = request.form.getlist('checkbox')

    # Check if the uploaded JSON file exists
    if not os.path.exists(UPLOADED_JSON_FILE_DIR):
        return "No uploaded JSON file found. Please upload a file first."

    pdf_path = File_gen.calculate_pdf(
        UPLOADED_JSON_FILE_DIR, GENERATED_PDF_PATH, GENERATED_MD_PATH, selected_options)

    return send_from_directory('.', pdf_path, as_attachment=True)


@app.route('/preview_pdf', methods=['POST'])
def preview_pdf():
    # Get uploaded JSON file
    uploaded_file = request.files.get('file')

    # If a file is uploaded, save it or process it
    if uploaded_file:
        uploaded_file.save(UPLOADED_JSON_FILE_DIR)

    # Get selected checkboxes
    selected_options = request.form.getlist('checkbox')

    # Check if the uploaded JSON file exists
    if not os.path.exists(UPLOADED_JSON_FILE_DIR):
        return "No uploaded JSON file found. Please upload a file first."

    pdf_path = File_gen.calculate_pdf(
        UPLOADED_JSON_FILE_DIR, GENERATED_PDF_PATH, GENERATED_MD_PATH, selected_options)

    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()

    return Response(pdf_data, content_type="application/pdf")
    # return url_for('static', filename='generated_pdf.pdf')


def run_app():
    app.run(port=8000, debug=True)


if __name__ == '__main__':
    run_app()  # Click 'RUN', and go to http://127.0.0.1:8000
