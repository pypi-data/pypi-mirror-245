import json
from adatoolbox.domain.event.adapters.pika_adapter import PikaBaseAdapter


class MqPublisherAdapter(PikaBaseAdapter):
    def publish(
            self,
            queue: str,
            exchange: str,
            routing_key: str,
            body: dict) -> None:
        self.channel.queue_declare(queue=queue)
        self.channel.basic_publish(
                            exchange=exchange,
                            routing_key=routing_key,
                            body=json.dumps(body))
        self.connection.close()
