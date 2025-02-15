using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System;
using System.Text;

class Program
{
    static void Main(string[] args)
    {
        var factory = new ConnectionFactory() { HostName = "localhost" };

        var connection = factory.CreateConnection(); 

        var channel = connection.CreateModel();

        channel.QueueDeclare(queue: "soap_requests", durable: false, exclusive: false, autoDelete: false, arguments: null);

        var consumer = new EventingBasicConsumer(channel);

        consumer.Received += (model, ea) =>
        {
            var body = ea.Body.ToArray();

            var message = Encoding.UTF8.GetString(body);
            
            Console.WriteLine($"Received {message}");

            // Aqui você pode usar Zeep ou outra biblioteca para fazer a chamada SOAP
            // Exemplo: CallSoapService(message);
        };

        channel.BasicConsume(queue: "soap_requests", autoAck: true, consumer: consumer);

        Console.WriteLine(" Press [enter] to exit.");

        Console.ReadLine();
    }
}
