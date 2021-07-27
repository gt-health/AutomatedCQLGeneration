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

class SimpleRetrievalEntity(BaseEntity):
    def __init__(self, group, fhir_resource, code_system, codes, valueset_oid):
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
        self.aggregator = AggregateEntity(data['returnAggregator'])
        
        
class ConceptEntity(BaseEntity):
    def __init__(self, data):
        self.entityType = 'ConceptEntity'
        self.name = data['name']
        self.codesets = list(map(lambda x: CodesetEntity(x), data['codesets']))
        
class CodesetEntity(BaseEntity):
    def __init__(self, data):
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
        
class InclusionEntity(BaseEntity):
    def __init__(self, data):
        self.entityType = "InclusionEntity"
        self.fhirResource = data['fhirResource']
        self.concept = data['concept']
        self.resultType = data['resultType']
        self.resultAnswer = data['resultAnswer']
        self.sourceValue = data['sourceValue']
        self.filterType = data['filterType']
        
class AggregateEntity(BaseEntity):
    def __init__(self, data):
        self.entityType = "AggregateEntity"
        self.aggregateType = data['type']











