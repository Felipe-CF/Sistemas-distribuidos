from flask import Flask
from spyne.protocol.soap import Soap11
from wsgiref.simple_server import make_server
from spyne.server.wsgi import WsgiApplication
from spyne import Application, rpc, ServiceBase, String


class HelloWorldService(ServiceBase):
    @rpc(String, _returns=String)
    def say_hello(ctx, name):
        return f"Olá, {name}! Bem-vindo ao serviço SOAP."


app = Flask(__name__)


soap_app = Application([HelloWorldService], 
                       'soap.example',
                       in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())


wsgi_app = WsgiApplication(soap_app)


@app.route("/soap", methods=["POST"])
def soap_service():
    return wsgi_app

if __name__ == "__main__":
    server = make_server('0.0.0.0', 5003, wsgi_app)
    print("Servidor SOAP rodando na porta 5003...")
    server.serve_forever()
