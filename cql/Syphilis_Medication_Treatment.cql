library Syphilis_Medication_Treatment version '4.0'
using FHIR version '3.0.0'
include FHIRHelpers version '3.0.0' called FHIRHelpers

codesystem "SNOMED": 'http://snomed.info/sct'
codesystem "RxNorm": 'http://www.nlm.nih.gov/research/umls/rxnorm'

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
define "Penicillin_MS": [MedicationStatement: Code in "PenicillinConcept"]
define "Ceftriaxone_MS": [MedicationStatement: Code in "CeftriaxoneConcept"]

define "Syphilis_Condition_DiagnosisTuple": from "Syphilis_Condition" target
	return all Tuple {
		fhirResourceId: target.id,
		fhirField: 'code.coding[0].code',
		questionConcept: '2000000002',
		sourceNote: target.code.coding[0].code+'^'+target.code.coding[0].system, 
		answerValue: 'http://snomed.info/sct^76272004^Syphilis (disorder)',
		valueType: 'String'
	}
define "Syphilis_Condition_Onset_DateTimeTuple": from "Syphilis_Condition" target
	return all Tuple {
		fhirResourceId: target.id,
		fhirField: 'onset',
		questionConcept: '2000000002',
		sourceNote: StripType(ToString(FHIRHelpers.ToDateTime(target.onset as FHIR.dateTime))), 
		answerValue: StripType(ToString(FHIRHelpers.ToDateTime(target.onset as FHIR.dateTime))),
		valueType: 'String'
	}
define "Syphilis_Condition_Onset_PeriodTuple": from "Syphilis_Condition" target
	return all Tuple {
		fhirResourceId: target.id,
		fhirField: 'onset',
		questionConcept: '2000000002',
		sourceNote: start of FHIRHelpers.ToInterval(target.onset as FHIR.Period), 
		answerValue: start of FHIRHelpers.ToInterval(target.onset as FHIR.Period),
		valueType: 'String'
	}
define "Penicillin_MS_MedicationTuple": from "Penicillin_MS" target
	return all Tuple {
		fhirResourceId: target.id,
		fhirField: 'medication.coding[0].code',
		questionConcept: '2000000004',
		sourceNote: target.medication.coding[0].code+'^'+target.medication.coding[0].system, 
		answerValue: 'http://www.nlm.nih.gov/research/umls/rxnorm^7980^penicillin G',
		valueType: 'String'
	}
define "Penicillin_MS_DosageTuple": from "Penicillin_MS" target
	return all Tuple {
		fhirResourceId: target.id,
		fhirField: 'dosage[0].dose',
		questionConcept: '2000000004',
		sourceNote: ToString(FHIRHelpers.ToQuantity(("target".dosage[0].dose as FHIR.Quantity))), 
		answerValue: target.dosage[0].dose as FHIR.Quantity,
		valueType: 'Quantity'
	}
define "Penicillin_MS_Date_Medication_Started_DateTimeTuple": from "Penicillin_MS" target
	return all Tuple {
		fhirResourceId: target.id,
		fhirField: 'effective',
		questionConcept: '2000000004',
		sourceNote: StripType(ToString(FHIRHelpers.ToDateTime(target.effective as FHIR.dateTime))), 
		answerValue: StripType(ToString(FHIRHelpers.ToDateTime(target.effective as FHIR.dateTime))),
		valueType: 'String'
	}
define "Penicillin_MS_Date_Medication_Started_PeriodTuple": from "Penicillin_MS" target
	return all Tuple {
		fhirResourceId: target.id,
		fhirField: 'effective',
		questionConcept: '2000000004',
		sourceNote: start of FHIRHelpers.ToInterval(target.effective as FHIR.Period), 
		answerValue: start of FHIRHelpers.ToInterval(target.effective as FHIR.Period),
		valueType: 'String'
	}
define "Ceftriaxone_MS_MedicationTuple": from "Ceftriaxone_MS" target
	return all Tuple {
		fhirResourceId: target.id,
		fhirField: 'medication.coding[0].code',
		questionConcept: '2000000004',
		sourceNote: target.medication.coding[0].code+'^'+target.medication.coding[0].system, 
		answerValue: 'http://www.nlm.nih.gov/research/umls/rxnorm^7980^penicillin G',
		valueType: 'String'
	}
define "Ceftriaxone_MS_DosageTuple": from "Ceftriaxone_MS" target
	return all Tuple {
		fhirResourceId: target.id,
		fhirField: 'dosage[0].dose',
		questionConcept: '2000000004',
		sourceNote: ToString(FHIRHelpers.ToQuantity(("target".dosage[0].dose as FHIR.Quantity))), 
		answerValue: target.dosage[0].dose as FHIR.Quantity,
		valueType: 'Quantity'
	}
define "Ceftriaxone_MS_Date_Medication_Started_DateTimeTuple": from "Ceftriaxone_MS" target
	return all Tuple {
		fhirResourceId: target.id,
		fhirField: 'effective',
		questionConcept: '2000000004',
		sourceNote: StripType(ToString(FHIRHelpers.ToDateTime(target.effective as FHIR.dateTime))), 
		answerValue: StripType(ToString(FHIRHelpers.ToDateTime(target.effective as FHIR.dateTime))),
		valueType: 'String'
	}
define "Ceftriaxone_MS_Date_Medication_Started_PeriodTuple": from "Ceftriaxone_MS" target
	return all Tuple {
		fhirResourceId: target.id,
		fhirField: 'effective',
		questionConcept: '2000000004',
		sourceNote: start of FHIRHelpers.ToInterval(target.effective as FHIR.Period), 
		answerValue: start of FHIRHelpers.ToInterval(target.effective as FHIR.Period),
		valueType: 'String'
	}

define "returnAggregator":
	"Penicillin_MS" union "Ceftriaxone_MS" 
	
define function StripType(Input System.String):
	case
		when BeginIndex(Input) = -1 then Input
		when EndIndex(Input) = -1 then Input
		else Substring(Input, BeginIndex(Input) + 1, EndIndex(Input) - BeginIndex(Input) - 1)
	end

define function BeginIndex(Input System.String):
	LastPositionOf('[', Input)

define function EndIndex(Input System.String):
	PositionOf(']', Input)
