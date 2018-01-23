from flask import Flask, request, jsonify 
import json

app = Flask(__name__)

@app.route('/confirm', methods=['POST'])
def user():
  content = request.get_json(force=True)
  name = content['username']
  password = content['password']
  if(name == 'user' and password == 'pw'):
    return 'Login Success: '+name 
  return 'Access Denied'

if __name__ == "__main__": 
  app.run(debug=True, host='0.0.0.0', port= 6013)



