import os
import base64
import requests
from io import BytesIO
from zeep import Client
from flask_cors import CORS
from dotenv import load_dotenv
from zeep.exceptions import Fault
import xml.etree.ElementTree as ET  # Importe a biblioteca para manipulação de XML
from flask_restx import Api, Resource, fields
from flask import Flask, request, jsonify, send_file


# variaveis de ambiente carregadas e disponíveis para todos os endpoints da API
load_dotenv("C:\\Users\\FelipeCF\\Desktop\\Codigos\\Sistemas-distribuidos\\.env")

app = Flask(__name__)

# adição em todas as rotas do gateway da permissão de origem e dos métodos do cliente
CORS(app, resources={
    r"/*": {
        "origins": "http://127.0.0.1:5500",
        "methods": ["GET", "POST", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_cridentials": True
    }
})


# Criando a instância do Swagger (Api do Flask-RESTPlus)
api = Api(app, version='1.0', title='API de Upload', description='Documentação para upload, download e exclusão de arquivos via SOAP')

# Definindo o modelo para o upload de arquivos usando o Swagger
file_upload_model = api.model('FileUploadRequest', {
    'file': fields.String(required=True, description='Arquivo a ser enviado em formato base64'),
})



@api.route("/upload")
class Upload(Resource):

    @api.doc('Faz o upload de um arquivo')
    @api.expect(file_upload_model)  # Especifica o modelo que a requisição espera
    def post(self):

        if 'file' not in request.files:
            return jsonify({"message": "nenhum arquivo"}), 400

        file = request.files['file'] # Extrai o  arquivo do FormData

        file_name = request.form.get('filename') # Extrai o nome do arquivo do FormData

        if not file_name:
            file_name = file.filename # Usa o nome do arquivo enviado pelo cliente

        file_content = base64.b64encode(file.read()).decode('utf-8')

        url_wsdl = os.getenv('CLIENTE_UPLOAD')

        cliente = Client(url_wsdl)

        response = cliente.service.UploadArquivo(file_name, file_content)


@api.route("/download")
class Download(Resource):
    @api.doc('Baixa um arquivo')
    def get(self):
        file_name = request.args.get('fileName')  # Obtém o nome do arquivo da query string

        if not file_name:
            return jsonify({"message": "Nome do arquivo não informado"}), 400
        
        
        url_wsdl = os.getenv('CLIENTE_DOWNLOAD')

        client = Client(url_wsdl)

        file_content = client.service.DownloadArquivo(file_name)

        temp_file = os.path.join(file_name)

        dir = os.path.dirname(os.path.abspath(__file__)) + "//temp"

        temp_file_path = os.path.join(dir, file_name)
        with open(temp_file_path, 'wb') as f:
            f.write(file_content)

        return send_file(temp_file, as_attachment=True)



@api.route("/delete", methods=["DELETE", "OPTIONS"])
class Delete(Resource):
    @api.doc('Deleta um arquivo')
    def delete(self):

        try:
            file_name = request.get_json().get('fileName')

            if not file_name:
                return jsonify({"message": "Nome do arquivo não informado"}), 400

            url_wsdl = os.getenv('CLIENTE_DELETE')

            client = Client(url_wsdl)

            response = client.service.DeleteArquivo(file_name)

        except Fault as fault:
            return jsonify({ "message": "erro ao deletar"}), 500
    
    def options(self):
        pass

    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
