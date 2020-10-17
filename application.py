from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

from main import process_file

from time import sleep
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'uploads'

executor = ThreadPoolExecutor(2)

@app.route('/')
def index():
    return render_template('index.html', data_visualization='', audio_url='')

@app.route('/', methods=['POST'])
def upload_file():
    # DISCLAIMER: uploading a file in a local server setting does not really make sense.
    # What this does now is that it copies the provided file to the output directory -- only really, REALLY slowly.
    # This should probably change.
    # No time for that within this hackathon, though. Oops, sorry! :)
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        filepath = os.path.join(app.config['UPLOAD_PATH'], uploaded_file.filename)
        out_dir = app.config['UPLOAD_PATH']
        uploaded_file.save(filepath)
        out_filepath = process_file(filepath, out_dir)
        with open(out_filepath, 'r') as out_file:
            viz = out_file.read()
        return render_template('index.html',
                               data_visualization=viz,
                               audio_url=f'/uploads/{uploaded_file.filename}')
    else:
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

# The code below could be useful if we'd want to use an asynchronous process in the background and AJAX to poll the
# results. Not for this hackathon, though!
#
# @app.route('/get-result')
# def get_result():
#     if not executor.futures.done('calc_power'):
#         return jsonify({'status': executor.futures._state('calc_power')})
#     future = executor.futures.pop('calc_power')
#     return jsonify({'status': done, 'result': future.result()})