import jwt
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)
key = "secretnyanih"

#curl -i -X POST http://127.0.0.1:7007/api/v1/tambah -H 'Content-Type: application/json' -d '{"a":2, "b": 2}'
@app.route("/api/v1/tambah", methods=["POST"])
def tambah():
  encoded = request.json['data']
  print(encoded)
  json = jwt.decode(encoded, key, algorithms="HS256")
  a = json['a']
  b = json['b']
  return jsonify({"result": (float(a) + float(b))}), 200

if __name__ == '__main__':
   app.run(debug = True, port=7007)