library Syphilis_Medication_Treatment version '1.0'
using FHIR version '3.0.0'
include FHIRHelpers version '3.0.0' called FHIRHelpers

codesystem "RxNorm": 'http://www.nlm.nih.gov/research/umls/rxnorm'
codesystem "SNOMED": 'http://snomed.info/sct'

define "SyphilisConcept": Concept {
	Code '76272004' from "SNOMED",
	Code '444150000' from "SNOMED"
}
define "PenicillinConcept": Concept {
	Code '7984' from "RxNorm",
	Code '7980' from "RxNorm"
}
define "CeftriaxoneConcept": Concept {
	Code '1665021' from "RxNorm"
}
context Patient

define "Syphilis_Condition": [Condition: Code in "SyphilisConcept"]
define "IndexEvent": "Syphilis_Condition" E return (E.onset as FHIR.dateTime)
define "Penicillin_MS": [MedicationStatement: Code in "PenicillinConcept"] target
	with "IndexEvent" e
		such that (target.effective as FHIR.dateTime) after e + 0 weeks and (target.effective as FHIR.dateTime) before e + 4 weeks
		or FHIRHelpers.ToInterval((target.effective)) overlaps Interval[e + 0 weeks, e + 4 weeks]
define "Ceftriaxone_MS": [MedicationStatement: Code in "CeftriaxoneConcept"] target
	with "IndexEvent" e
		such that (target.effective as FHIR.dateTime) after e + 0 weeks and (target.effective as FHIR.dateTime) before e + 4 weeks
		or FHIRHelpers.ToInterval((target.effective)) overlaps Interval[e + 0 weeks, e + 4 weeks]
define "Penicillin_MS_MedicationTuple": from "Penicillin_MS" target
	return all Tuple {
		fhirResourceId: target.id,
		fhirField: 'medication.coding[0].code',
		questionConcept: '200000055',
		sourceNote: target.medication.coding[0].code+'^'+target.medication.coding[0].system, 
		answerValue: 'http://www.nlm.nih.gov/research/umls/rxnorm^7980^penicillin G',
		valueType: 'String'
	}
define "Penicillin_MS_DosageTuple": from "Penicillin_MS" target
	return all Tuple {
		fhirResourceId: target.id,
		fhirField: 'dosage[0].dose',
		questionConcept: '200000066',
		sourceNote: ToString(FHIRHelpers.ToQuantity(("target".dosage[0].dose as FHIR.Quantity))), 
		answerValue: target.dosage[0].dose as FHIR.Quantity,
		valueType: 'Quantity'
	}
define "Penicillin_MS_Date_Medication_StartedTuple": from "Penicillin_MS" target
	return all Tuple {
		fhirResourceId: target.id,
		fhirField: 'effective',
		questionConcept: '200000077',
		sourceNote: ToString(FHIRHelpers.ToDateTime(target.effective as FHIR.dateTime)), 
		answerValue: target.effective as FHIR.dateTime,
		valueType: 'String'
	}
define "returnAggregator":
	"Penicillin_MS" union "Ceftriaxone_MS" 