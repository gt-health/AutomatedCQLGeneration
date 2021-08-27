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
define "EventReturn": "Syphilis_Condition" E return (E.onset as FHIR.dateTime)
define "Penicillin_MS": [MedicationStatement: Code in "PenicillinConcept"] target
	with "EventReturn" e
		such that (target.effective as FHIR.dateTime) after e + 2 weeks and (target.effective as FHIR.dateTime) before e + 4 weeks
		or FHIRHelpers.ToInterval((target.effective)) overlaps Interval[e + 2 weeks, e + 4 weeks]
define "FirstPenicillin_MS": First(Penicillin_MS)
define "FirstPenicillin_MSTuple": from FirstPenicillin_MS target
	return Tuple {
		questionConcept: '20000005',
		sourceValue: target.medication.coding[0].code+'^'+target.medication.coding[0].system, 
		answerValue: 'http://www.nlm.nih.gov/research/umls/rxnorm^7980^penicillin G',
		resultType: 'Drug'
	}
define "Ceftriaxone_MS": [MedicationStatement: Code in "CeftriaxoneConcept"] target
	with "EventReturn" e
		such that (target.effective as FHIR.dateTime) after e + 2 weeks and (target.effective as FHIR.dateTime) before e + 4 weeks
		or FHIRHelpers.ToInterval((target.effective)) overlaps Interval[e + 2 weeks, e + 4 weeks]
define "FirstCeftriaxone_MS": First(Ceftriaxone_MS)
define "FirstCeftriaxone_MSTuple": from FirstCeftriaxone_MS target
	return Tuple {
		questionConcept: '20000005',
		sourceValue: target.medication.coding[0].code+'^'+target.medication.coding[0].system, 
		answerValue: 'http://www.nlm.nih.gov/research/umls/rxnorm^1665021^ceftriaxone 1000 MG Injection',
		resultType: 'Drug'
	}
define "Penicillin_MS_DosageTuple": from FirstPenicillin_MS target
	return Tuple {
		fhirResourceId: target.id,
		questionConcept: '20000005',
		sourceValue: (target.dosage.dose as FHIR.Quantity).value + " " + (target.dosage.dose as FHIR.Quantity).unit,
		answerValue: 'target.dosage.dose.value + " " + target.dosage.dose.unit',
		resultType: 'Drug',
		field: target.dosage.dose.value
	}
define "Penicillin_MS_Date_Medication_StartedTuple": from FirstPenicillin_MS target
	return Tuple {
		fhirResourceId: target.id,
		questionConcept: '20000005',
		sourceValue: target.effective as FHIR.dateTime, 
		answerValue: 'target.effective as FHIR.dateTime',
		resultType: 'Drug',
		field: target.effective
	}
define "Ceftriaxone_MS_DoseTuple": from FirstCeftriaxone_MS target
	return Tuple {
		fhirResourceId: target.id,
		questionConcept: '20000005',
		sourceValue: target.dosage.dose.value, 
		answerValue: 'target.dosage.dose.value',
		resultType: 'Drug',
		field: target.dosage.dose.value
	}
define "Ceftriaxone_MS_Dosage_UnitTuple": from FirstCeftriaxone_MS target
	return Tuple {
		fhirResourceId: target.id,
		questionConcept: '20000005',
		sourceValue: target.dosage.dose.unit, 
		answerValue: 'target.dosage.dose.unit',
		resultType: 'Drug',
		field: target.dosage.dose.unit
	}
define "Ceftriaxone_MS_Date_Medication_StartedTuple": from FirstCeftriaxone_MS target
	return Tuple {
		fhirResourceId: target.id,
		questionConcept: '20000005',
		sourceValue: target.effective as FHIR.dateTime, 
		answerValue: 'target.effective as FHIR.dateTime',
		resultType: 'Drug',
		field: target.effective
	}
define "returnAggregator":
	"Penicillin_MS" union "Ceftriaxone_MS" 