import json
from aio_pika import DeliveryMode, Message, connect, ExchangeType
from aio_pika.abc import AbstractExchange

class RabbitMQ:
    exchanges = {}
    channel = None

    @staticmethod
    async def publish(message_dict: dict, exchange_name: str, routing_key: str):
        message_body = json.dumps(message_dict).encode()
        message = Message(
            message_body,
            delivery_mode=DeliveryMode.PERSISTENT,
        )

        try:
            exchange: AbstractExchange = RabbitMQ.exchanges[exchange_name]
        except KeyError:
            # exchange = await RabbitMQ.declare_exchange(exchange_name)
            raise Exception(f"Exchange {exchange_name} not found")

        # Sending the message
        await exchange.publish(message, routing_key=routing_key)

    @staticmethod
    async def connect(connection_url: str):
        # Creating a connection
        # example url = "amqp://guest:guest@localhost/"
        url = connection_url 
        connection = await connect(url)

        # Creating a channel
        RabbitMQ.channel = await connection.channel()
        await RabbitMQ.channel.set_qos(prefetch_count=1)

    @staticmethod
    async def declare_exchange(exchange_name: str):
        exchange = await RabbitMQ.channel.declare_exchange(
            exchange_name,
            type=ExchangeType.FANOUT,
        )
        # Register exchange
        RabbitMQ.exchanges[exchange_name] = exchange
        return exchange

    @staticmethod
    async def declare_queue_and_bind(queue_name: str, exchange_name: str, app_listener):
        queue = await RabbitMQ.channel.declare_queue(queue_name)
 
        try:
            exchange: AbstractExchange = RabbitMQ.exchanges[exchange_name]
        except KeyError:
            # exchange = await RabbitMQ.declare_exchange(exchange_name)
            raise Exception(f"Exchange {exchange_name} not found")

        # Binding the queue to the exchange
        await queue.bind(exchange)
        await queue.consume(app_listener)
