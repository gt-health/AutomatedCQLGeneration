
        library testcsv version '1.0'
        using FHIR version '3.0.0'
        include FHIRHelpers version '3.0.0' called FHIRHelpers
        codesystem "LOINC": 'http://loinc.org'
        codesystem "SNOMED": 'http://snomed.info/sct'
        codesystem "RxNorm": 'http://www.nlm.nih.gov/research/umls/rxnorm'
        codesystem "CPT": 'http://www.ama-assn.org/go/cpt'
        codesystem "ICD9": 'urn:oid:2.16.840.1.113883.6.42'
        codesystem "ICD10": 'urn:oid:2.16.840.1.113883.6.3'
        codesystem USCoreEthnicitySystem: 'urn:oid:2.16.840.1.113883.6.238' 
        codesystem RelationshipType: 'urn:oid:2.16.840.1.113883.4.642.3.449'

        context Patient

        define "ChlamydiaConditions_concepts": Concept {
            Code 'A56' from "http://snomed.info/sct", 
            Code 'A56.00' from "http://snomed.info/sct"
        }

       define "ChlamydiaConditions": 
             [Condition: Code in "ChlamydiaConditions_concepts"]

       define "ProceduresRefused": 
            [Procedure: Code in ['someCode'] p where p.status in ['not done'] and p.statusReason in ['183944003']] /*Procedure refused */

       define "ChlamydiaDuring2019": 
             [Condition: Code in "ChlamydiaDuring2019_concepts"]
        target
            where target.onset during Interval[@2019-01-01T00:00:00,@2020-01-01T00:00:00]
