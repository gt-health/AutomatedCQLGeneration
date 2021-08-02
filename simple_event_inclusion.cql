library Syphilis_Medication_Treatment version '1.0'
using FHIR version '3.0.0'
include FHIRHelpers version '3.0.0' called FHIRHelpers
context Patient

codesystem "RXNORM": 'http://www.nlm.nih.gov/research/umls/rxnorm'
codesystem "SNOMED": 'http://snomed.info/sct'

define "SyphilisConcept": Concept {
	Code '76272004' from SNOMED,
	Code '444150000' from SNOMED
}
define "PenicillinConcept": Concept {
	Code '7984' from RXNORM,
	Code '7980' from RXNORM
}
define "Syphilis_Condition": [Condition: Code in "SyphilisConcept"]
define "EventReturn" E return E.onsetDateTime
define "Penicillin_MS": [MedicationStatement: Code in "PenicillinConcept"] target
	where target.effectiveDateTime after "EventReturn" + 2 weeks and target.effectiveDateTime before "EventReturn" + 4 weeks
define "FirstPenicillin_MS": First(Penicillin_MS)
define "FirstPenicillin_MSTuple": from FirstPenicillin_MS target
	return Tuple { questionConcept: '20000005',
		sourceValue: target.medication.coding[0].code+'^'+target.medication.coding[0].system, 
		answerValue: 'http://www.nlm.nih.gov/research/umls/rxnorm^7980^penicillin G',
		resultType: 'Drug',
		dateTime: (target.effectiveDateTime as FHIR.period).start.value}