library Syphilis_Medication_Treatment version '1.0'
using FHIR version '3.0.0'
include FHIRHelpers version '3.0.0' called FHIRHelpers
context Patient

codesystem "RxNorm": 'http://www.nlm.nih.gov/research/umls/rxnorm'
codesystem "SNOMED": 'http://snomed.info/sct'

define "SyphilisConcept": Concept {
	Code '76272004' from SNOMED,
	Code '444150000' from SNOMED
}
define "PenicillinConcept": Concept {
	Code '7984' from RxNorm,
	Code '7980' from RxNorm
}
define "CeftriaxoneConcept": Concept {
	Code '1665021' from RxNorm
}
define "Syphilis_Condition": [Condition: Code in "SyphilisConcept"]
define "EventReturn" "Syphilis_Condition" E return E.onsetDateTime
define "Penicillin_MS": [MedicationStatement: Code in "PenicillinConcept"] target
	where target.effectiveDateTime after "EventReturn" + 2 weeks and target.effectiveDateTime before "EventReturn" + 4 weeks
define "FirstPenicillin_MS": First(Penicillin_MS)
define "FirstPenicillin_MSTuple": from FirstPenicillin_MS target
	return Tuple {
		questionConcept: '20000005',
		sourceValue: target.medication.coding[0].code+'^'+target.medication.coding[0].system, 
		answerValue: 'http://www.nlm.nih.gov/research/umls/rxnorm^7980^penicillin G',
		resultType: 'Drug'
	}
define "Ceftriaxone_MS": [MedicationStatement: Code in "CeftriaxoneConcept"] target
	where target.effectiveDateTime after "EventReturn" + 2 weeks and target.effectiveDateTime before "EventReturn" + 4 weeks
define "FirstCeftriaxone_MS": First(Ceftriaxone_MS)
define "FirstCeftriaxone_MSTuple": from FirstCeftriaxone_MS target
	return Tuple {
		questionConcept: '20000005',
		sourceValue: target.medication.coding[0].code+'^'+target.medication.coding[0].system, 
		answerValue: 'http://www.nlm.nih.gov/research/umls/rxnorm^1665021^ceftriaxone 1000 MG Injection',
		resultType: 'Drug'
	}
define "Penicillin_MS_DoseTuple": from FirstPenicillin_MS target
	return Tuple {
		fhirResourceId: target.id,
		questionConcept: '20000005',
		sourceValue: target.dosage.doseAndRate.doseQuantity.value, 
		answerValue: 'target.dosage.doseAndRate.doseQuantity.value',
		resultType: 'Drug',
		field: target.dosage.doseAndRate.doseQuantity.value
	}
define "Penicillin_MS_Dosage_UnitTuple": from FirstPenicillin_MS target
	return Tuple {
		fhirResourceId: target.id,
		questionConcept: '20000005',
		sourceValue: target.dosage.doseAndRate.doseQuantity.unit, 
		answerValue: 'target.dosage.doseAndRate.doseQuantity.unit',
		resultType: 'Drug',
		field: target.dosage.doseAndRate.doseQuantity.unit
	}
define "Penicillin_MS_Date_Medication_StartedTuple": from FirstPenicillin_MS target
	return Tuple {
		fhirResourceId: target.id,
		questionConcept: '20000005',
		sourceValue: target.effectiveDateTime, 
		answerValue: 'target.effectiveDateTime',
		resultType: 'Drug',
		field: target.effectiveDateTime
	}
define "Ceftriaxone_MS_DoseTuple": from FirstCeftriaxone_MS target
	return Tuple {
		fhirResourceId: target.id,
		questionConcept: '20000005',
		sourceValue: target.dosage.doseAndRate.doseQuantity.value, 
		answerValue: 'target.dosage.doseAndRate.doseQuantity.value',
		resultType: 'Drug',
		field: target.dosage.doseAndRate.doseQuantity.value
	}
define "Ceftriaxone_MS_Dosage_UnitTuple": from FirstCeftriaxone_MS target
	return Tuple {
		fhirResourceId: target.id,
		questionConcept: '20000005',
		sourceValue: target.dosage.doseAndRate.doseQuantity.unit, 
		answerValue: 'target.dosage.doseAndRate.doseQuantity.unit',
		resultType: 'Drug',
		field: target.dosage.doseAndRate.doseQuantity.unit
	}
define "Ceftriaxone_MS_Date_Medication_StartedTuple": from FirstCeftriaxone_MS target
	return Tuple {
		fhirResourceId: target.id,
		questionConcept: '20000005',
		sourceValue: target.effectiveDateTime, 
		answerValue: 'target.effectiveDateTime',
		resultType: 'Drug',
		field: target.effectiveDateTime
	}
define "returnAggregator":
	"Penicillin_MS" union "Ceftriaxone_MS" 