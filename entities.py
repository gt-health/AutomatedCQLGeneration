#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class BaseEntity:
    def __init__(self):
        self.entityType = 'BaseEntity'
    def __repr__(self):
        print('Trying to print entity of type ', self.entityType)
        return str(vars(self))
    
class BaseScript:
    def __init__(self, data):
        self.scriptType = 'BaseScript'
        self.name = data['name']
    def __repr__(self):
        print('Trying to print script of type ', self.scriptType)
        return str(vars(self))

class ShapedEntity(BaseEntity):
    def __init__(self, data):
        super().__init__()
        self.entityType = 'ShapedEntity'
        self.resultType = data['resultType']
        self.questionConcept = data['questionConcept']
        self.answerValue = data['answerValue']
        self.sourceValue = data['sourceValue']

class SimpleRetrievalEntity(BaseEntity):
    def __init__(self, group, fhir_resource, code_system, codes, valueset_oid):
        super().__init__()
        self.entityType = "SimpleRetrievalEntity"
        self.group = group
        self.fhir_resource = fhir_resource
        self.code_system = code_system
        self.codes = codes
        self.valueset_oid = valueset_oid

class FreeTextEntity(SimpleRetrievalEntity):
    def __init__(self, group, fhir_resource, cql_expression):
        self.entityType = "FreeTextEntity"
        self.group = group
        self.fhir_resource = fhir_resource
        self.cql_expression = cql_expression

class TemporalFilterEntity(SimpleRetrievalEntity):
    def __init__(self, group, fhir_resource, code_system, codes, valueset_oid, where_clause_attribute, where_clause_during_begin, where_clause_during_after):
        self.entityType = "TemporalFilterEntity"
        self.group = group
        self.fhir_resource = fhir_resource
        self.code_system = code_system
        self.codes = codes
        self.valueset_oid = valueset_oid
        self.where_clause_attribute = where_clause_attribute
        self.where_clause_during_begin = where_clause_during_begin
        self.where_clause_during_after = where_clause_during_after

class ValueFilterEntity(SimpleRetrievalEntity):
    def __init__(self, group, fhir_resource, where_clause_attribute, where_clause_value):
        self.entityType = "ValueFilterEntity"
        self.group = group
        self.fhir_resource = fhir_resource
        self.where_clause_attribute = where_clause_attribute
        self.where_clause_value = where_clause_value

class RelatedEntity(SimpleRetrievalEntity):
    def __init__(self, group, fhir_resource, code_system, codes, valueset_oid, relationship_fhir_resource_type, relationship_codes, relationship_code_system, relationship_valueset, relationship_where_clause):
        self.entityType = "RelatedEntity"
        self.group = group
        self.fhir_resource = fhir_resource
        self.code_system = code_system
        self.codes = codes
        self.valueset_oid = valueset_oid
        self.relationship_fhir_resource_type = relationship_fhir_resource_type
        self.relationship_codes = relationship_codes
        self.relationship_code_system = relationship_code_system
        self.relationship_valueset = relationship_valueset
        self.relationship_where_clause = relationship_where_clause

class NonEntity:
    def __init__(self, group, fields):
        self.entityType = "NonEntity"
        self.group = group
        self.fields = fields


    
class EventAndInclusionScript(BaseScript):
    def __init__(self, data):
        super().__init__(data)
        self.scriptType = 'EventAndInclusionScript'
        self.concepts = list(map(lambda x: ConceptEntity(x), data['concepts']))
        self.event = EventEntity(data['event'])
        self.inclusions = list(map(lambda x: InclusionEntity(x), data['inclusions']))
        self.deriveds = list(map(lambda x: DerivedEntity(x), data['deriveds']))
        self.returnAggregator = AggregateEntity(data['returnAggregator'])
        
        
class ConceptEntity(BaseEntity):
    def __init__(self, data):
        super().__init__()
        self.entityType = 'ConceptEntity'
        self.name = data['name']
        if type(data['codesets']) == str: self.codesets = data['codesets']
        else: self.codesets = list(map(lambda x: CodesetEntity(x), data['codesets']))
        
class CodesetEntity(BaseEntity):
    def __init__(self, data):
        super().__init__()
        self.entityType = 'CodesetEntity'
        self.codelist = data['codelist']
        self.system = data['system']

class EventEntity(SimpleRetrievalEntity):
    def __init__(self, data):
        self.entityType = "EventEntity"
        self.name = data['name']
        self.fhirResource = data['fhirResource']
        self.concept = data['concept']
        self.returnField = data['returnField']
        self.returnType = data['returnType']
        
class InclusionEntity(ShapedEntity):
    def __init__(self, data):
        super().__init__(data)
        self.entityType = "InclusionEntity"
        self.name = data['name']
        self.fhirResource = data['fhirResource']
        self.concept = data['concept']
        self.filterType = data['filterType']
        self.timeFrame = TimeFrameEntity(data['timeFrame'])

class DerivedEntity(ShapedEntity):
    def __init__(self, data):
        super().__init__(data)
        self.baseDefinition = data['baseDefinition']
        self.name = data['name']
        self.fhirField = data['fhirField']

class AggregateEntity(BaseEntity):
    def __init__(self, data):
        super().__init__()
        self.entityType = "AggregateEntity"
        self.aggregateType = data['type']

class TimeFrameEntity(BaseEntity):
    def __init__(self, data):
        super().__init__()
        self.entityType = "TimeFrameEntity"
        self.start = data['start']
        self.end = data['end']

class AtlasConceptSetEntity(BaseEntity):
    def __init__(self, data):
        super().__init__()
        self.entityType = 'AtlasConceptSetEntity'
        self.concepts = list(map(lambda x: AtlasConceptEntity(x), data['items']))

class AtlasConceptEntity(BaseEntity):
    def __init__(self, data):
        super().__init__()
        self.entityType = 'AtlasConceptEntity'
        self.CONCEPT_ID = data['concept']['CONCEPT_ID']
        self.CONCEPT_NAME = data['concept']['CONCEPT_NAME']
        self.STANDARD_CONCEPT = data['concept']['STANDARD_CONCEPT']
        self.STANDARD_CONCEPT_CAPTION = data['concept']['STANDARD_CONCEPT_CAPTION']
        self.INVALID_REASON = data['concept']['INVALID_REASON']
        self.INVALID_REASON_CAPTION = data['concept']['INVALID_REASON_CAPTION']
        self.CONCEPT_CODE = data['concept']['CONCEPT_CODE']
        self.DOMAIN_ID = data['concept']['DOMAIN_ID']
        self.VOCABULARY_ID = data['concept']['VOCABULARY_ID']
        self.CONCEPT_CLASS_ID = data['concept']['CONCEPT_CLASS_ID']
