library Simple_Event_Inclusion version '1.0'
using FHIR version '4.0.0'
include FHIRHelpers version '4.0.0' called FHIRHelpers

codesystem "SNOMED": 'http://snomed.info/sct'

define "SyphilisConcept": Concept {
	Code '76272004' from "SNOMED",
	Code '444150000' from "SNOMED"
}
context Patient

define "Syphilis_Condition": [Condition: Code in "SyphilisConcept"]
define "IndexEvent": "Syphilis_Condition" E return (E.onset as FHIR.dateTime)
define "Penicillin_MS": [MedicationStatement: Code in "PenicillinConcept"]
define "FirstPenicillin_MS": First(Penicillin_MS)

