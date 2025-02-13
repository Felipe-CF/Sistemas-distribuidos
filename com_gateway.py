import os
import base64
import requests
from io import BytesIO
from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file
from flask_restx import Api, Resource, fields
import xml.etree.ElementTree as ET  # Importe a biblioteca para manipulação de XML


app = Flask(__name__)

# adição em todas as rotas do gateway da permissão de origem e dos métodos do cliente
CORS(app, resources={
    r"/*": {
        "origins": "http://localhost:5500",
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


@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())


@api.route("/upload")
class Upload(Resource):

    @api.doc('Faz o upload de um arquivo')
    @api.expect(file_upload_model)  # Especifica o modelo que a requisição espera
    def post(self):
        
        load_dotenv("C:\\Users\\FelipeCF\\Desktop\\Codigos\\Sistemas-distribuidos\\.env")

        url = os.getenv("UPLOAD_SOAP_URL")
        
        print(f"📡 Enviando requisição para: {url}")

        if 'file' not in request.files:
            return jsonify({"message": "nenhum arquivo"}), 400

        file = request.files['file'] # Extrai o  arquivo do FormData

        file_name = request.form.get('filename') # Extrai o nome do arquivo do FormData

        print(file)

        print(file_name)

        if not file_name:
            file_name = file.filename # Usa o nome do arquivo enviado pelo cliente

        file_content = base64.b64encode(file.read()).decode('utf-8')

        print('aqui')

        xml_request = f"""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
        <s:Body>
            <UploadArquivo xmlns="http://tempuri.org/">
            <nomeArquivo>{file_name}</nomeArquivo>
            <conteudoArquivo>{file_content}</conteudoArquivo> 
            </UploadArquivo>
        </s:Body>
        </s:Envelope>
        """

        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": os.getenv("UPLOAD_SOAP_ACTION")
        }

        response = requests.post(url=url, headers=headers, data=xml_request)

        print(response.content)

        # print('aqui')
        # return jsonify({"message": "Arquivo enviado com sucesso!"}), 200



@api.route("/download")
class Download(Resource):
    @api.doc('Baixa um arquivo')
    def get(self):
        file_name = request.args.get('fileName')  # Obtém o nome do arquivo da query string

        if not file_name:
            return jsonify({"message": "Nome do arquivo não informado"}), 400

        # Formata a requisição SOAP para o serviço de download
        xml_request = f"""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
        <s:Body>
            <DownloadArquivo xmlns="http://tempuri.org/">
                <nomeArquivo>{file_name}</nomeArquivo>
            </DownloadArquivo>
        </s:Body>
        </s:Envelope>
        """

        # Configura os headers para a requisição SOAP
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": os.getenv("DOWNLOAD_SOAP_ACTION")  # Ação SOAP para o download
        }

        # Envia a requisição para o serviço SOAP
        url = os.getenv("DOWNLOAD_SOAP_URL")
        response = requests.post(url=url, headers=headers, data=xml_request)

        # Verifica se a requisição foi bem-sucedida
        if response.status_code != 200:
            return jsonify({"message": "Erro ao buscar arquivo na API SOAP"}), 500

        # Analisa o XML de resposta
        try:
            # Remove namespaces para facilitar a análise
            namespaces = {
                's': 'http://schemas.xmlsoap.org/soap/envelope/',
                '': 'http://tempuri.org/'  # Namespace padrão do serviço SOAP
            }

            # Converte o conteúdo da resposta em um objeto XML
            root = ET.fromstring(response.content)

            # Extrai o conteúdo de <DownloadArquivoResult>
            download_result = root.find(
                './/DownloadArquivoResult',
                namespaces
            )

            if download_result is None:
                return jsonify({"message": "Tag <DownloadArquivoResult> não encontrada na resposta"}), 500

            # Converte o conteúdo de <DownloadArquivoResult> de base64 para bytes
            file_content = base64.b64decode(download_result.text)

        except Exception as e:
            return jsonify({"message": f"Erro ao processar a resposta SOAP: {str(e)}"}), 500

        # Retorna o arquivo para o cliente
        return send_file(
            BytesIO(file_content),  # Conteúdo binário do arquivo
            as_attachment=True,    # Força o download
            download_name=file_name,  # Nome do arquivo
            mimetype='application/octet-stream'  # Tipo MIME genérico para arquivos binários
        )



@api.route("/delete", methods=["DELETE"])
class Delete(Resource):
    @api.doc('Deleta um arquivo')
    def delete(self):
        file_name = request.get_json().get('fileName')

        if not file_name:
            return jsonify({"message": "Nome do arquivo não informado"}), 400

        xml_request = f"""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
        <s:Body>
            <DeleteArquivo xmlns="http://tempuri.org/">
                <nomeArquivo>{file_name}</nomeArquivo>
            </DeleteArquivo>
        </s:Body>
        </s:Envelope>
        """

        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": os.getenv("DELETE_SOAP_ACTION")
        }

        url = os.getenv("DELETE_SOAP_URL")

        response = requests.post(url=url, headers=headers, data=xml_request)

        if response.status_code != 200:
            return jsonify({"message": "Erro ao deletar arquivo na API SOAP"}), 500

        return jsonify({
            "message": f"Arquivo {file_name} deletado com sucesso",
        }), 200


    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
