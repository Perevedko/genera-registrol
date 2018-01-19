from flask import Flask, request, flash, redirect, url_for, make_response
from werkzeug.utils import secure_filename
import os
import actions
app = Flask(__name__)

UPLOAD_FOLDER = os.getcwd()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'zip'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def return_csv(csv_filename):
    with open(csv_filename, 'r') as f:
        response = make_response(f.read())
        cd = 'attachment; filename=data.csv'
        response.headers['Content-Disposition'] = cd
        response.mimetype = 'text/csv'
        return response

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            zip_file_name = 'data.zip'
            zip_full_filename = os.path.join(app.config['UPLOAD_FOLDER'], zip_file_name)
            file.save(zip_full_filename)
            actions.unzip_file(zip_full_filename)
            actions.process_folder_to_csv(actions.unzip_folder)
            return return_csv(actions.csv_file)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=8080)
