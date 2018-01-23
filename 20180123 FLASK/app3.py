
from flask import Flask

app = Flask(__name__)


@app.route('/testConfirm/<uuid>', methods=['POST','GET'])
def testfirst(uuid):
  return 'First'



@app.route('/testConfirm', methods=['POST','GET'])
def test():
  return 'Instead?!'





if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port= 80)


