import logging
from flask import Flask, jsonify
import time

global model_loaded
model_loaded = False

app = Flask(__name__)

def app_init():
    global model_loaded
    if not model_loaded:
        app.logger.info('Loading model')
        time.sleep(2)
        app.logger.info('Model loaded !!!')
        model_loaded = True

@app.route('/')
def index():
    app.logger.debug('this is a DEBUG message')
    app.logger.info('this is an INFO message')
    app.logger.warning('this is a WARNING message')
    app.logger.error('this is an ERROR message')
    app.logger.critical('this is a CRITICAL message')
    return jsonify('hello world')

@app.route('/ioTask')
def ioTask():
    time.sleep(2)
    return jsonify("IO bound task finish!")

@app.route('/cpuTask')
def cpuTask():
    for i in range(10000000):
        n = i*i*i
    return jsonify("CPU bound task finish!")

@app.route('/model')
def model():
    app.logger.info('model_loaded: ' + str(model_loaded) + ' !!!')
    return jsonify('model_loaded: ' + str(model_loaded) + ' !!!')

if __name__ == '__main__':
    app_init()
    app.run()
    
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app_init()