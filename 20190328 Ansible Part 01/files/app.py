from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/example')
def index():
    if 'name' in request.args:
       name = request.args['name']
       status = 'success'
    else:
       name = 'no name'
       status = 'failed'
    ret = {
      'name': name,
      'status': status
    }
    return jsonify(ret)

if __name__ == '__main__':
    app.run(debug=True)
