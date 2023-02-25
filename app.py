from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "This is  basic  server made from flask!"


@app.route("/GET",methods=['GET'])
def get():
    return "get example"

@app.route("/POST",methods=['POST']) 
def post():
    return jsonify(
        {
            'name' :  request.json['name'],
            'age'  :  request.json['age']
         })

if __name__ == '__main__':
    app.run(debug=True,port=3030)
    