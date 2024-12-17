import os
import uuid
from flask import Flask, request, url_for, send_from_directory, render_template

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'pdf', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """ Check if the file type is allowed """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """ Handle file upload and shareable link generation """
    if request.method == 'POST':
        file = request.files['file']
        
        if 'file' not in request.files or file.filename == '':
            return "No file selected. Please upload a file."

        if file and allowed_file(file.filename):
            unique_filename = f"{uuid.uuid4()}-{file.filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            
            # Generate shareable link
            file_link = url_for('uploaded_file', filename=unique_filename, _external=True)
            return f"File uploaded successfully! <br> Shareable link: <a href='{file_link}'>{file_link}</a>"

    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """ Serve the uploaded file """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
