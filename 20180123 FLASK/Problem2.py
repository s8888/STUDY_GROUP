from flask import Flask, request
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/test', methods=['POST','GET'])
def index():
  if request.method == 'POST':
     upfile = request.files['file']
     if upfile and allowed_file(upfile.filename):
         filename = upfile.filename
         upfile.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'],filename ))
         return filename
     return 'Wrong Type of  File '
  return 'Success Connect'

@app.route('/basic', methods=['POST','GET'])
def basictest():
  print(request.form)
  print(request.args)
  print(request.values)
  print(request.headers)
  print(request.files)
  print(request.url)
  
  if request.files:
     upfile = request.files['file']
     return upfile.filename
  return 'error'
  
  

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port = 6012)
 


