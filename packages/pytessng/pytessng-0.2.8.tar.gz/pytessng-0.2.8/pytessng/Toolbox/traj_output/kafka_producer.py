import json
import threading
from kafka import KafkaProducer


class KafkaMessageProducer:
    def __init__(self, bootstrap_servers, topic):
        self.producer = KafkaProducer(
            bootstrap_servers = bootstrap_servers,
            api_version = (0, 10),
            max_request_size = 20 * 1024 * 1024,
            acks = 0,  # 不等待确认
            max_in_flight_requests_per_connection=100,  # 控制最大同时未确认的请求
        )
        self.topic = topic

    def send_message(self, message):
        try:
            self.producer.send(self.topic, json.dumps(message).encode('utf-8'))
            print(f"消息发送成功.")
        except Exception as e:
            print(f"发送消息时发生错误：{e}")

    def close(self):
        self.producer.close()


def kafka_send_message_thread(producer, message):
    producer.send_message(message)


# 使用线程去发送，防止阻塞主进程
def kafka_send_message(producer, message):
    thread = threading.Thread(target=kafka_send_message_thread, args=(producer, message))
    thread.start()