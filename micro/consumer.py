from json.tool import main
from flask import Flask
from flask import request, send_file, jsonify
import os
from kafka import KafkaConsumer  # pip install kafka-python
import json
import time
import threading
import ctypes


"""def Kafka_Comsumer():
    #  Kafka Server
    KAFKA_SERVER = 'kafka.vhil-dev.kpit.com:9092'
    # Kafka Consumer Example
    TOPIC_NAME = 'stla'
    KAFKA_CONSUMER = KafkaConsumer(
        bootstrap_servers=KAFKA_SERVER,
        group_id='stla',#To make sure a message is consumed only once (Refer Kafka consumer groups)
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    tp = TopicPartition(TOPIC_NAME, 0)
    KAFKA_CONSUMER.assign([tp])

    # obtain the last offset value
    KAFKA_CONSUMER.seek_to_end(tp)
    offset = KAFKA_CONSUMER.position(tp)
    check = offset
    KAFKA_CONSUMER.seek(tp, offset-1)
    for message in KAFKA_CONSUMER:
        if check == offset-1:
            break
        else:
            message = message.value
            json_url = os.path.join("data", "data.json")
            with open(json_url, "r+") as file:
                data_json = json.load(file)
                data_json['data'].append(message)
                file.seek(0)
                json.dump(data_json, file, indent=1)
            break

    KAFKA_CONSUMER.close()"""


def Kafka_Comsumer():
    #  Kafka Server
    KAFKA_SERVER = 'kafka.vhil-dev.kpit.com:9092'
    while True:
    # Kafka Consumer Example
        KAFKA_CONSUMER = KafkaConsumer(
            'stla',
            bootstrap_servers=KAFKA_SERVER,
            group_id='stla',#To make sure a message is consumed only once (Refer Kafka consumer groups)
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        for message in KAFKA_CONSUMER:
            message = message.value
            json_url = os.path.join("data.json")
            with open(json_url, "r+") as file:
                data_json = json.load(file)
                data_json['data'].append(message)
                file.seek(0)
                json.dump(data_json, file, indent=1)
        time.sleep(10)


app = Flask(__name__)

# decorator


@app.route("/")
def page():
    text = "Navigate /all to view all records" \
           " navigate /data/build_number to get specific record"

    return text

@app.route("/all")
def view():
    js = os.path.join("data.json")
    data_j = json.load(open(js))
    # render_template is always looking in templates folder
    return jsonify(data_j)


@app.route("/data/<int:build>", methods=['GET'])
def add_year(build):
    js = os.path.join("data.json")
    if request.method == 'GET':
        data_j = json.load(open(js))
        data = data_j['data']
        year = request.view_args['build']
        output_data = [x for x in data if x['build'] == build]

        # render template is always looking in template folder
        return jsonify(output_data)


if __name__ == "__main__":
    t1 = threading.Thread(target=Kafka_Comsumer)
    t1.start()
    app.run(debug=True)
    t1.join()




