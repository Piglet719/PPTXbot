import os
from flask import Flask, request, jsonify, session, send_file
from werkzeug.utils import secure_filename
import google.generativeai as genai
from dotenv import load_dotenv
from md2pptx import convert_markdown_to_pptx
from utils import user_input, output_md, save_uploadedfile, display_pdf
from flask_cors import CORS
from io import BytesIO

load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = 'supersecretkey'

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
    context = request.form.get('context')
    template = request.files.get('template')
    if context and template:
        template_path = save_uploadedfile(template)
        response = output_md()  # Assuming output_md takes context as input
        pptx_file = convert_markdown_to_pptx(response, template_path)
        output_path = os.path.join('generated_files', 'presentation.pptx')
        print(output_path)
        with open(output_path, "wb") as f:
            f.write(pptx_file.read())
        session['pptx_file_path'] = output_path  # Store the pptx file path in session
        return jsonify(success=True, message='PPT created successfully')
    return jsonify(success=False, message='Context or template missing')

@app.route('/api/download', methods=['GET'])
def download():
    pptx_file_path = session.get('pptx_file_path')
    if pptx_file_path and os.path.exists(pptx_file_path):
        return send_file(pptx_file_path, as_attachment=True, download_name='presentation.pptx', mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation')
    return jsonify(success=False, message='No file to download')

@app.route('/api/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    if prompt:
        response = user_input(prompt)
        session['messages'] = session.get('messages', []) + [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': response}]
        return jsonify(success=True, messages=session['messages'])
    return jsonify(success=False, message='Prompt missing')

@app.route('/api/view_files', methods=['GET'])
def view_files():
    pdf_files = os.listdir('uploaded_files')
    return jsonify(pdf_files=pdf_files)

@app.route('/api/display_image/<int:image_num>', methods=['GET'])
def display_image(image_num):
    images = session.get('images')
    if images and 0 <= image_num < len(images):
        return send_file(images[image_num], mimetype='image/png')
    return '', 404

if __name__ == "__main__":
    app.run(debug=True)
