import base64
import requests
from flask_cors import CORS
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)
CORS(app)

@app.route("/upload", methods=["POST"])
def upload_arquivo():
    url = "http://127.0.0.1:8001/upload"
    
    print(f"📡 Enviando requisição para: {url}")

    if 'file' not in request.files:
        return jsonify({"message": "nenhum arquivo"}), 400

    file = request.files['file']
    file_content = base64.b64encode(file.read()).decode('utf-8')

    soap_body = f"""
    <FileUploadRequest>
        <FileName>{file.filename}</FileName>
        <FileContent>{file_content}</FileContent>
    </FileUploadRequest>
    """

    headers = {'Content-Type': 'application/xml; charset=utf-8'}

    response = requests.post(url=url, headers=headers, data=soap_body)

    print(f"📡 Status da resposta: {response.status_code}")
    print(f"📡 Corpo da resposta: {response.text}")

    return jsonify({"message": "arquivo foi salvo"}), response.status_code


@app.route("/delete", methods=["DELETE"])
def delete_arquivo():
    
    file_name = request.get_json().get('fileName')

    if not file_name:
        return jsonify({"message": "Nome do arquivo não informado"}), 400

    xml_data = f"""
        <DeleteRequest>
            <FileName>{file_name}</FileName>
        </DeleteRequest>
    """

    url = "http://127.0.0.1:8002/delete"

    # Enviar XML para a API C# usando requests
    headers = {'Content-Type': 'application/xml'}

    response = requests.post(url=url, data=xml_data, headers=headers)


    if response.status_code != 200:
        return jsonify({"message": "Erro ao buscar arquivo na API C#"}), 500
    
    return jsonify({"message": "arquivo deletado"}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
