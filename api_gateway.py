import os
import pika
import time
import json
import base64
from flask_cors import CORS
from dotenv import load_dotenv
from zeep.exceptions import Fault
from flask_restx import Api, Resource, fields
from flask import Flask, request, jsonify, send_file


app = Flask(__name__)

# variaveis de ambiente carregadas e disponíveis para todos os endpoints da API
load_dotenv("C:\\Users\\FelipeCF\\Desktop\\Codigos\\Sistemas-distribuidos\\.env")

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


# função que cria uma conexão com o rabbitMQ
def queue_message_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    return connection


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

        # mensagem json para ser enviada para a fila            
        json_message ={
            "url_wsdl": os.getenv('CLIENTE_UPLOAD'),
            "service": "upload",
            "file": file_content,
            "file_name": file_name
        }

        # cria a conexão com a fila de mensagem
        connection = queue_message_connection()

        # cria canal de comunicação com a fila
        channel = connection.channel()

        # declaro o rotulo da fila
        channel.queue_declare(queue='gateway')

        # insiro a mensagem na fila
        channel.basic_publish(exchange='', routing_key='gateway', body=json.dumps(json_message))



@api.route("/download")
class Download(Resource):
    @api.doc('Baixa um arquivo')
    def get(self):
        file_name = request.args.get('fileName')  # Obtém o nome do arquivo da query string

        if not file_name:
            return jsonify({"message": "Nome do arquivo não informado"}), 400
        

        # mensagem json para ser enviada para a fila            
        json_message ={
            "url_wsdl": os.getenv('CLIENTE_DOWNLOAD'),
            "service": "download",
            "file": None,
            "file_name": file_name
        }

        # cria a conexão com a fila de mensagem
        connection = queue_message_connection()

        # cria canal de comunicação com a fila
        channel = connection.channel()

        # declaro o rotulo da fila
        channel.queue_declare(queue='gateway')

        # insiro a mensagem na fila
        channel.basic_publish(exchange='', routing_key='gateway', body=json.dumps(json_message))

        file_returned = os.path.join("temp", json_message['file_name'])

        timer = 0

        while not os.path.exists(file_returned):

            time.sleep(1)

            timer += 1

            if timer == 30:
                return "erro ao baixar"
        
        return send_file(file_returned, as_attachment=True)






@api.route("/delete", methods=["DELETE", "OPTIONS"])
class Delete(Resource):
    @api.doc('Deleta um arquivo')
    def delete(self):

        file_name = request.get_json().get('fileName')

        # mensagem json para ser enviada para a fila            
        json_message ={
            "url_wsdl": os.getenv('CLIENTE_DELETE'),
            "service": "delete",
            "file": None,
            "file_name": file_name
        }

        # cria a conexão com a fila de mensagem
        connection = queue_message_connection()

        # cria canal de comunicação com a fila
        channel = connection.channel()

        # declaro o rotulo da fila
        channel.queue_declare(queue='gateway')

        # insiro a mensagem na fila
        channel.basic_publish(exchange='', routing_key='gateway', body=json.dumps(json_message))

    
    def options(self):
        pass
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
