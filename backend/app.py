import os
from flask import Flask, request, render_template, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
import google.generativeai as genai
from dotenv import load_dotenv
from md2pptx import convert_markdown_to_pptx
from utils import user_input, output_md, save_uploadedfile, display_pdf

load_dotenv()

app = Flask(__name__)
app.secret_key = 'supersecretkey'

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('uploaded_files', filename))
            return redirect(url_for('upload_file'))
    return render_template('upload_file.html')

@app.route('/create_ppt', methods=['GET', 'POST'])
def create_ppt():
    if request.method == 'POST':
        context = request.form['context']
        template = request.files['template']
        template_path = save_uploadedfile(template)
        response = output_md()
        pptx_file = convert_markdown_to_pptx(response, template_path)
        return send_file(pptx_file, as_attachment=True, download_name='presentation.pptx')
    return render_template('create_ppt.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = user_input(prompt)
        session['messages'] = session.get('messages', []) + [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': response}]
    return render_template('chat.html', messages=session.get('messages', []))

@app.route('/view_files', methods=['GET', 'POST'])
def view_files():
    pdf_files = os.listdir('uploaded_files')
    if request.method == 'POST':
        selected_file = request.form['selected_file']
        session['selected_file'] = selected_file
        images = display_pdf(os.path.join('uploaded_files', selected_file))
        session['images'] = images
        return render_template('view_files.html', pdf_files=pdf_files, images=images)
    return render_template('view_files.html', pdf_files=pdf_files)

@app.route('/display_image/<int:image_num>')
def display_image(image_num):
    images = session.get('images')
    if images and 0 <= image_num < len(images):
        return send_file(images[image_num], mimetype='image/png')
    return '', 404

if __name__ == "__main__":
    app.run(debug=True)
