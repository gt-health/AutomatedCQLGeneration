library Syphilis_Medication_Treatment version '1.0'
using FHIR version '3.0.0'
include FHIRHelpers version '3.0.0' called FHIRHelpers
context Patient

codesystem "LOINC":'http://loinc.org'

define "myConcept": Concept {
    Code A56 from LOINC,
	Code A57 from LOINC
}

define "Syphilis_Condition": [Condition: Code in "myConcept"]
define "EventReturn" E return E.onsetDateTime
define "Penicillin_MS": [MedicationStatement: Code in "myConcept"] target
	where target.effectiveDateTime after eventOnset + 2 weeks and target.effectiveDateTime before eventOnset + 4 weeks
define "FirstPenicillin_MS": First(Penicillin_MS)
define "Penicillin_MSTuple": from Penicillin_MS target
	return Tuple { questionConcept: '20000005',
		sourceValue: target.medication.coding[0].code+'^'+target.medication.coding[0].system, 
		answerValue: 'http://www.nlm.nih.gov/research/umls/rxnorm^7980^penicillin G',
		resultType: 'Drug',
		dateTime: (target.effectiveDateTime as FHIR.period).start.value}