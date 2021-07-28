#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import STU3Templates
import dateutil.parser as parser

class STU3Generator:
    
    def generate(script):
        if script.scriptType == 'EventAndInclusionScript':
            return STU3Generator.generateEventAndInclusion(script)
    
    def generateEventAndInclusion(script):
        header = STU3Templates.cql_header.format(script.name)
        codesystems = STU3Generator.generateCodesystems(script.concepts)
        concepts = STU3Generator.generateConcepts(script.concepts)
        event = STU3Generator.generateEvent(script.event)
        inclusions = STU3Generator.generateInclusions(script.inclusions)
        output = '\n'.join([header, codesystems, concepts, event, inclusions])
        return output

    
    def generateCodesystems(concepts):
        unique_codesystems = set()
        for concept in concepts:
            for codeset in concept.codesets:
                unique_codesystems.add(codeset.system)
        
        codesystems_output = ''
        for codesystem_uri in unique_codesystems:
            common_name = STU3Generator.getCommonCodesystemName(codesystem_uri)
            codesystem_cql = STU3Templates.cql_codesystem.format(common_name, codesystem_uri)
            codesystems_output += codesystem_cql
        
        return codesystems_output
            
    def generateConcepts(concepts):
        
        concepts_cql_list = []
        
        for concept in concepts:
            concept_code_values = []
            for codeset in concept.codesets:
                codesystem_common_name = STU3Generator.getCommonCodesystemName(codeset.system)
                for code in codeset.codelist:
                    concept_code_values.append(STU3Templates.cql_concept_code_template.format(code, codesystem_common_name))
            
            concept_values_block = ',\n\t'.join(concept_code_values)
            concept_cql = STU3Templates.cql_concept_template.format(concept.name, concept_values_block)
            concepts_cql_list.append(concept_cql)
        
        concepts_output = '\n'.join(concepts_cql_list)
        return concepts_output
        
    def getCommonCodesystemName(codesystem):
        if (codesystem in STU3Templates.codesystems_map.keys()):
            return STU3Templates.codesystems_map[codesystem]
        else:
            return codesystem
        
    def generateEvent(event):
        event_cql = STU3Templates.cql_event.format(event.name, event.fhirResource, event.concept)
        event_return_field = ''.join([event.returnField.lower(),event.returnType])
        event_return = STU3Templates.cql_event_return.format(event_return_field)
        event_output = '\n'.join([event_cql, event_return])
        return event_output

    def convertToISO(date):
        return parser.parse(date).isoformat()

    def generateInclusions(inclusions):

        inclusions_cql_list = []

        for inclusion in inclusions:
            temporal_field = STU3Templates.resource_temporal_map[inclusion.fhirResource]

            if inclusion.timeFrame:
                event_cql = STU3Templates.cql_event.format(inclusion.name, inclusion.fhirResource, inclusion.concept)
                event_target = ' '.join([event_cql, 'target'])

                if inclusion.timeFrame.start[0]=='+' or inclusion.timeFrame.end[0]=='+':
                    if inclusion.timeFrame.start and inclusion.timeFrame.end:
                        temporal_suffix = STU3Templates.cql_temporal_both_suffix.format(temporal_field, inclusion.timeFrame.start, temporal_field, inclusion.timeFrame.end)
                    elif inclusion.timeFrame.start:
                        temporal_suffix = STU3Templates.cql_temporal_start_suffix.format(temporal_field, inclusion.timeFrame.start)
                    elif inclusion.timeFrame.end:
                        temporal_suffix = STU3Templates.cql_temporal_end_suffix.format(temporal_field, inclusion.timeFrame.end)
                    inclusion_cql = '\n\t'.join([event_target, temporal_suffix])
                    inclusions_cql_list.append(inclusion_cql)

                elif inclusion.timeFrame.start[0].isnumeric() or inclusion.timeFrame.end[0].isnumeric:
                    if inclusion.timeFrame.start and inclusion.timeFrame.end:
                        start = STU3Generator.convertToISO(inclusion.timeFrame.start)
                        end = STU3Generator.convertToISO(inclusion.timeFrame.end)
                        temporal_suffix = STU3Templates.cql_temporal_interval_suffix.format(temporal_field, start, end)
                    elif inclusion.timeFrame.start:
                        start = STU3Generator.convertToISO(inclusion.timeFrame.start)
                        temporal_suffix = STU3Templates.cql_temporal_datetime_start_suffix.format(temporal_field, start)
                    elif inclusion.timeFrame.end:
                        end = STU3Generator.convertToISO(inclusion.timeFrame.end)
                        temporal_suffix = STU3Templates.cql_temporal_datetime_end_suffix.format(temporal_field, end)
                    inclusion_cql = '\n\t'.join([event_target, temporal_suffix])
                    inclusions_cql_list.append(inclusion_cql)

            if inclusion.filterType:
                filter_name = ''.join([inclusion.filterType, inclusion.name])
                filter_cql = STU3Templates.cql_filter.format(filter_name, inclusion.filterType, inclusion.name)
                inclusions_cql_list.append(filter_cql)

            shaping_cql = STU3Templates.cql_shaping.format(inclusion.name, inclusion.name, inclusion.questionConcept,
                                                           inclusion.sourceValue, inclusion.answerValue, inclusion.resultType,
                                                           temporal_field)
            inclusions_cql_list.append(shaping_cql)

        inclusions_output = '\n'.join(inclusions_cql_list)
        return inclusions_output

