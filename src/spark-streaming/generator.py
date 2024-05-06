from time import sleep
from datetime import datetime

from numpy import random
from faker import Faker
from kafka import KafkaProducer

faker = Faker()
# здесь укажите IP-адрес вашей машины с запущенной Kafka
producer = KafkaProducer(bootstrap_servers=['kafka:9092'])
while True:
    verbs=['GET', 'POST', 'DELETE', 'PUT']
    ualist=[faker.firefox, faker.chrome, faker.safari, faker.internet_explorer, faker.opera]

    ip = str(faker.ipv4())
    dt = str(datetime.now())
    verb = str(random.choice(verbs, p=[0.6,0.1,0.1,0.2]))
    uri = str(faker.uri())
    ua = str(random.choice(ualist, p=[0.5,0.3,0.1,0.05,0.05])())

    # формируем строку
    line = f'{ip}|{dt}|{verb}|{uri}|{ua}'
    # отправляем ее в качестве сообщения в топик logs
    # необходимо отправлять строку в бинарном виде
    producer.send('logs', line.encode('utf-8'))
    # ждем случайное количество секунд от 1 до 3
    sleep(random.uniform(1, 3))
