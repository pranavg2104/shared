FROM python:alpine3.7

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "gunicorn" , "-w 4" , "--bind" , "0.0.0.0:5001" , "consumer:app"]


