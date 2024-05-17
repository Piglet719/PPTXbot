from flask import Flask, request, render_template, send_file, session, jsonify
import boto3
import json
import pdf2image
from PyPDF2 import PdfReader
from md2pptx import convert_markdown_to_pptx
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# AWS setup
region = boto3.Session().region_name
session_boto = boto3.Session(region_name=region)
lambda_client = session_boto.client('lambda')
s3_client = boto3.client('s3')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_ppt', methods=['GET', 'POST'])
def create_ppt():
    prompt_template = """
    Please use Markdown syntax to output detailed presentation content from the provided context. Make sure to provide all the details. \n\n
    Context:\n {context}\n

    Presentation content example:
    # Title
    ## Introduction
    - **Keyword**: Description.
    - **Keyword2**: Description2.
    """

    if request.method == 'POST':
        context = request.form.get('context')
        template = request.files.get('template')
        
        question = prompt_template.format(context=context)

        payload = json.dumps({"question": question, "sessionId": session.get('sessionId', '')})
        result = lambda_client.invoke(
                    FunctionName='InvokeKnowledgeBase',
                    Payload=payload
                )
        result = json.loads(result['Payload'].read().decode("utf-8"))
        answer = result['body']['answer']
        
        # Convert Markdown to PPTX
        pptx_path = convert_markdown_to_pptx(answer, template)
        
        # Read the PPTX file
        pptx_io = BytesIO()
        with open(pptx_path, "rb") as f:
            pptx_io.write(f.read())
        pptx_io.seek(0)
        
        session['sessionId'] = result['body']['sessionId']

        return send_file(pptx_io, as_attachment=True, download_name='presentation.pptx', mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation')

    return render_template('create_ppt.html')

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        bucket = 'knowledgebase-135615144901'
        object_name = 'dataset/' + uploaded_file.filename
        try:
            s3_client.upload_fileobj(uploaded_file, bucket, object_name)
            return jsonify(success=True, message=f'Successfully uploaded to {object_name}')
        except Exception as e:
            return jsonify(success=False, message=f'Upload failed. Error: {str(e)}')

    return render_template('upload_file.html')

@app.route('/view_files', methods=['GET', 'POST'])
def view_files():
    files = s3_client.list_objects_v2(Bucket='knowledgebase-135615144901', Prefix='dataset/')['Contents']
    pdf_files = [file['Key'] for file in files if file['Key'].endswith('.pdf')]

    if request.method == 'POST':
        selected_file = request.form.get('selected_file')
        response = s3_client.get_object(Bucket='knowledgebase-135615144901', Key=selected_file)
        pdf_file = response['Body'].read()
        images = pdf2image.convert_from_bytes(pdf_file)
        images_io = [BytesIO() for _ in images]
        for img, img_io in zip(images, images_io):
            img.save(img_io, format='PNG')
            img_io.seek(0)
        return send_file(images_io[0], mimetype='image/png')

    return render_template('view_files.html', pdf_files=pdf_files)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        payload = json.dumps({"question": prompt, "sessionId": session.get('sessionId', '')})
        result = lambda_client.invoke(
            FunctionName='InvokeKnowledgeBase',
            Payload=payload
        )
        result = json.loads(result['Payload'].read().decode("utf-8"))
        answer = result['body']['answer']
        session['sessionId'] = result['body']['sessionId']
        
        if 'messages' not in session:
            session['messages'] = []
        session['messages'].append({"role": "user", "content": prompt})
        session['messages'].append({"role": "assistant", "content": answer})

        return jsonify(success=True, messages=session['messages'])

    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)
