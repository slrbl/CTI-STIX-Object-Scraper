# STIX_NER
Named entity recognition for cyber threat intelligence.
The current version uses LLM to extract threat intelligence entities. 

## How does it work

TBD

## Prerequisites

### Ollama
### Using Docker 
Ollama is included in the provided configuration. 

### Using without Docker
You need to install Ollama on your local machine or to set the URL where it is running as service in your config file. 

## Using a Python virtual env
```shell
python -m venv stix_ner
source stix_ner/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Settings file
Copy config.template to config.ini and adjust it according to your needs.
You can also create a new settings file as showed in the following example:
```shell
[LLM]
model:llama3.2      
url:http://127.0.0.1:11434

[PROMPT]
description:"Extract threat intelligence information if they are mentioned including tool, threat actor, attack pattern, sector, country, vulnerability, malware and indicator in the order they appear in the text."
example:"The threat actor group known as Silver Spear targeted the aviation sector in France using a watering hole attack. They exploited a vulnerability in Internet Explorer (CVE-2021-26411) to drop TrickBot. The attackers leveraged the Cobalt Strike tool for lateral movement, and communications were observed with silverspear-c2[.]aero."
labels:"{'threat_actor':'Silver Spear','sector':'aviation','country':'France','attack_pattern':'watering hole','vulnerability':'CVE-2021-26411','malware':'TrickBot','tool':'Cobalt Strike','indicator':'silverspear-c2[.]aero'}"


```

## Usage
### Using the script ner.py

```
python ner.py -h
usage: ner.py [-h] [-x EXTRACT] [-e ENTITY] [-t TEST]

STIX NER main script. You can use it to extract entities or to test performances.

options:
  -h, --help            show this help message and exit
  -x, --extract EXTRACT
                        Extract entities from a new text (added it after the -x)
  -e, --entity ENTITY   The entity to extract - All entities will extracted by default
  -t, --test TEST       Test performances for a labelled data file (add file path after -t) for a given entity (use -e to define the
                        entity
```

This is an example of threat intelligence data extraction from a raw text:
```shell
python ner.py -x "A cybercriminal group known as Ember Fox launched a campaign against an energy sector company by exploiting an unpatched Apache Struts vulnerability (CVE-2017-5638) in a public-facing web server. They deployed Metasploit to gain a reverse shell, then installed NanoCore RAT for persistence and surveillance. Analysts detected the intrusion through unusual outbound traffic to dynamic DNS domains and new registry run keys"
```
This is an example of testing and getting extraction performance:
```shell
python ner.py -e 'MALWARE' -t ../data/annotated/stix_ner_synthetic_reviewed_sample_for_testing.json
```

## Using the API
Launching the API
```shell
uvicorn api:app --reload
```
An example of API usage:
```python
import requests
url = "http://127.0.0.1:8000/ctiner"
data = {"text": "A cybercriminal group known as Ember Fox launched a campaign against an energy sector company by exploiting an unpatched Apache Struts vulnerability (CVE-2017-5638) in a public-facing web server. They deployed Metasploit to gain a reverse shell, then installed NanoCore RAT for persistence and surveillance. Analysts detected the intrusion through unusual outbound traffic to dynamic DNS domains and new registry run keys"}
response = requests.post(url, json=data)
```

## Using Docker
```shell
docker-compose build
docker-compose up
```
Once the docker service is running, you can use it as using the API.

If you are running an API  request for the first time after building the service using ```docker-compose build``` for the first time, then it is expected that the call time more time to pull the defined Ollama model.

## TODO 
Adding the possibility to use a spaCy based NER model\
Putting in place docker container DONE
