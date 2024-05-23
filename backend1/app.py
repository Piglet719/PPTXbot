import os
from flask import Flask, request, jsonify, session, send_file
from werkzeug.utils import secure_filename
import google.generativeai as genai
from dotenv import load_dotenv
from md2pptx import convert_markdown_to_pptx
from utils import user_input, output_md, save_uploadedfile
from flask_cors import CORS
import textwrap

load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploaded_files'

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route('/')
def index():
    return jsonify(message="Welcome to the API")

@app.route('/api/upload_file', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploaded_files', filename))
        return jsonify(success=True, message='File uploaded successfully')
    return jsonify(success=False, message='No file uploaded')

@app.route('/api/create_ppt', methods=['POST'])
def create_ppt():
    templates = os.listdir(UPLOAD_FOLDER)
    print(f'template in uploaded_files directory: {templates}')
    template = [file for file in templates if file.endswith('.pptx')]
    if template:
        # template_path = save_uploadedfile(template)
        response = output_md()
        full_response = ''.join(response['output_text'])
        cleaned_text = textwrap.dedent(full_response).strip()
        pptx_file = convert_markdown_to_pptx(cleaned_text, 'output.pptx', 'C:\\Users\\USER\\Downloads\\test\\test.pptx')
        if pptx_file:
            return send_file(pptx_file, as_attachment=True, download_name='GeneratedPresentation.pptx', mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation')
        else:
            return jsonify(success=False, message='Failed to create PowerPoint presentation')
    return jsonify(success=False, message='No template file provided')

@app.route('/api/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    if prompt:
        response = user_input(prompt)
        session['messages'] = session.get('messages', []) + [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': response}]
        return jsonify(success=True, messages=session['messages'])
    return jsonify(success=False, message='Prompt missing')

@app.route('/api/recent_file', methods=['GET'])
def recent_file():
    files = os.listdir(UPLOAD_FOLDER)
    print(f'Files in uploaded_files directory: {files}')
    pdf_files = [file for file in files if file.endswith('.pdf')]
    if pdf_files:
        recent_file = max(pdf_files, key=lambda x: os.path.getctime(os.path.join(UPLOAD_FOLDER, x)))
        return jsonify(filename=recent_file)
    return jsonify(success=False, message='No recent file found'), 404

@app.route('/api/display_file', methods=['GET'])
def display_file():
    file_name = request.args.get('file')
    if file_name:
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=False, mimetype='application/pdf')
    return jsonify(success=False, message='File not found'), 404

if __name__ == "__main__":
    app.run(debug=True)
