FROM python:3.10-slim

WORKDIR /home

RUN apt-get update && \
    apt-get install -y nano vim && \
    apt-get clean

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY  . /home/

EXPOSE 8000

CMD [ "python3" , "main.py"]