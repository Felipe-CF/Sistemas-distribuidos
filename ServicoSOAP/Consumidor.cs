using System;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Hosting;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;

public class RabbitMqConsumer : BackgroundService
{
    private readonly string _queueName = "minha_fila"; // Nome da fila que será consumida
    private IConnection _connection;
    private IModel _channel;

    public RabbitMqConsumer()
    {
        var factory = new ConnectionFactory()
        {
            HostName = "rabbitmq", // Usar "rabbitmq" dentro do Docker
            UserName = "guest",
            Password = "guest"
        };


        _connection = factory.CreateConnection();
        _channel = _connection.CreateModel();
        _channel.QueueDeclare(queue: _queueName, durable: true, exclusive: false, autoDelete: false, arguments: null);
    }

    protected override Task ExecuteAsync(CancellationToken stoppingToken)
    {
        var consumer = new EventingBasicConsumer(_channel);
        consumer.Received += (model, ea) =>
        {
            var body = ea.Body.ToArray();
            var message = Encoding.UTF8.GetString(body);
            Console.WriteLine($"[x] Mensagem recebida: {message}");

            // Aqui você pode chamar a API SOAP para processar o XML recebido
        };

        _channel.BasicConsume(queue: _queueName, autoAck: true, consumer: consumer);
        return Task.CompletedTask;
    }

    public override void Dispose()
    {
        _channel?.Close();
        _connection?.Close();
        base.Dispose();
    }
}
