
        library EventAndInclusion version '1.0'
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

        define "myConcept": Concept {
            Code 'A56' from "http://loinc.org", 
            Code 'A57' from "http://loinc.org"
        }

        define "Syphilis_Condition": [Condition: Code in "myConcept"]
        define "EventOnset" E return E.onsetDateTime