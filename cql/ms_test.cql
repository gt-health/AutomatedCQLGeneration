library Test_Dosage version '1.0'
using FHIR version '3.0.0'
include FHIRHelpers version '3.0.0' called FHIRHelpers

context Patient

define "MS": [MedicationStatement]

define "MS_dosage": "MS".dosage
define "MS_dosage_0": "MS".dosage[0]
define "MS_dosage_0_dose": "MS".dosage[0].dose
define "MS_dosage_0_dose_as_quantity": ("MS".dosage[0].dose as FHIR.Quantity)
define "MS_dosage_0_dose_as_quantity_value": ("MS".dosage[0].dose as FHIR.Quantity).value
define "MS_dosage_0_dose_as_quantity_unit": ("MS".dosage[0].dose as FHIR.Quantity).unit
define "MS_dosage_0_dose_as_quantity_value_toString": ToString(("MS".dosage[0].dose as FHIR.Quantity).value)

define "FhirHelper_Quantity": FHIRHelpers.ToQuantity(("MS".dosage[0].dose as FHIR.Quantity))
define "SystemQuantity_asString": ToString("FhirHelper_Quantity")