FROM python:2.7.13

ADD . .
# ADD requirements.txt /

RUN pip install -r "requirements.txt"

CMD [ "python", "./start.py"]