# Automated CQL Tutorial
This is a quick guide for working with the Automated CQL Generation Tool. This tool
* Reads a .JSON file as configuration
* Generates CQL snippets based on the configuration
* Writes the final CQL script to a file of the same name
The guide will first give a basic overview of JSON as a structure, then the supported JSON definitions.

# Running the Automated CQL Generation tool
The tool can be run via a simple command line interface (CLI). To ensure that it can be run, Python 3.x needs to be installed on your computer. 

1. In Terminal/Command Prompt, navigate to the directory where this repo has been placed
2. Run the command ```pip install -r requirements.txt``` to install the required packages for this tool
3. Run ```python3 automated_cql_generation.py --input --output``` where --input is the optional flag for naming the location of an input JSON (default is input_JSON.JSON in the current directory) and --output is the optional flag for naming the output CQL file (default is the name of the input file in a subdirectory named cql). You can run ```python3 automated_cql_generation.py -h``` at any time to see the descriptions for each of the optional parameters again

# JSON Overview
## External Tutorials
If you would rather learn JSON through a video tutorial, we recommend this overview [on youtube](https://www.youtube.com/watch?v=GpOO5iKzOmY). If you prefer a more visual approach, you can refer to [the beginner's book here](https://beginnersbook.com/2015/04/JSON-tutorial/).
## What Is JSON?
JSON(**J**ava**S**cript **O**bject **N**otation) is a hierarchical data format that is very easily parsed by machines, while also maintaining readability for humans as well. We store JSON as files with a ```.JSON``` extension. Each JSON file is a set of objects, which 
Despite the name, no Javascript is needed to work with JSON.
## JSON Basics
JSON objects are always enclosed between ``{`` and ``}``.
```
{
  "name":"John Appleseed",
  "age":26,
  "favorite color":"blue"
}
```
Each value is a set of ``key:value`` pairs separated by colons, keys are always strings and surrounded by quotes ``""``. Values can be
*  Numbers ``7, 3.1, 4.23478``
* String ``"This is a string"``
* Boolean ``True, False``
* Object ``{...}``
* Array ``[...]``
* Empty, or Null ``null``
## A More Complicated JSON Example
```
{
  "students": [
    { "name": "Abe", "year": 2019, "grade": "A" },
    { "name": "Betty", "year": 2020, "grade": "B" },
    { "name": "Charlie", "year": 2021, "grade": "F" },
    { "name": "Dennis", "year": 2020, "grade": "C" },
  ]
}
```
# CQL JSON Templates
Example CQL template definitions can be found in [cql_template_definitions folder](https://github.com/gt-health/AutomatedCQLGeneration/tree/main/cql_template_definition). The Currently supported JSON templates are defined in a top level key named ``type`` of the .JSON file. The currently support architypes are
* IndexEventAndInclusion
## IndexEventAndInclusion JSON template
IndexEventAndInclusion is a template designed to
* Capture an event given a positive Condition, Observation, Medication, or Procedure
* If successful include other sets within a time frame on the given event
* Create tuples based on other events included previously
* Aggregate the inclusions together through either a union or an intersection

IndexEventAndInclusion JSON files consist of 3 fields

* A list of **concepts**
* A single **event**
* A list of **inclusions**
* A list of **deriveds**
* A single **Aggregator**
## IndexEventAndInclusion Concepts
The concept section defines the concepts to be referenced further in the template.
```
"concepts": [
  {  
    "name": "SyphilisConcept",  
    "codesets": [  
        {  
          "codelist" : ["76272004","444150000"],  
          "system": "http://snomed.info/sct"  
        }  
    ]  
  }
]
```
Generates a CQL snippet:
```
codesystem "SNOMED": 'http://snomed.info/sct'
define "SyphilisConcept": Concept {  
   Code '76272004' from SNOMED,  
   Code '444150000' from SNOMED  
}
```
Each concept consists of a ``name`` which will be referenced later, and a list of ``codesets``.
``codesets`` consist of a ``codelist`` and a ``system`` which describe the set of codes with either a system url, or a common supported system.
### Atlas Url Concepts
Concepts can also be defined in [ohdsi-atlas](http://atlas-demo.ohdsi.org/#/conceptsets) and referenced as a url as so:
```
"concepts":[  
  {  
    "name": "SyphilisConcept",  
    "codesets": "http://atlas-demo.ohdsi.org/#/conceptset/1868958/expression"  
  }
]
```
Generates the same type of CQL snippet:
```
codesystem "SNOMED": 'http://snomed.info/sct'
define "SyphilisConcept": Concept {  
   Code '76272004' from SNOMED,  
   Code '444150000' from SNOMED  
}
```
## IndexEventAndInclusion IndexEvent
Each IndexEventAndInclusion JSON includes a single IndexEvent
```
"indexEvent": {  
  "name": "Syphilis_Condition",  
  "fhirResource": "Condition",  
  "conceptReference": "SyphilisConcept",  
  "returnField": "Onset",  
  "returnType" : "DateTime" 
}
```
Creates a CQL snippet
```
define "Syphilis_Condition": [Condition: Code in "SyphilisConcept"]  
define "EventReturn": "Syphilis_Condition" E return E.onset as FHIR.dateTime
```
The event includes
* A unique ``name``
* A ``fhirResource`` to be used as the resource to query.
* A ``conceptReference`` to reference a previously defined concept set to use in the query. If none are defined, no concept will be used
* A ``returnField`` to define which field in the fhir Resource will be used as the timing event. Common choices are ``Onset, Abatement, Effective, WhenPrepared, Performed``, and are dependent on the ``fhirResource`` being used.
* A ``returnType`` defined in the cases where the fhirResource is a *choice* field, and can be multiple types, the returnType enforces a type.
## IndexEventAndInclusion Inclusion
Each IndexEventAndInclusion JSON may include many Inclusions
```
"inclusions": [  
  {  
    "name": "Penicillin_MS",  
    "fhirResource": "MedicationStatement",  
    "conceptReference": "PenicillinConcept",  
    "filterType": "First",  
    "timeFrameRelativeToIndexEvent": {  
      "start": "+ 2 weeks",  
      "end": "+ 4 weeks"  
    }  
  }
]
```
Creates a CQL snippet
```
define "Penicillin_MS": [MedicationStatement: Code in "PenicillinConcept"] target
	with "IndexEvent" e
		such that (target.effective as FHIR.dateTime) after e + 2 weeks and (target.effective as FHIR.dateTime) before e + 4 weeks
		or FHIRHelpers.ToInterval((target.effective)) overlaps Interval[e + 2 weeks, e + 4 weeks] 
define "FirstPenicillin_MS": First(Penicillin_MS) 
```
Each Inclusion consists of 
* A unique ``name``
* A ``fhirResource`` to query
* A ``conceptReference`` to reference a previously defined concept set to use in the query. If none are defined, no concept will be used
* A ``filterType``, which describes how to filter the results to a singular object, values include ``First,Last``
* A ``timeFrame`` object, with the fields ``start`` and ``end``, describe a time period **in terms of the original event** where the inclusion must be valid. This object can also be empty, contain empty strings as values, or be an empty string instead of an object if there is no filtering time frame


## IndexEventAndInclusion Derived
Each IndexEventAndInclusion JSON may include many Deriveds
```
"deriveds": [
    {
      "name": "Penicillin_MS_Medication",
      "baseInclusion": "Penicillin_MS",
      "fhirField": "medication.coding[0].code",
      "fhirReturnResource": "Observation",
      "questionConcept": "200000055",
      "answerValue": {
        "valueType": "String",
        "renderAnswerWithCQL": false,
        "value": "http://www.nlm.nih.gov/research/umls/rxnorm^7980^penicillin G"
      },
      "sourceNote": "target.medication.coding[0].code+'^'+target.medication.coding[0].system"
    }
]
```
Creates a CQL snippet
```
define "Penicillin_MS_MedicationTuple": from "Penicillin_MS" target
	return all Tuple {
		fhirResourceId: target.id,
		fhirField: 'medication.coding[0].code',
		questionConcept: '200000055',
		sourceNote: target.medication.coding[0].code+'^'+target.medication.coding[0].system, 
		answerValue: 'http://www.nlm.nih.gov/research/umls/rxnorm^7980^penicillin G',
		valueType: 'String'
	}
```
Each Derived consists of
* A unique ``name``
* A ``baseInclusion`` to base the derived off of
* A ``fhirField`` to display where the sourceNote is coming from in the FHIR resource
* A ``fhirReturnResource`` describes the FHIR resource being used
* A ``questionConcept`` is a unique concept code for question being asked per derived
* An ``answerValue`` object that contains the answer valueType, if the answer should be rendered with CQL, and what the result answer value is
* A ``sourceNote`` for displaying the source value