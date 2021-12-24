library Syphilis_Medication_Treatment version '1.0'
using FHIR version '3.0.0'
include FHIRHelpers version '3.0.0' called FHIRHelpers

parameter Demographics Tuple { address String, city String, zip String }

define "DemographicsExpression": Demographics { address: 'North Ave', city: 'Atlanta', zip: '30308' }