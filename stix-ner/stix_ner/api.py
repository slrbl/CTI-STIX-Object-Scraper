# Run the api
# uvicorn api:app --reload

from fastapi import FastAPI
from pydantic import BaseModel
from ner import *

app = FastAPI()

# Define the request body model
class InputText(BaseModel):
    text: str

# Define the response endpoint
@app.post("/ctiner")
def main(input_text: InputText):
    return extract_ner(input_text.text,None)
