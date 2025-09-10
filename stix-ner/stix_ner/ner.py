# NER logic here
import langextract as lx
import json
import argparse
import sys
import configparser
import requests
from utils import *






def pull_model(model_name,url):
    response = requests.post('{}/api/pull'.format(url), json={"name": model_name}, stream=True)
    if response.status_code == 200:
        print(f"Pulling model: {model_name}")
        for line in response.iter_lines():
            if line:
                print(line.decode('utf-8'))
        print("Model pulled successfully.")
    else:
        print(f"Failed to pull model: {response.status_code}")
        print(response.text)


def extract_ner(input_text,entity):

    # Initialize the parser
    config = configparser.ConfigParser()
    
    # Read the config file
    config.read('config.ini')

    # Pull model
    print("............................. Model pull started")
    pull_model(config['LLM']['model'],config['LLM']['url'])
    print("............................. Model pull end")

    # Extraction prompt
    prompt_description=config['PROMPT']['description']
    extractions=[]
    lables=eval(json.loads(config['PROMPT']['labels']))
    for entity_class in lables:
        extractions.append(
            lx.data.Extraction(extraction_class=entity_class, extraction_text=lables[entity_class])
        )
    examples = [
        lx.data.ExampleData(
            text=config['PROMPT']['example'],
            extractions=extractions
        )
    ]

    # Run the extraction
    result = lx.extract(
        text_or_documents=input_text,
        prompt_description=prompt_description,
        examples=examples,
        language_model_type=lx.inference.OllamaLanguageModel,
        model_id=config['LLM']['model'],               
        model_url=config['LLM']['url'], 
        debug=False
    )

    if entity!=None:
        findings=[]
        for ext in result.extractions:
            if ext.char_interval!=None:
                if ext.extraction_class==entity.lower():
                    findings.append(ext.extraction_text)
    else:
        findings={}
        for ext in result.extractions:
            if ext.char_interval!=None:
                if ext.extraction_class in findings:
                    findings[ext.extraction_class].append(ext.extraction_text)
                else:
                    findings[ext.extraction_class]=[ext.extraction_text]
    return findings


def extract_label(data_entry,entity):
    extracted_names=[]
    for label in data_entry['labels']:
        if entity.upper() in label:
            extracted_names.append(data_entry['text'][label[0]:label[1]])
    return extracted_names
            

def get_labelled_data(test_json):
    data = []
    with open(test_json, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():  # skip empty lines
                unit=json.loads(line)
                data.append(unit)
    return data



def main():
    

    # Text with a medication mention
    parser = argparse.ArgumentParser(description="STIX NER main script. You can use it to extract entities or to test performances.")

    # Positional argument
    parser.add_argument("-x","--extract", help="Extract entities from a new text (added it after the -x)")
    parser.add_argument("-e","--entity", help="The entity to extract - All entities will extracted by default")
    parser.add_argument("-t","--test", help="Test performances for a labelled data file (add file path after -t) for a given entity (use -e to define the entity")

    args = parser.parse_args()
    
    entity=args.entity

    placeholder_input_text = "A cybercriminal group known as Ember Fox launched a campaign against an energy sector company by exploiting an unpatched Apache Struts vulnerability (CVE-2017-5638) in a public-facing web server. They deployed Metasploit to gain a reverse shell, then installed NanoCore RAT for persistence and surveillance. Analysts detected the intrusion through unusual outbound traffic to dynamic DNS domains and new registry run keys."

    # Run predict/extract mode 
    if args.extract != None:
        print(extract_ner(args.extract,entity))
        sys.exit(0)

    # Run test mode 
    elif args.test != None:
        if entity==None:
            print('You need to choose an entity: user -e argument')
            sys.exit(1)
        data=get_labelled_data(args.test)
        total=len(data)
        count,correct,FP,TP,TN,FN=0,0,0,0,0,0
        for entry in data:
            try:
                findings=extract_ner(entry['text'],entity)
                count+=1
                print('-'*50)
                print("{}/{}\n".format(count,total))
                print(entry)
            except:
                continue
            extracted_names=extract_label(entry,entity)
            print("Actual {} entities from the labelled data:".format(entity))
            print(extracted_names)
            print("Extracted entities:")
            print(findings)
            if len(findings)>0 and len(extracted_names)>0:
                if all(elem in findings for elem in extracted_names):
                    correct+=1
                    TP+=1
                else:
                    FN+=1
            elif len(findings)>0 and len(extracted_names)==0:
                FP+=1
            elif len(findings)==0 and len(extracted_names)==0:
                TN+=1
                correct+=1
            elif len(findings)==0 and len(extracted_names)>0:
                FN+=1
            print("Correct extraction: {}/{}".format(correct,count))
            print("TP: {}\nFP: {}\nTN: {}\nFN: {}".format(TP,FP,TN,FN))

        metrics=classification_metrics_from_counts(TP, FP, TN, FN)
        print(metrics)

if __name__ == "__main__":
    main()