from fastapi import FastAPI
from automated_cql_generation import cql_from_json_with_entities
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def get_root():
    return "This is the root of the API, please use POST to process an input JSON"

@app.post('/')
def generate_cql(input_json: dict):
    output_cql = cql_from_json_with_entities(input_json)
    return output_cql