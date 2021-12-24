import json
import requests
import codecs

with open('cql/atlas_event_inclusion.cql', 'r') as file:
    input_cql = file.readlines()

cql = ''.join(input_cql)
cql = str(cql.replace('"', '\"'))

full_post_body = {
    "code": cql,
    "dataServiceUri":"https://apps.hdap.gatech.edu/omoponfhir3/fhir/",
    "dataUser":"client",
    "dataPass":"secret",
    "patientId":"46526",
    "terminologyServiceUri":"https://cts.nlm.nih.gov/fhir/",
    "terminologyUser":"jduke99",
    "terminologyPass":"v6R4*SsU39"
}

headers = {'Content-Type': 'application/json'}

result = requests.post('https://apps.hdap.gatech.edu/cql/evaluate', json=full_post_body, headers=headers)
print(result.json())
print(result.elapsed.total_seconds())