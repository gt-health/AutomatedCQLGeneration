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