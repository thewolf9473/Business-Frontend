FROM python:alpine3.7 
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt 
CMD python3 app.py