library Syphilis_Laboratory_Results version '1.0'
using FHIR version '3.0.0'
include FHIRHelpers version '3.0.0' called FHIRHelpers

codesystem "SNOMED": 'http://snomed.info/sct'
codesystem "LOINC": 'http://loinc.org'

define "SyphilisDiagnosisConcept": Concept {
Code '76272004' from "SNOMED",
Code '444150000' from "SNOMED"
}

define "SyphilisLabConcept": Concept {
Code '8041-6' from "LOINC",
Code '6660-5' from "LOINC",
Code '6580-7' from "LOINC",
Code '22588-8' from "LOINC",
Code '22589-6' from "LOINC",
Code '22591-2' from "LOINC",
Code '22593-8' from "LOINC",
Code '6607-6' from "LOINC",
Code '660-1' from "LOINC",
Code '22459-2' from "LOINC",
Code '5290-2' from "LOINC",
Code '43813-5' from "LOINC",
Code '51783-9' from "LOINC",
Code '22461-8' from "LOINC",
Code '20507-0' from "LOINC",
Code '5292-8' from "LOINC",
Code '22463-4' from "LOINC",
Code '47360-3' from "LOINC",
Code '21030-2' from "LOINC",
Code '22464-2' from "LOINC",
Code '14904-7' from "LOINC",
Code '46203-6' from "LOINC",
Code '87925-4' from "LOINC",
Code '31146-4' from "LOINC",
Code '11084-1' from "LOINC",
Code '31147-2' from "LOINC",
Code '50690-7' from "LOINC",
Code '47476-7' from "LOINC",
Code '47235-7' from "LOINC",
Code '22460-0' from "LOINC",
Code '5289-4' from "LOINC",
Code '22462-6' from "LOINC",
Code '20508-8' from "LOINC",
Code '5291-0' from "LOINC",
Code '73752-8' from "LOINC",
Code '22586-2' from "LOINC",
Code '50689-9' from "LOINC",
Code '9826-9' from "LOINC",
Code '22587-0' from "LOINC",
Code '24312-1' from "LOINC",
Code '17723-8' from "LOINC",
Code '24110-9' from "LOINC",
Code '57032-5' from "LOINC",
Code '5393-4' from "LOINC",
Code '46206-9' from "LOINC",
Code '43238-5' from "LOINC",
Code '51475-2' from "LOINC",
Code '50695-6' from "LOINC",
Code '22590-4' from "LOINC",
Code '26009-1' from "LOINC",
Code '34382-2' from "LOINC",
Code '5394-2' from "LOINC",
Code '71793-4' from "LOINC",
Code '22585-4' from "LOINC",
Code '13288-6' from "LOINC",
Code '47511-1' from "LOINC",
Code '39015-3' from "LOINC",
Code '51474-5' from "LOINC",
Code '49800-6' from "LOINC",
Code '11597-2' from "LOINC",
Code '5392-6' from "LOINC",
Code '63464-2' from "LOINC",
Code '17724-6' from "LOINC",
Code '17725-3' from "LOINC",
Code '41122-3' from "LOINC",
Code '58031-6' from "LOINC",
Code '58751-9' from "LOINC",
Code '6561-5' from "LOINC",
Code '47238-1' from "LOINC",
Code '40679-3' from "LOINC",
Code '17726-1' from "LOINC",
Code '47513-7' from "LOINC",
Code '47361-1' from "LOINC",
Code '47512-9' from "LOINC",
Code '47051-8' from "LOINC",
Code '22592-0' from "LOINC",
Code '51838-1' from "LOINC",
Code '17727-9' from "LOINC",
Code '34954-8' from "LOINC",
Code '68502-4' from "LOINC",
Code '34147-9' from "LOINC",
Code '47236-5' from "LOINC",
Code '69946-2' from "LOINC",
Code '6562-3' from "LOINC",
Code '47237-3' from "LOINC",
Code '40680-1' from "LOINC",
Code '17729-5' from "LOINC",
Code '47514-5' from "LOINC",
Code '47063-3' from "LOINC",
Code '22594-6' from "LOINC",
Code '51839-9' from "LOINC",
Code '17728-7' from "LOINC",
Code '29310-0' from "LOINC",
Code '26658-5' from "LOINC"
}

context Patient

define "Syphilis_Condition": [Condition: Code in "SyphilisDiagnosisConcept"]
define "IndexEvent": "Syphilis_Condition" E return (E.onset as FHIR.dateTime)
define "Syphillis_Test_Obs": [Observation: Code in "SyphilisLabConcept"]

define "Syphilis_Test_Result": from "Syphillis_Test_Obs" target
    let codeStringFormat: target.code.coding[0].code+'^'+target.code.coding[0].system + '^' + target.code.coding[0].code+'^'+target.code.coding[0].display
return all Tuple {
    fhirResourceId: target.id,
    questionConcept: '1234',
    sourceNote: codeStringFormat + ' ' + ToString(target.value as FHIR.Quantity),
    answerValue: codeStringFormat + ' ' + ToString(target.value as FHIR.Quantity),
    valueType: 'String'
}
