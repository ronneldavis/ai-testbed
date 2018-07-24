from flask import Flask, url_for, send_from_directory, request, render_template
import logging, os
from werkzeug import secure_filename
from test import get_categories
import time

app = Flask(__name__)
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/upload', methods = ['POST'])
def api_root():
    app.logger.info(PROJECT_HOME)
    if request.method == 'POST' and request.files['image']:
    	app.logger.info(app.config['UPLOAD_FOLDER'])
    	img = request.files['image']
    	img_name = secure_filename(img.filename)
    	create_new_folder(app.config['UPLOAD_FOLDER'])
    	saved_path = os.path.join(app.config['UPLOAD_FOLDER'], str(time.time()*100))
    	app.logger.info("saving {}".format(saved_path))
    	img.save(saved_path)
    	json = str(get_categories(saved_path))
        os.remove(saved_path)
        return json
    else:
    	return "Where is the image?"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=8083)