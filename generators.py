#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import STU3Templates
import dateutil.parser as parser
import requests
import entities

class STU3Generator:
    baseNameToFinalNameMap = {}
    def generate(script):
        if script.scriptType == 'IndexEventAndInclusionScript':
            return STU3Generator.generateIndexEventAndInclusion(script)

    def generateIndexEventAndInclusion(script):
        STU3Generator.baseNameToFinalNameMap = {}
        script_concepts = []
        atlas_concepts = []
        header = STU3Templates.cql_header.format(script.name)
        for concept in script.concepts:
            if type(concept.codesets) == str:
                atlas_concepts.append(concept)
            else:
                script_concepts.append(concept)
        script_concepts.append(STU3Generator.translateFromAtlas(atlas_concepts))
        codesystems = STU3Generator.generateCodesystems(script_concepts[0])
        concepts = STU3Generator.generateConcepts(script_concepts[0])
        indexEvent = STU3Generator.generateIndexEvent(script.indexEvent)
        aggregatorEntity = None
        if script.returnAggregator:
            aggregatorEntity = script.returnAggregator
        inclusions, inclusion_names = STU3Generator.generateInclusions(script.inclusions, aggregatorEntity)
        deriveds = STU3Generator.generateDervied(script.deriveds)
        aggregator = STU3Generator.generateAggregator(inclusion_names, aggregatorEntity)
        output = '\n'.join([header, codesystems, concepts, '''context Patient\n''', indexEvent, inclusions, deriveds, aggregator])
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

    def translateFromAtlas(concepts):
        output_concepts = []
        for concept in concepts:
            split_url = concept.codesets.split('#')
            full_url = 'WebAPI'.join(split_url)
            if full_url[-10:] != 'expression':
                full_url = ''.join([full_url, '/expression'])
            atlas_concepts = requests.get(url = full_url).json()
            atlas_concept_set = entities.AtlasConceptSetEntity(atlas_concepts)
            pulled_concepts = {}
            for atlas_concept in atlas_concept_set.concepts:
                try: codesystem = list(STU3Templates.codesystems_map.keys())[list(STU3Templates.codesystems_map.values()).index(atlas_concept.VOCABULARY_ID)]
                except: codesystem = atlas_concept.VOCABULARY_ID
                pulled_concepts.update(
                    {atlas_concept.CONCEPT_ID: {'codelist': [atlas_concept.CONCEPT_CODE], 'system': codesystem}})
            output_concepts_list = []

            for key in pulled_concepts:
                output_concepts_list.append(pulled_concepts[key])
            output_json = {'name': concept.name, 'codesets': output_concepts_list}
            output_concept_entity = entities.ConceptEntity(output_json)
            output_concepts.append(output_concept_entity)
        return output_concepts

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

    def generateIndexEvent(indexEvent):
        base_inclusion = STU3Templates.cql_index_event.format(indexEvent.name, indexEvent.fhirResource, indexEvent.conceptReference)
        index_event_return = STU3Templates.cql_index_event_return_with_choice_cast.format(indexEvent.name,indexEvent.returnField.lower(), indexEvent.returnType)
        index_event_output = '\n'.join([base_inclusion, index_event_return])
        return index_event_output

    def convertToISO(date):
        return parser.parse(date).isoformat()

    def generateInclusions(inclusions, aggregator):

        inclusions_cql_list = []
        inclusion_names = []

        for inclusion in inclusions:
            temporal_field = STU3Templates.resource_temporal_map[inclusion.fhirResource]
            inclusion_names.append(inclusion.name)
            base_inclusion = STU3Templates.cql_index_event.format(inclusion.name, inclusion.fhirResource, inclusion.conceptReference)
            
            if inclusion.timeFrame:
                base_inclusion_target = ' '.join([base_inclusion, 'target'])
                if inclusion.timeFrame.start[0]=='+' or inclusion.timeFrame.end[0]=='+':
                    if inclusion.timeFrame.start and inclusion.timeFrame.end:
                        temporal_suffix = STU3Templates.cql_temporal_both_suffix.format(temporal_field, 'dateTime',inclusion.timeFrame.start, temporal_field, 'dateTime', inclusion.timeFrame.end, temporal_field, inclusion.timeFrame.start, inclusion.timeFrame.end)
                    elif inclusion.timeFrame.start:
                        temporal_suffix = STU3Templates.cql_temporal_start_suffix.format(temporal_field, 'dateTime', inclusion.timeFrame.start)
                    elif inclusion.timeFrame.end:
                        temporal_suffix = STU3Templates.cql_temporal_end_suffix.format(temporal_field, 'dateTime', inclusion.timeFrame.end)
                    inclusion_cql = '\n\t'.join([base_inclusion_target, temporal_suffix])
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
                    inclusion_cql = '\n\t'.join([base_inclusion_target, temporal_suffix])
                    inclusions_cql_list.append(inclusion_cql)
            else:
                inclusions_cql_list.append(base_inclusion)

            filter_name = inclusion.name
            if inclusion.filterType != '':
                filter_name = ''.join([inclusion.filterType, inclusion.name])
                filter_cql = STU3Templates.cql_filter.format(filter_name, inclusion.filterType, inclusion.name)
                inclusions_cql_list.append(filter_cql)
                STU3Generator.baseNameToFinalNameMap[inclusion.name] = filter_name

        inclusions_output = '\n'.join(inclusions_cql_list)
        return inclusions_output, inclusion_names

    def generateDervied(deriveds):
        deriveds_cql_list = []
        for derived in deriveds:
            if STU3Generator.baseNameToFinalNameMap:
                baseFinalName = STU3Generator.baseNameToFinalNameMap[derived.baseInclusion]
            else:
                baseFinalName = derived.baseInclusion
            
            if not derived.answerValue.renderAnswerWithCQL:
                answerValue = ''.join(['\'',derived.answerValue.value, '\''])
            else:
                answerValue = derived.answerValue.value

            derived_cql = STU3Templates.cql_shaping_derived.format(derived.name, baseFinalName, derived.fhirField,
                                                                   derived.questionConcept, derived.sourceNote,
                                                                   answerValue, derived.answerValue.valueType)
            deriveds_cql_list.append(derived_cql)
        derived_output = '\n'.join(deriveds_cql_list)
        return derived_output

    def generateAggregator(inclusion_names, aggregator):
        if aggregator and len(inclusion_names)>1:
            aggregate_cql_list = []
            for count, name in enumerate(inclusion_names):
                if count==0: aggregate_cql_list.append(STU3Templates.cql_aggregator_prefix.format('returnAggregator', name))
                else: aggregate_cql_list.append(STU3Templates.cql_aggregator_suffix.format(aggregator.aggregateType, name))
            aggregate_output = ''.join(aggregate_cql_list)
            return aggregate_output

    def handleChoice(choice_field_name):
        choice_types = STU3Templates.fhir_choice_fields_map[choice_field_name]
        choice_texts = []
        for choice_type in choice_types:
            choice_text = STU3Generator.generateChoiceOptionHandler(choice_field_name,choice_type)
            choice_texts.append(choice_text)
        return '\n'.join(choice_texts)


    def generateChoiceOptionHandler(input_field_name,choice_type):
        #STU3Template.${choice_type}_handler.format(input_field_name)
        return ''
