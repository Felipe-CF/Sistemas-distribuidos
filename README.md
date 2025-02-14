# HATEOAS (Hypermedia As The Engine Of Application State)

## Introdução
HATEOAS é um conceito no qual as respostas da API retornam além de dados, fornecem informações sobre as possíveis ações ou links relacionados com o estado atual. Isso permite que o cliente descubra dinamicamente como interagir com a API através das respostas

## Implementação
Ao enviar o arquivo para ser salvo na "nuvem", a API Gateway retorna um JSON contendo um campo ```_links```. Esse campo inclui informações sobre o endpoint da requisição feita e outras possíveis ações, tais como: deletar e baixar arquivos. 

# Documentação da API Gateway com Flask-Swagger-UI

## Instalação das dependências

```
pip install flask-swagger-ui 
```

## Configuração do Swagger no Gateway

```python
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

## Acessando o Swagger

```
http://localhost:5000/swagger
```


# Servidor SOAP

## Instalação a biblioteca Spyne
```
pip install spyne
```


# Exemplo de requisição XML

## Estrutura do XML

```xml
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
```

- ```<soapenv:Envelope>```: define o início da requisição SOAP.
- ```<soapenv:Header>```: pode ser usado para autenticação.
- ```<soapenv:Body>```: contém a requisição real com o método ```ConvertCelsiusToFahrenheit```.
- ```temp:Celsius>```: parâmetro passado para o serviço.

# API C#

## Criação do projeto web API com suporte a XML

```bash 
dotnet new webapi -n XmlApiExample

cd XmlApiExample

dotnet add package Microsoft.AspNetCore.Mvc.Formatters.Xml


```
Agora a API estará pronta para lidar com as requisições e respostas no formato XML.
