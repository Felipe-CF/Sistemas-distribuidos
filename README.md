# HATEOAS (Hypermedia As The Engine Of Application State)

## O que é?
As respostas da API não apenas retornam dados, mas também fornecem informações sobre ações possíveis ou links relacionados com o estado atual. Isso permite que o cliente descubra, dinamicamente, como interagir com a API através das respostas.


## Como se apresenta aqui?
Ao enviar o arquivo para ser salvo na "nuvem", a api gateway retorna um json com um campo "_links", ele contém informações sobre o endpoint da requisição feita e de outros possíveis passos que podem ser feitos (como deletar e baixar o arquivo)



# Documentação Gateway - Flask-Swagger-UI

## Instalar dependências

```
pip install flask-swagger-ui 
```

## Adicionar ao gateway

```
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # Caminho para o arquivo swagger.json

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Configurações extras do Swagger
        'app_name': "API Gateway"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

```

## Acessar swagger

````
http://localhost:5000/swagger
````


# Servidor SOAP

## Instalar a biblioteca Spyne
````
pip install spyne
````


# XML

## Estrutura 
````
<?xml version="1.0"?>

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:temp="http://exemplo.com/temperatura">
   <soapenv:Header/>

   <soapenv:Body>

      <temp:ConvertCelsiusToFahrenheit>
         <temp:Celsius>30</temp:Celsius>
      </temp:ConvertCelsiusToFahrenheit>
      
   </soapenv:Body>

</soapenv:Envelope>
````

> \<soapenv:Envelope> : Define o início da requisição SOAP.

> \<soapenv:Header>: Pode ser usado para autenticação, mas é opcional.

> \<soapenv:Body>: Contém a requisição real, com o método ConvertCelsiusToFahrenheit.

> \<temp:Celsius>: Parâmetro passado para o serviço.


# XML

## Estrutura 
````
<?xml version="1.0"?>

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:temp="http://exemplo.com/temperatura">
   <soapenv:Header/>

   <soapenv:Body>

      <temp:ConvertCelsiusToFahrenheit>
         <temp:Celsius>30</temp:Celsius>
      </temp:ConvertCelsiusToFahrenheit>
      
   </soapenv:Body>

</soapenv:Envelope>
````

> \<soapenv:Envelope> : Define o início da requisição SOAP.

> \<soapenv:Header>: Pode ser usado para autenticação, mas é opcional.

> \<soapenv:Body>: Contém a requisição real, com o método ConvertCelsiusToFahrenheit.

> \<temp:Celsius>: Parâmetro passado para o serviço.



# API C#

## Estrutura 
````
dotnet new webapi -n XmlApiExample

cd XmlApiExample

dotnet add package Microsoft.AspNetCore.Mvc.Formatters.Xml


````

> \<soapenv:Envelope> : Define o início da requisição SOAP.

> \<soapenv:Header>: Pode ser usado para autenticação, mas é opcional.

> \<soapenv:Body>: Contém a requisição real, com o método ConvertCelsiusToFahrenheit.

> \<temp:Celsius>: Parâmetro passado para o serviço.