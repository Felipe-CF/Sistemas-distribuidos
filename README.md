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




# API Gateway Integrado com SOAP e RabbitMQ

## Objetivo da Atividade

Este projeto implementa um sistema que integra REST e SOAP utilizando um API Gateway. O fluxo consiste em um cliente web que interage com o gateway, que por sua vez armazena mensagens em uma fila (RabbitMQ). Um consumidor processa essas mensagens e executa operações na API SOAP, que gerencia arquivos.

## Tecnologias Utilizadas

- **Python (Flask)**: Implementação do API Gateway
- **RabbitMQ**: Mensageria para comunicação assíncrona
- **Docker**: Gerenciamento de containers para RabbitMQ
- **C# (SOAP API)**: Implementação do serviço SOAP para manipulação de arquivos
- **JavaScript (Cliente Web)**: Interface web para interação com o sistema

## Estrutura do Projeto

```
/api_gateway
    ├── app.py                  # Implementação do API Gateway com Flask
    ├── requirements.txt         # Dependências do Python
    ├── Dockerfile               # Configuração do ambiente Docker

/soap_service
    ├── Service.svc              # Implementação do serviço SOAP
    ├── Web.config               # Configuração do serviço SOAP
    ├── ...                      # Outros arquivos relacionados ao serviço SOAP

/consumer
    ├── consumer.py              # Script que lê mensagens da fila e processa a requisição SOAP

/client_web
    ├── index.html               # Interface web para enviar requisições
    ├── script.js                # Lógica de comunicação com o API Gateway

/docker
    ├── docker-compose.yml       # Configuração para subir os serviços necessários
```

## Como Instalar e Rodar

### Pré-requisitos

- **Python 3.9+**
- **Docker e Docker Compose**
- **.NET Core** (para o serviço SOAP)

### Passos de Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/seuusuario/seurepositorio.git
   cd seurepositorio
   ```
2. Instale as dependências do API Gateway:
   ```sh
   pip install -r api_gateway/requirements.txt
   ```
3. Suba os containers do RabbitMQ:
   ```sh
   docker-compose up -d
   ```
4. Inicie o API Gateway:
   ```sh
   python api_gateway/app.py
   ```
5. Inicie o consumidor que processa as mensagens:
   ```sh
   python consumer/consumer.py
   ```
6. Inicie o serviço SOAP no ambiente .NET
7. Abra o cliente web (`client_web/index.html`) e interaja com o sistema.

## Funcionamento

1. O **cliente web** envia requisições (upload, download e remoção de arquivos) para o **API Gateway**.
2. O **API Gateway** recebe a requisição e a envia para uma fila RabbitMQ.
3. O **consumidor** monitora a fila, processa a mensagem e chama o **serviço SOAP**.
4. O **serviço SOAP** executa a operação e retorna a resposta ao consumidor.

## Conceitos Aplicados

- **API Gateway**: Centraliza o acesso a diferentes serviços (REST e SOAP)
- **HATEOAS**: Navegação entre recursos REST
- **Mensageria (RabbitMQ)**: Comunicação assíncrona entre processos
- **SOAP**: Serviço baseado em XML para manipulação de arquivos
- **Docker**: Containerização do RabbitMQ

## Exemplo de Requisição

### Envio de Arquivo (POST)

```sh
curl -X POST "http://localhost:5000/upload" -F "file=@arquivo.txt"
```

### Download de Arquivo (GET)

```sh
curl -X GET "http://localhost:5000/download/arquivo.txt"
```

### Deletar Arquivo (DELETE)

```sh
curl -X DELETE "http://localhost:5000/delete/arquivo.txt"
```

## WSDL do Serviço SOAP

O serviço SOAP expõe um arquivo WSDL que descreve as operações disponíveis. Para visualizar o WSDL, acesse:

```
http://localhost:port/Service.svc?wsdl
```

## Conclusão

Este projeto demonstra a integração de arquiteturas REST e SOAP usando um API Gateway, filas de mensagens e processamento assíncrono. Com isso, conseguimos escalabilidade e flexibilidade na comunicação entre serviços heterogêneos.

## Link do Repositório

[GitHub - Seu Repositório](https://github.com/seuusuario/seurepositorio)

