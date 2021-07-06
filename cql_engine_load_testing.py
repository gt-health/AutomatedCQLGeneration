import requests
import aiohttp
import asyncio
import time

cql_engine_url = 'https://apps.hdap.gatech.edu/cql/evaluate'
cql_body_escaped = body = "library \"TestShape\" version '1'\r\nusing FHIR version '3.0.0'\r\ninclude FHIRHelpers version '3.0.0' called FHIRHelpers\r\ncodesystem \"SNOMED\": 'http:\/\/snomed.info\/sct'\r\ndefine \"Chlamydia_Conditions_concepts\": Concept {\r\n  Code '271737000' from \"SNOMED\",\r\n  Code '111904009' from \"SNOMED\"\r\n}\r\ncontext Patient\r\ndefine \"Some_Condition\": [Condition: Code in \"Chlamydia_Conditions_concepts\"]"
body = {"code":cql_body_escaped,"dataServiceUri":"https://apps.hdap.gatech.edu/omoponfhir3/fhir/","dataUser":"client","dataPass":"secret","patientId":"18","terminologyServiceUri":"https://cts.nlm.nih.gov/fhir/","terminologyUser":"jduke99","terminologyPass":"v6R4*SsU39"}

#response_times = []

#for i in range(0,100):
#    response = requests.post(cql_engine_url, json = body)
#    response_times.append(response.elapsed.total_seconds())

#print('Average response time for the request is: ', sum(response_times)/len(response_times), 'for 100 requests.')

async def fetch(url, session):
    async with session.post(url, json=body) as response:
        return await response.read()

async def run(r):
    url = cql_engine_url
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with aiohttp.ClientSession() as session:
        for i in range(r):
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable


loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(100))
loop.run_until_complete(future)