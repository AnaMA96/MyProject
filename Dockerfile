FROM python:3.8.1

ADD ./ ./

RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install -r requirements.txt

CMD ["python3","redirect.py"]