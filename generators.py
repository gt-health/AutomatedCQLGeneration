#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import STU3Templates

class STU3Generator:
    
    def generate(script):
        if script.scriptType == 'EventAndInclusionScript':
            return STU3Generator.generateEventAndInclusion(script)
    
    def generateEventAndInclusion(script):
        header = STU3Templates.cql_header.format(script.name)
        codesystems = STU3Generator.generateCodesystems(script.concepts)
        concepts = STU3Generator.generateConcepts(script.concepts)
        output = '\n'.join([header, codesystems, concepts])
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
        
        
    def generateEvent: