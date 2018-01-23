from flask import Flask, request

app = Flask(__name__)

@app.route('/ABC',methods=['POST','GET'])
def testflask():
  parameter = request.values
  print(parameter['test'])
  if request.method == 'POST':
     return 'POST METHOD'
  return 'NoService'  

if __name__ == '__main__':
  app.run(debug = True, host='0.0.0.0', port = 6011)  
  
  
  
