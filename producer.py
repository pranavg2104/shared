import requests
import json
from requests.auth import HTTPBasicAuth
import sys
from time import sleep
from json import dumps
from kafka import KafkaProducer

#commit different

def kafkaProducer(feature,start,end,duration,status):

    kafkaServer = 'kafka.vhil-dev.kpit.com:9092'

    producer = KafkaProducer(
        bootstrap_servers=kafkaServer,
        value_serializer=lambda x: dumps(x).encode('utf-8')
    )
    data = {'Feature': feature, 'Build_Status': status , 'Start_Time':start,'End_Time':end,'Total_Duration':duration}
    producer.send('stla_demo', value=data)


if __name__ == "__main__":
  status = requests.get("http://192.168.0.106:8111/app/rest/builds/buildType:"+sys.argv[1]+"/status",auth = HTTPBasicAuth('admin','admin'))
  startTime = requests.get("http://192.168.0.106:8111/app/rest/builds/buildType:"+sys.argv[1]+"/startDate",auth = HTTPBasicAuth('admin','admin'))
  endTime = requests.get("http://192.168.0.106:8111/app/rest/builds/buildType:"+sys.argv[1]+"/finishDate",auth = HTTPBasicAuth('admin','admin'))
  duration = requests.get("http://192.168.0.106:8111/app/rest/builds/buildType:"+sys.argv[1]+"/statistics/BuildDuration",auth = HTTPBasicAuth('admin','admin'))
  feature = sys.argv[2]

  print("Start Time is ",startTime.text)
  print("End Time is ",endTime.text)
  print("Total Duration is ",int(duration.text)/(1000*3600))
  print("Status is ",status.text)
  print("Pipeline is ",sys.argv[1])
  print("Feature is ",sys.argv[2])
  

  
  #kafkaProducer(sys.argv[1],startTime,finishTime,int(duration.text)/(1000*3600),status.text)



