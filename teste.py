import base64
from zeep.exceptions import Fault
from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_restx import Resource

app = Flask(__name__)

@app.route("/", methods=["DELETE", "OPTIONS", "GET", "POST"])
class Delete(Resource):
    def teste(self):
        return jsonify({"message": "to ouvindo"}), 200

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
