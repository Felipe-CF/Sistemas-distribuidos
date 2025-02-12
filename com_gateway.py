import os
import base64
import requests
from io import BytesIO
from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file
from flask_restx import Api, Resource, fields


app = Flask(__name__)
CORS(app, resources={r"/upload": {"origins": "http://localhost:5500"}})

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

# @api.route("/download")
# class Download(Resource):
#     @api.doc('Baixa um arquivo')
#     def get(self):
#         file_name = request.args.get('fileName')

#         if not file_name:
#             return jsonify({"message": "Nome do arquivo não informado"}), 400

#         xml_data = f"""
#             <DownloadRequest>
#                 <FileName>{file_name}</FileName>
#             </DownloadRequest>
#         """

#         url = "http://127.0.0.1:8002/download"
#         headers = {'Content-Type': 'application/xml'}

#         response = requests.post(url=url, data=xml_data, headers=headers)

#         if response.status_code != 200:
#             return jsonify({"message": "Erro ao buscar arquivo na API C#"}), 500

#         file_content = response.content

#         return send_file(
#             BytesIO(file_content),
#             as_attachment=True,
#             download_name=file_name
#         )

# @api.route("/delete")
# class Delete(Resource):
#     @api.doc('Deleta um arquivo')
#     def delete(self):
#         file_name = request.get_json().get('fileName')

#         if not file_name:
#             return jsonify({"message": "Nome do arquivo não informado"}), 400

#         xml_data = f"""
#             <DeleteRequest>
#                 <FileName>{file_name}</FileName>
#             </DeleteRequest>
#         """

#         url = "http://127.0.0.1:8002/delete"
#         headers = {'Content-Type': 'application/xml'}

#         response = requests.post(url=url, data=xml_data, headers=headers)

#         if response.status_code != 200:
#             return jsonify({"message": "Erro ao buscar arquivo na API C#"}), 500

#         return jsonify({
#             "message": "arquivo deletado",
#             "links": [
#                 {"rel": "self", "href": "http://127.0.0.1:8000/delete", "method": "DELETE"},
#                 {"rel": "download", "href": "http://127.0.0.1:8000/download?fileName=exemplo.png", "method": "GET"},
#                 {"rel": "upload", "href": "http://127.0.0.1:8000/upload", "method": "POST"},
#             ]
#         }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
