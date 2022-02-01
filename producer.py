import requests
import json
from requests.auth import HTTPBasicAuth
import sys
from time import sleep
from json import dumps
from kafka import KafkaProducer


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
    
  """finishDate = endTime.text[:8]
  finishDate = finishDate[:4] + '-' + finishDate[4:6] + '-' + finishDate[6:]
  print(finishDate)
  finishTime = endTime.text[9:15]
  startTime = startTime[:2] + ':' + startTime[2:4] + ':' + startTime[4:] 
  print(startTime)
  finishTime = finishTime[:2] + ':' + finishTime[2:4] + ':' + finishTime[4:] 
  print(finishTime)
  print(int(duration.text)/(1000*3600))
  startDate = sys.argv[3]
  startDate = startDate[:4] + '-' + startDate[4:6] + '-' + startDate[6:]
  print(startDate)"""

  endTime = endTime.text
  endTime = endTime[:4] + '-' + endTime[4:6] + '-' + endTime[6:11] + ':' + endTime[11:13] + ':' + endTime[13:]
  endTime = endTime.replace("T"," ")
    
  startTime = startTime.text
  startTime = startTime[:4] + '-' + startTime[4:6] + '-' + startTime[6:11] + ':' + startTime[11:13] + ':' + startTime[13:]
  startTime = startTime.replace("T"," ")

  print("Start Time is ",startTime)
  print("End Time is ",endTime)
  print("Total Duration is ",int(duration.text)/(1000*3600))
  print("Status is ",status.text)
  print("Pipeline is ",sys.argv[1])
  

  
  #kafkaProducer(sys.argv[1],startTime,finishTime,int(duration.text)/(1000*3600),status.text)



