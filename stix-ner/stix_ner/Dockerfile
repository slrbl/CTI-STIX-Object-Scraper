FROM python:3.13.5

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir /stix_ner
COPY . /stix_ner
WORKDIR /stix_ner
