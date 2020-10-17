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
    audio_url = ''
    viz = ''
    # viz = 'Nothing to see just yet!'
    # audio_url = '/uploads/hybridminds.wav'
    return render_template('index.html', data_visualization=viz, audio_url=audio_url)

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        filepath = os.path.join(app.config['UPLOAD_PATH'], uploaded_file.filename)
        uploaded_file.save(filepath)
        yhat = process_file(filepath)
    return render_template('index.html', data_visualization=yhat, audio_url=f'/uploads/{uploaded_file.filename}')
    # return redirect(url_for('index', viz=str(yhat), audio_url=f'/uploads/{uploaded_file.filename}'))

@app.route('/get-result')
def get_result():
    if not executor.futures.done('calc_power'):
        return jsonify({'status': executor.futures._state('calc_power')})
    future = executor.futures.pop('calc_power')
    return jsonify({'status': done, 'result': future.result()})

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)