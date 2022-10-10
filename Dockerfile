FROM continuumio/miniconda3:latest
#FROM alpine:3.14

WORKDIR /usr/src/app
RUN apt-get update

COPY requirements.txt ./
#RUN apk add --no-cache python3 py3-pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080/tcp

CMD [ "python", "./init.py" ]
#CMD ["bash"]