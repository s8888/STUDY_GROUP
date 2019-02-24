import logging
from flask import Flask, jsonify

global model_loaded
model_loaded = False

app = Flask(__name__)

def app_init():
    global model_loaded
    if not model_loaded:
        app.logger.info('Loading model')
        # TODO
        # do something IO bound simulate loading model 
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
    # TODO
    # do something IO bound
    return jsonify("IO bound task finish!")

@app.route('/cpuTask')
def cpuTask():
    # TODO
    # do something CPU bound
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