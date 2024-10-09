from flask import Flask, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

# Directory where uploaded files will be saved
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # Display the upload form and list of uploaded files
    files = []
    for root, dirs, filenames in os.walk(app.config['UPLOAD_FOLDER']):
        for filename in filenames:
            # Collect relative paths of all files
            relative_path = os.path.relpath(os.path.join(root, filename), app.config['UPLOAD_FOLDER'])
            files.append(relative_path)

    return '''
    <h1>Upload a Folder</h1>
    <form method="POST" enctype="multipart/form-data" action="/upload" multiple>
        <input type="file" name="files" webkitdirectory multiple>
        <input type="submit" value="Upload">
    </form>
    <h2>Uploaded Files</h2>
    <ul>
    ''' + ''.join([f'<li><a href="/download/{file}">{file}</a></li>' for file in files]) + '''
    </ul>
    '''

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return 'No files part'

    files = request.files.getlist('files')
    if not files:
        return 'No selected files'

    for file in files:
        # Print the original filename to debug path structure
        # print(f"Received file: {file.filename}")

        if file.filename:
            # Debug: Check if filename includes folder structure
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            
            # Print path to confirm the subfolder structure is maintained
            # print(f"Saving to: {file_path}")

            # Ensure the directory exists for the file
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Save file to the designated path
            file.save(file_path)

    return redirect(url_for('index'))

@app.route('/download/<path:filename>')
def download_file(filename):
    # Serve the requested file for download, preserving nested directory structure
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
