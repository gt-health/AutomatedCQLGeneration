#!/usr/bin/env python3
# -*- coding: utf-8 -*-

cql_template_header = '''
        library {} version '1.0'
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
'''


basic_data_entity_template = '''
define final {}:
    {}
'''
cql_valueset_template = '''
        valueset "{}_valueset": '{}'
'''

pt_define = '''
    define "Pt": [Patient]

    '''

cql_simple_define_template = '''
    {}
    {}
'''
cql_template = '''
        library Retrieve2 version '1.0'
        using FHIR version '3.0.0'
        include FHIRHelpers version '3.0.0' called FHIRHelpers
        codesystem "LOINC": 'http://loinc.org'
        codesystem "SNOMED": 'urn:oid:2.16.840.1.113883.6.96'
        codesystem "RxNorm": 'http://www.nlm.nih.gov/research/umls/rxnorm'
        codesystem "CPT": 'http://www.ama-assn.org/go/cpt'
        codesystem "ICD9": 'urn:oid:2.16.840.1.113883.6.42'
        codesystem "ICD10": 'urn:oid:2.16.840.1.113883.6.3'
        codesystem USCoreEthnicitySystem: 'urn:oid:2.16.840.1.113883.6.238' 
        codesystem RelationshipType: 'urn:oid:2.16.840.1.113883.4.642.3.449'

        {}
        context Patient
{}

{}
{}
'''

# +
cql_concept_template = '''
        define "%s": Concept {
            %s
        }
'''


cql_filter_where_in_clause_template =  '''
        target
            where target.{} in {}
'''

cql_filter_where_during_clause_template =  '''
        target
            where target.{} during Interval[{},{}]
'''

cql_filter_where_before_clause_template =  '''
        target
            where target.{} before {}
'''

cql_filter_where_after_clause_template =  '''
        target
            where target.{} after {}
'''

cql_with_relationship_template = """
        target1
            with {} target2
                such that {}
"""

cql_without_relationship_template = """
        target1
            without {} target2
                such that target1.{} {} target2.{}
"""

# -

# Code '26464-8' from "LOINC",
# Code '804-5' from "LOINC",
# Code '6690-2' from "LOINC",
# Code '49498-9' from "LOINC"

# +

cql_retrieval = '''\n        define "{}": [{}: Code in "{}"]'''

cql_event_return = '''\n        define "Event{}" E return E.{}'''

cql_result_template = '''
       define "{}": 
            {}
'''

cql_result_template_res = ''' [{}]'''

cql_result_template_cs = ''' [{}: Code in "{}_concepts"]'''

cql_result_template_vs = '''[{}:"{}_valueset"]'''

cql_task_template = '''
define final %s:
    Clarity.CQLExecutionTask({
        "task_index": %s,
        cql: \"\"\"
                %s
             \"\"\"
    });
'''